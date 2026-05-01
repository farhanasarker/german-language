/**
 * Multi-dimensional configurable flash card system.
 * Users choose how many sides and which fields appear on each side.
 */
import type { CardEntry } from "./data";

// All available data fields that can be shown on a card face
export interface FieldOption {
  key: keyof CardEntry;
  label: string;
  defaultOn: number[]; // Which preset sides include this by default
}

export const ALL_FIELDS: FieldOption[] = [
  { key: "word", label: "Word", defaultOn: [0] },
  { key: "article", label: "Article", defaultOn: [0] },
  { key: "plural", label: "Plural", defaultOn: [1] },
  { key: "english", label: "English", defaultOn: [1] },
  { key: "bangla", label: "Bangla", defaultOn: [1] },
  { key: "partizipII", label: "Partizip II", defaultOn: [2] },
  { key: "auxiliary", label: "Auxiliary (hat/sein)", defaultOn: [2] },
  { key: "exampleSentence", label: "Example Sentence", defaultOn: [1, 2] },
  { key: "synonyms", label: "Synonyms", defaultOn: [] },
  { key: "antonyms", label: "Antonyms", defaultOn: [] },
  { key: "wordType", label: "Word Type", defaultOn: [] },
];

export interface CardSideConfig {
  fields: (keyof CardEntry)[]; // Which fields to show
  label: string; // e.g. "Side 1", "Word", "Meaning"
}

export interface CardSettings {
  sides: CardSideConfig[];
  name: string; // Preset name
}

// ---- Presets ----

export const PRESETS: Record<string, CardSettings> = {
  simple: {
    name: "Simple (Word → Meaning)",
    sides: [
      { label: "Word", fields: ["word", "article"] },
      { label: "Meaning", fields: ["english", "bangla", "exampleSentence", "plural"] },
    ],
  },
  deep: {
    name: "Deep (Word → Meaning → Sentence)",
    sides: [
      { label: "Word", fields: ["word", "article"] },
      { label: "Meaning", fields: ["english", "bangla", "plural", "synonyms"] },
      { label: "Sentence", fields: ["exampleSentence"] },
    ],
  },
  grammar: {
    name: "Grammar (Word → Meaning → Grammar → Sentence)",
    sides: [
      { label: "Word", fields: ["word", "article"] },
      { label: "Meaning", fields: ["english", "bangla"] },
      { label: "Grammar", fields: ["partizipII", "auxiliary", "plural", "wordType"] },
      { label: "Sentence", fields: ["exampleSentence", "synonyms"] },
    ],
  },
  minimal: {
    name: "Minimal (Sentence → Word)",
    sides: [
      { label: "Cloze", fields: ["exampleSentence"] },
      { label: "Answer", fields: ["word", "article", "english", "bangla"] },
    ],
  },
};

export const DEFAULT_SETTINGS: CardSettings = PRESETS.simple;

// ---- Render a side ----

export interface CardFaceData {
  lines: string[];
}

export function renderSide(entry: CardEntry, fields: (keyof CardEntry)[]): CardFaceData {
  const lines: string[] = [];

  for (const field of fields) {
    const value = entry[field];
    if (!value || (typeof value === "string" && !value.trim())) continue;

    switch (field) {
      case "word":
        lines.push(entry.word);
        break;
      case "article":
        lines.push(`(${entry.article})`);
        break;
      case "plural":
        lines.push(`Plural: ${entry.plural}`);
        break;
      case "english":
        lines.push(entry.english);
        break;
      case "bangla":
        lines.push(entry.bangla);
        break;
      case "partizipII":
        lines.push(`Partizip II: ${entry.partizipII}`);
        break;
      case "auxiliary":
        lines.push(`Auxiliary: ${entry.auxiliary}`);
        break;
      case "exampleSentence":
        lines.push(`"${entry.exampleSentence}"`);
        break;
      case "synonyms":
        lines.push(`Syn: ${entry.synonyms}`);
        break;
      case "antonyms":
        lines.push(`Ant: ${entry.antonyms}`);
        break;
      case "wordType":
        lines.push(`Type: ${entry.wordType}`);
        break;
      case "tags":
        // Skip tags in card display
        break;
      default:
        break;
    }
  }

  return { lines };
}
