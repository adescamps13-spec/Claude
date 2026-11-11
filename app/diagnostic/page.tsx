import type { Metadata } from "next";
import { connection } from "next/server";
import { Suspense } from "react";
import { APIErrorCode, isNotionClientError } from "@notionhq/client";
import { DATA_SOURCES, JetonManquantError, getNotion } from "@/lib/notion";

export const metadata: Metadata = {
  title: "Diagnostic · Electra Brand",
  robots: { index: false, follow: false },
};

const ATTENDU = 19;

type Resultat =
  | { ok: true; total: number }
  | { ok: false; titre: string; aide: string };

async function compterLesAssets(): Promise<Resultat> {
  // Relu côté serveur à chaque visite : jamais de résultat mis en cache.
  await connection();
  try {
    const notion = getNotion();
    let total = 0;
    let curseur: string | undefined = undefined;
    do {
      const page = await notion.dataSources.query({
        data_source_id: DATA_SOURCES.assets,
        start_cursor: curseur,
        page_size: 100,
        result_type: "page",
      });
      total += page.results.length;
      curseur = page.has_more ? (page.next_cursor ?? undefined) : undefined;
    } while (curseur);
    return { ok: true, total };
  } catch (erreur) {
    if (erreur instanceof JetonManquantError) {
      return {
        ok: false,
        titre: "Le jeton Notion est absent",
        aide: "Ajoutez la variable NOTION_TOKEN dans les réglages de Vercel (Settings → Environment Variables), puis relancez le déploiement.",
      };
    }
    if (isNotionClientError(erreur)) {
      switch (erreur.code) {
        case APIErrorCode.Unauthorized:
          return {
            ok: false,
            titre: "Le jeton Notion est refusé",
            aide: "Le jeton collé dans Vercel n'est pas reconnu par Notion. Recopiez-le depuis la page de l'intégration Notion, remplacez la valeur de NOTION_TOKEN dans Vercel, puis relancez le déploiement.",
          };
        case APIErrorCode.ObjectNotFound:
        case APIErrorCode.RestrictedResource:
          return {
            ok: false,
            titre: "L'accès à la banque d'assets est refusé",
            aide: "Le jeton fonctionne, mais l'intégration n'a pas accès à la base. Dans Notion, ouvrez la page racine de la maquette, menu « ••• » → Connexions, et ajoutez l'intégration.",
          };
        case APIErrorCode.RateLimited:
          return {
            ok: false,
            titre: "Notion est momentanément saturé",
            aide: "Trop de requêtes en peu de temps. Attendez une minute puis rechargez la page.",
          };
        default:
          return {
            ok: false,
            titre: "Notion a répondu par une erreur",
            aide: `Code renvoyé par Notion : ${erreur.code}. Transmettez ce code pour que l'on puisse corriger.`,
          };
      }
    }
    return {
      ok: false,
      titre: "Notion ne répond pas",
      aide: "La connexion à Notion a échoué pour une raison inattendue. Rechargez la page dans un instant.",
    };
  }
}

async function ResultatDiagnostic() {
  const resultat = await compterLesAssets();
  return resultat.ok ? (
    <section
      className={`rounded-2xl border p-6 ${
        resultat.total === ATTENDU
          ? "border-emerald-200 bg-emerald-50 text-emerald-950"
          : "border-amber-200 bg-amber-50 text-amber-950"
      }`}
    >
      <p className="text-5xl font-semibold">{resultat.total}</p>
      <p className="mt-2 text-lg">
        {resultat.total > 1 ? "fiches trouvées" : "fiche trouvée"} dans la
        banque d&apos;assets
      </p>
      <p className="mt-4 text-sm">
        {resultat.total === ATTENDU
          ? `Tout est en ordre : ${ATTENDU} fiches étaient attendues.`
          : `La connexion fonctionne, mais ${ATTENDU} fiches étaient attendues. À signaler avant d'aller plus loin.`}
      </p>
    </section>
  ) : (
    <section
      role="alert"
      className="rounded-2xl border border-rose-200 bg-rose-50 p-6 text-rose-950"
    >
      <h2 className="text-xl font-semibold">{resultat.titre}</h2>
      <p className="mt-3">{resultat.aide}</p>
    </section>
  );
}

export default function DiagnosticPage() {
  return (
    <main className="mx-auto flex w-full max-w-xl flex-1 flex-col justify-center gap-6 px-6 py-16">
      <p className="text-sm uppercase tracking-widest text-neutral-500">
        Diagnostic
      </p>
      <h1 className="text-3xl font-semibold">Connexion à Notion</h1>

      <Suspense
        fallback={
          <p
            role="status"
            className="rounded-2xl border border-neutral-200 p-6 text-neutral-500"
          >
            Interrogation de Notion en cours…
          </p>
        }
      >
        <ResultatDiagnostic />
      </Suspense>

      <p className="text-sm text-neutral-500">
        Cette page est temporaire. Elle n&apos;affiche jamais le jeton et sera
        retirée avant la démo.
      </p>
    </main>
  );
}
