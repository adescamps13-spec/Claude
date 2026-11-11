import Link from "next/link";

export default function Home() {
  return (
    <main className="mx-auto flex w-full max-w-xl flex-1 flex-col justify-center gap-6 px-6 py-16">
      <p className="text-2xl font-semibold">
        Electra <span className="font-normal text-neutral-500">Brand</span>
      </p>
      <h1 className="text-3xl font-semibold">Le site est en préparation.</h1>
      <p className="text-neutral-600">
        Le socle technique est en place. Prochaine étape : vérifier la
        connexion à Notion.
      </p>
      <Link
        href="/diagnostic"
        className="w-fit rounded-full bg-neutral-900 px-5 py-3 text-white hover:bg-neutral-700"
      >
        Ouvrir le diagnostic
      </Link>
    </main>
  );
}
