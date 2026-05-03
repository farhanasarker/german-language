/**
 * Custom words — user pastes words (comma/space/newline separated),
 * we match them against the full dictionary (all.json) in-memory.
 */
import type { CardEntry } from "./data";

const ALL_URL = import.meta.env.BASE_URL + "data/all.json";
const DECK_ID = "deck-custom";

let cachedEntries: CardEntry[] | null = null;
let lookupMap: Map<string, CardEntry> | null = null;

export async function loadAllEntries(): Promise<CardEntry[]> {
  if (cachedEntries) return cachedEntries;
  const res = await fetch(ALL_URL);
  if (!res.ok) throw new Error(`Failed to load dictionary: ${res.status}`);
  cachedEntries = await res.json();
  return cachedEntries!;
}

export function getLookupMap(): Map<string, CardEntry> {
  if (!cachedEntries) throw new Error("Entries not loaded");
  if (lookupMap) return lookupMap;
  lookupMap = new Map();
  for (const e of cachedEntries) {
    lookupMap.set(normalizeWord(e.word), e);
  }
  return lookupMap;
}

/** Case-insensitive, umlaut-normalized key. */
function normalizeWord(s: string): string {
  return s
    .trim()
    .toLowerCase()
    .replace(/ä/g, "a").replace(/ö/g, "o").replace(/ü/g, "u")
    .replace(/ß/g, "ss");
}

export interface MatchResult {
  entry: CardEntry;
}

export interface NoMatch {
  word: string;
}

/** Match extracted words against the lookup map. */
export function matchWords(
  words: string[],
  lookup: Map<string, CardEntry>
): { matches: MatchResult[]; unmatched: NoMatch[] } {
  const matches: MatchResult[] = [];
  const unmatched: NoMatch[] = [];

  for (const word of words) {
    const key = normalizeWord(word);
    if (!key) continue;

    // Exact match
    const exact = lookup.get(key);
    if (exact) {
      matches.push({ entry: exact });
      continue;
    }

    // Check if word matches any individual word within multi-word entries
    // (e.g. "waschen" matches "sich waschen")
    let found = false;
    for (const [entryKey, entry] of lookup) {
      const entryWords = entryKey.split(/\s+/);
      if (entryWords.some((w) => w === key)) {
        matches.push({ entry });
        found = true;
        break;
      }
    }

    if (!found) {
      unmatched.push({ word });
    }
  }

  return { matches, unmatched };
}

/** Extract individual words from user text (whitespace, comma, or semicolon separated). */
export function extractWords(text: string): string[] {
  return text
    .split(/[\s,;]+/)
    .map((s) => s.trim())
    .filter((s) => s.length > 0);
}

// Persist text across page navigation within the session
let savedText = "";

export function getCustomText(): string {
  return savedText;
}

export function setCustomText(text: string): void {
  savedText = text;
}

export function getCustomDeckId(): string {
  return DECK_ID;
}

export function getCustomDeckInfo(): {
  id: string;
  name: string;
  description: string;
  cardCount: number;
  category: string;
} {
  return {
    id: DECK_ID,
    name: "Custom Words",
    description: "Paste words, match against dictionary",
    cardCount: 0,
    category: "Custom",
  };
}
