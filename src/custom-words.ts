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

/** Strip punctuation, brackets, hyphens at edges, and normalize case/umlauts. */
function normalizeWord(s: string): string {
  return s
    .trim()
    .replace(/^[(\[]+|[)\]]+$/g, "")
    .replace(/^[-–]+|[-–]+$/g, "")
    .replace(/[.,!?;:"""()[\]]+$/g, "")
    .replace(/^[.,!?;:"""()[\]]+/, "")
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

// Common words (A1 pronouns, articles, prepositions, etc.) that aren't in the
// B1 vocabulary list but shouldn't be reported as "not found"
const SKIP_WORDS = new Set([
  "ich", "du", "er", "sie", "es", "wir", "ihr", "man",
  "mich", "dich", "sich", "uns", "euch",
  "mir", "dir", "ihm", "ihnen",
  "mein", "dein", "sein", "unser", "euer",
  "meine", "deine", "seine", "unsere", "eure", "ihre",
  "meinen", "deinen", "seinen", "unseren", "euren", "ihren",
  "meinem", "deinem", "seinem", "unserem", "eurem", "ihrem",
  "meiner", "deiner", "seiner", "unserer", "eurer", "ihrer",
  "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "einem", "einer",
  "dieser", "diese", "dieses", "diesen", "diesem",
  "jeder", "jede", "jedes", "jeden", "jedem",
  "welcher", "welche", "welches", "welchen", "welchem",
  "im", "am", "zum", "zur", "vom", "beim", "ins", "ans",
  "und", "oder", "aber", "denn", "weil", "dass", "wenn", "als", "ob",
  "da", "so", "zu", "von", "fur", "mit", "auf", "aus", "bei", "nach", "seit", "vor",
  "ist", "bin", "bist", "sind", "war", "hat", "habe", "hast", "haben", "wird",
  "kann", "muss", "will", "soll", "darf", "mag",
  "kannst", "musst", "willst", "sollst", "darfst",
  "nicht", "kein", "keine", "keinen", "keinem", "keiner",
  "auch", "noch", "schon", "nur", "sehr", "oft", "hier", "dort",
  "was", "wer", "wo", "wie", "wann", "warum",
  "ja", "nein", "doch",
]);

/** Match extracted words against the lookup map with fuzzy stem matching. */
export function matchWords(
  words: string[],
  lookup: Map<string, CardEntry>
): { matches: MatchResult[]; unmatched: NoMatch[] } {
  const matches: MatchResult[] = [];
  const unmatched: NoMatch[] = [];
  const seen = new Set<string>();

  for (const word of words) {
    const key = normalizeWord(word);
    if (!key || key.length < 2) continue;
    if (seen.has(key)) continue;
    seen.add(key);

    if (SKIP_WORDS.has(key)) continue;

    const entry = findMatch(key, lookup);
    if (entry) {
      matches.push({ entry });
    } else {
      unmatched.push({ word });
    }
  }

  return { matches, unmatched };
}

function findMatch(key: string, lookup: Map<string, CardEntry>): CardEntry | null {
  // 1. Exact match
  const exact = lookup.get(key);
  if (exact) return exact;

  // 2. Check if word matches any individual word within multi-word entries
  for (const [entryKey, entry] of lookup) {
    const entryWords = entryKey.split(/\s+/);
    if (entryWords.some((w) => w === key)) return entry;
  }

  // 3. Stem matching — strip common German suffixes and try again
  const stems = getStemVariants(key);
  for (const stem of stems) {
    const stemMatch = lookup.get(stem);
    if (stemMatch) return stemMatch;
  }

  // 4. Prefix match — the input word starts with a dictionary entry (inflected form)
  for (const [entryKey, entry] of lookup) {
    if (entryKey.length >= 3 && key.startsWith(entryKey) && key.length - entryKey.length <= 4) {
      return entry;
    }
  }

  // 5. Dictionary entry starts with input (user typed a stem shorter than the entry)
  for (const [entryKey, entry] of lookup) {
    if (key.length >= 4 && entryKey.startsWith(key) && entryKey.length - key.length <= 3) {
      return entry;
    }
  }

  return null;
}

function getStemVariants(word: string): string[] {
  const variants: string[] = [];
  const suffixes = ["st", "t", "e", "en", "er", "es", "em", "et", "est", "te", "ten", "ung", "nen"];
  for (const suffix of suffixes) {
    if (word.endsWith(suffix) && word.length - suffix.length >= 3) {
      variants.push(word.slice(0, -suffix.length));
    }
  }
  // Handle ge- prefix (past participle)
  if (word.startsWith("ge") && word.length > 4) {
    const stripped = word.slice(2);
    variants.push(stripped);
    for (const suffix of ["t", "en", "et"]) {
      if (stripped.endsWith(suffix) && stripped.length - suffix.length >= 3) {
        variants.push(stripped.slice(0, -suffix.length));
      }
    }
  }
  return variants;
}

/** Extract individual words from user text (whitespace, comma, or semicolon separated). */
export function extractWords(text: string): string[] {
  return text
    .split(/[\s,;]+/)
    .map((s) => s.trim())
    .map((s) => s.replace(/^[(\[]+|[)\]]+$/g, ""))
    .map((s) => s.replace(/[.,!?;:"""]+$/g, ""))
    .filter((s) => s.length >= 2)
    .filter((s) => !/^-+$/.test(s))
    .filter((s) => !/^\d+\.?$/.test(s));
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
