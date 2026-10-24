# REVIEW (delivery note, v3 narrated 45 s)

**Render**: `renders/electra-45s-vo.mp4`, 45.0 s, 1080x1920, 30 fps, H.264 + AAC.
`hyperframes check`: ok (0 errors). Audio measured on the file: -15.8 LUFS integrated, true peak -1.4 dBTP, no clipping.
**Measured, not heard**: I cannot listen. The 10 voice lines were transcribed back by Gemini and match the script word for word.

## What changed from v2
- French voiceover (Gemini TTS `gemini-3.8-flash-tts`, voice "Puck", directed energetic/warm), script in `audio_request.json`,
  files in `assets/voice/` (loudness-normalised to -14 LUFS; raw takes kept out of git in `.media/vo-raw/`).
- The whole film is retimed on the voice: crates land on the spoken questions, the lift-off on "portons", coins on "Electra+",
  logo / rating / CTA on "Electra" / "4,8" / "Téléchargez".
- More energy: title slams, camera push-ins, bumps and shakes on every impact, speed lines and a rolling whip on the road,
  proof scenes compressed to the voice (designed timelines played 1.03-1.39x via a nested timeScale).
- End card now follows the voice: logo -> 4,8 + stars -> signature -> CTA, all held together.

## No music
No usable music source in this environment: Lyria 3 has a zero free-tier quota on this Gemini key, Lyria RealTime needs
WebSockets (not allowed by the environment proxy), MusicGen weights (Hugging Face) and Openverse are blocked.
To add one: drop a track in `assets/bgm/` and say so; the cuts will be re-snapped to its beats (`npx hyperframes beats`).

## Weakest shot / with more time
- A music bed is the biggest missing piece for energy.
- Gemini free tier allows 10 TTS requests/day: re-takes of a line wait until the quota resets.

## Warnings kept on purpose
- `line_unread` on SVG labels: false positives (the SVG is redrawn every frame).
- One `contrast_aa_failure` sample during the dive (a tag mid-zoom) and one `content_overlap` info on route pins mid-move.
