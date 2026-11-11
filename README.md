# Electra Brand (prototype)

Interface interne de la marque Electra : demandes à l'équipe brand, fondamentaux de marque, banque d'assets et assistants.

- Next.js (App Router), TypeScript, Tailwind CSS.
- Les données vivent dans Notion ; le site les lit côté serveur.
- Le jeton Notion est fourni uniquement par la variable d'environnement `NOTION_TOKEN`, réglée dans Vercel. Il ne doit jamais figurer dans le code.
