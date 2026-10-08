#!/usr/bin/env node
// Synthesize the locked narration (SCRIPT.md) with Gemini TTS, one WAV per line.
//
// Auth: no key is sent. In this cloud environment the egress proxy adds the
// x-goog-api-key header to every request to generativelanguage.googleapis.com.
// If GEMINI_API_KEY is set locally it is used instead.
//
// Usage: node tools/gemini-vo.mjs [--voice Algieba] [--only 2,5] [--probe]
//   writes assets/voice/line-NN.wav and assets/voice/vo-manifest.json
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const opt = (name, def) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : def;
};
const VOICE = opt("voice", "Algieba");
const ONLY = opt("only", "")
  .split(",")
  .filter(Boolean)
  .map(Number);
const MODELS = ["gemini-3.8-flash-tts", "gemini-2.5-pro-preview-tts", "gemini-2.5-flash-preview-tts"];
const BASE = "https://generativelanguage.googleapis.com/v1beta";
const headers = { "Content-Type": "application/json" };
if (process.env.GEMINI_API_KEY) headers["x-goog-api-key"] = process.env.GEMINI_API_KEY;

function parseScript() {
  const md = readFileSync(join(ROOT, "SCRIPT.md"), "utf8");
  const direction = /\*\*Voice direction:\*\*\s*(.+)/.exec(md)?.[1].trim() ?? "";
  const lines = [];
  for (const sec of md.split(/\n## /).slice(1)) {
    const m = /^Line (\d+) — ([^(]+)\(Frame (\d+)\)/.exec(sec);
    if (!m) continue;
    const delivery = /\*\*Delivery:\*\*\s*(.+)/.exec(sec)?.[1].trim() ?? "";
    const text = sec
      .split("\n")
      .filter((l) => l.startsWith("    "))
      .map((l) => l.trim())
      .join(" ");
    lines.push({ n: +m[1], label: m[2].trim(), frame: +m[3], text, style: `${direction} ${delivery}`.trim() });
  }
  return lines;
}

function pcmToWav(pcm, rate) {
  const h = Buffer.alloc(44);
  h.write("RIFF");
  h.writeUInt32LE(36 + pcm.length, 4);
  h.write("WAVEfmt ", 8);
  h.writeUInt32LE(16, 16);
  h.writeUInt16LE(1, 20);
  h.writeUInt16LE(1, 22);
  h.writeUInt32LE(rate, 24);
  h.writeUInt32LE(rate * 2, 28);
  h.writeUInt16LE(2, 32);
  h.writeUInt16LE(16, 34);
  h.write("data", 36);
  h.writeUInt32LE(pcm.length, 40);
  return Buffer.concat([h, pcm]);
}

const toWav = (b64, mime = "") => {
  const bytes = Buffer.from(b64, "base64");
  if (bytes.toString("ascii", 0, 4) === "RIFF") return bytes;
  const rate = Number(/rate=(\d+)/i.exec(mime)?.[1] ?? 24000);
  return pcmToWav(bytes, rate);
};

// 3.8 models: Interactions API with a speech_metadata style annotation.
async function viaInteractions(model, { text, style }) {
  const res = await fetch(`${BASE}/interactions`, {
    method: "POST",
    headers,
    signal: AbortSignal.timeout(180_000),
    body: JSON.stringify({
      model,
      input: [{ type: "user_input", content: [{ type: "text", text, annotations: [{ type: "speech_metadata", style }] }] }],
      response_format: { type: "audio", mime_type: "audio/wav" },
      generation_config: { speech_config: [{ voice: VOICE }] },
      store: false,
    }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${(await res.text()).slice(0, 300)}`);
  const p = await res.json();
  const part = (p.steps ?? []).filter((s) => s.type === "model_output").flatMap((s) => s.content ?? []).find((c) => c.type === "audio");
  if (!part?.data) throw new Error(`no audio (status ${p.status})`);
  return toWav(part.data, part.mime_type);
}

// 2.5 preview models: generateContent with a delivery prompt before the transcript.
async function viaGenerateContent(model, { text, style }) {
  const res = await fetch(`${BASE}/models/${model}:generateContent`, {
    method: "POST",
    headers,
    signal: AbortSignal.timeout(180_000),
    body: JSON.stringify({
      contents: [{ parts: [{ text: `${style}\nLis exactement le texte suivant, sans rien ajouter :\n\n${text}` }] }],
      generationConfig: {
        responseModalities: ["AUDIO"],
        speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: VOICE } } },
      },
    }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${(await res.text()).slice(0, 300)}`);
  const p = await res.json();
  const part = p.candidates?.[0]?.content?.parts?.find((x) => x.inlineData);
  if (!part) throw new Error("no audio part");
  return toWav(part.inlineData.data, part.inlineData.mimeType);
}

async function synth(line) {
  const errors = [];
  for (const model of MODELS) {
    try {
      const wav = model.startsWith("gemini-3.8") ? await viaInteractions(model, line) : await viaGenerateContent(model, line);
      return { wav, model };
    } catch (e) {
      errors.push(`${model}: ${e.message}`);
    }
  }
  throw new Error(errors.join(" | "));
}

if (args.includes("--probe")) {
  const res = await fetch(`${BASE}/models?pageSize=200`, { headers });
  const body = await res.json();
  if (!res.ok) {
    console.error("probe failed:", res.status, body.error?.message);
    process.exit(1);
  }
  console.log("TTS models:", (body.models ?? []).map((m) => m.name).filter((n) => n.includes("tts")).join(", ") || "(none listed)");
  process.exit(0);
}

const lines = parseScript().filter((l) => !ONLY.length || ONLY.includes(l.n));
const outDir = join(ROOT, "assets/voice");
mkdirSync(outDir, { recursive: true });
const manifestPath = join(outDir, "vo-manifest.json");
let manifest = {};
try {
  manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
} catch {}
let failed = 0;
for (const line of lines) {
  const file = `line-${String(line.n).padStart(2, "0")}.wav`;
  try {
    const { wav, model } = await synth(line);
    writeFileSync(join(outDir, file), wav);
    const rate = wav.readUInt32LE(24);
    const seconds = (wav.length - 44) / (rate * 2);
    manifest[line.n] = { file: `assets/voice/${file}`, frame: line.frame, label: line.label, text: line.text, voice: VOICE, model, seconds: +seconds.toFixed(2) };
    console.log(`✓ line ${line.n} (${model}) ${seconds.toFixed(2)}s`);
  } catch (e) {
    failed++;
    console.error(`✗ line ${line.n}: ${e.message}`);
  }
}
writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + "\n");
process.exit(failed ? 1 : 0);
