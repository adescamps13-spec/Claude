import "server-only";
import { Client } from "@notionhq/client";

/**
 * Identifiants des sources de données Notion (voir BRIEF.md, partie 5).
 * Avec le SDK Notion v5 (API 2025-09-03), on interroge une « source de données »
 * via notion.dataSources.query, et non plus la base elle-même.
 */
export const DATA_SOURCES = {
  demandes: "98ac7b49-0f6d-46a7-b637-45421d4cd4a3",
  ressources: "d38c2525-8089-4b52-9c6e-ebc1cb8e8d11",
  assets: "31f73a1a-5d72-45a2-ae34-1e648ac11747",
} as const;

/** Erreur levée quand la variable NOTION_TOKEN est absente. */
export class JetonManquantError extends Error {
  constructor() {
    super("La variable d'environnement NOTION_TOKEN est absente.");
    this.name = "JetonManquantError";
  }
}

/**
 * Crée le client Notion. Le jeton est lu uniquement ici, côté serveur,
 * et n'est jamais renvoyé ni affiché.
 */
export function getNotion(): Client {
  const token = process.env.NOTION_TOKEN?.trim();
  if (!token) throw new JetonManquantError();
  return new Client({ auth: token });
}
