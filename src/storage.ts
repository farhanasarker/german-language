import Dexie, { type Table } from "dexie";
import type { SRSCard } from "./srs";
import type { CardSettings } from "./cards";
import { DEFAULT_SETTINGS } from "./cards";

export interface DeckProgress {
  deckId: string;
  cardsStudied: number;
  cardsMastered: number;
  lastStudied: number; // timestamp
}

export interface StoredSettings {
  id: string; // "cardSettings"
  settings: CardSettings;
}

class GermanFlashcardDB extends Dexie {
  srsCards!: Table<SRSCard, string>;
  deckProgress!: Table<DeckProgress, string>;
  settings!: Table<StoredSettings, string>;

  constructor() {
    super("GermanFlashcards");
    this.version(1).stores({
      srsCards: "cardId, nextReview",
      deckProgress: "deckId",
    });
    this.version(2).stores({
      srsCards: "cardId, nextReview",
      deckProgress: "deckId",
      settings: "id",
    });
  }
}

export const db = new GermanFlashcardDB();

// ---- SRS Card Operations ----

export async function getCardState(cardId: string): Promise<SRSCard | undefined> {
  return db.srsCards.get(cardId);
}

export async function saveCardState(card: SRSCard): Promise<void> {
  await db.srsCards.put(card);
}

export async function getDueCardIds(deckCardIds: string[]): Promise<string[]> {
  const now = Date.now();
  const cards = await db.srsCards
    .where("cardId")
    .anyOf(deckCardIds)
    .and((c) => c.nextReview <= now)
    .toArray();
  return cards.sort((a, b) => a.nextReview - b.nextReview).map((c) => c.cardId);
}

export async function countDueCards(deckCardIds: string[]): Promise<number> {
  const now = Date.now();
  return db.srsCards
    .where("cardId")
    .anyOf(deckCardIds)
    .and((c) => c.nextReview <= now)
    .count();
}

export async function countStudiedCards(deckCardIds: string[]): Promise<number> {
  return db.srsCards
    .where("cardId")
    .anyOf(deckCardIds)
    .and((c) => c.repetitions > 0)
    .count();
}

// ---- Deck Progress Operations ----

export async function getDeckProgress(deckId: string): Promise<DeckProgress | undefined> {
  return db.deckProgress.get(deckId);
}

export async function saveDeckProgress(progress: DeckProgress): Promise<void> {
  await db.deckProgress.put(progress);
}

// ---- Export / Import ----

export async function exportAllProgress(): Promise<string> {
  const [srsCards, deckProgress] = await Promise.all([
    db.srsCards.toArray(),
    db.deckProgress.toArray(),
  ]);
  return JSON.stringify({ srsCards, deckProgress, exportedAt: Date.now() }, null, 2);
}

export async function importProgress(json: string): Promise<void> {
  const data = JSON.parse(json);
  if (data.srsCards) {
    await db.srsCards.bulkPut(data.srsCards);
  }
  if (data.deckProgress) {
    await db.deckProgress.bulkPut(data.deckProgress);
  }
}

export async function clearAllProgress(): Promise<void> {
  await db.srsCards.clear();
  await db.deckProgress.clear();
}

// ---- Card Settings ----

export async function getCardSettings(): Promise<CardSettings> {
  const stored = await db.settings.get("cardSettings");
  return stored?.settings ?? DEFAULT_SETTINGS;
}

export async function saveCardSettings(settings: CardSettings): Promise<void> {
  await db.settings.put({ id: "cardSettings", settings });
}
