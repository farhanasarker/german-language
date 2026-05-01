/**
 * Loads deck data from pre-built JSON files inside public/data/.
 */

export interface CardEntry {
  id: string;
  word: string;
  article: string;
  plural: string;
  wordType: string;
  english: string;
  bangla: string;
  partizipII: string;
  auxiliary: string;
  exampleSentence: string;
  synonyms: string;
  antonyms: string;
  tags: string;
}

export interface DeckInfo {
  id: string;
  name: string;
  description: string;
  cardCount: number;
  category: string;
}

export interface DeckIndex {
  decks: DeckInfo[];
  generatedAt: string;
}

const DATA_BASE = import.meta.env.BASE_URL + "data/";

let cachedIndex: DeckIndex | null = null;

export async function loadDeckIndex(): Promise<DeckIndex> {
  if (cachedIndex) return cachedIndex;
  const res = await fetch(DATA_BASE + "index.json");
  if (!res.ok) throw new Error(`Failed to load deck index: ${res.status}`);
  cachedIndex = await res.json();
  return cachedIndex!;
}

export async function loadDeck(deckId: string): Promise<CardEntry[]> {
  const res = await fetch(`${DATA_BASE}${deckId}.json`);
  if (!res.ok) throw new Error(`Failed to load deck "${deckId}": ${res.status}`);
  return res.json();
}
