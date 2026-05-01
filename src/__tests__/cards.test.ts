import { describe, it, expect } from "vitest";
import { renderSide, PRESETS, DEFAULT_SETTINGS, ALL_FIELDS, type CardFaceData } from "../cards";
import type { CardEntry } from "../data";

function makeEntry(overrides: Partial<CardEntry> = {}): CardEntry {
  return {
    id: "test-001",
    word: "Tisch",
    article: "der",
    plural: "-e",
    wordType: "noun",
    english: "table",
    bangla: "টেবিল",
    partizipII: "",
    auxiliary: "",
    exampleSentence: "Der Tisch ist aus Holz.",
    synonyms: "",
    antonyms: "",
    tags: "Wohnen",
    ...overrides,
  };
}

function makeVerbEntry(): CardEntry {
  return {
    id: "test-002",
    word: "abschreiben",
    article: "",
    plural: "",
    wordType: "verb",
    english: "to copy (from someone)",
    bangla: "নকল করা",
    partizipII: "abgeschrieben",
    auxiliary: "hat",
    exampleSentence: "Er hat die Hausaufgaben von mir abgeschrieben.",
    synonyms: "",
    antonyms: "",
    tags: "Bildung",
  };
}

describe("renderSide", () => {
  it("renders word and article on one side", () => {
    const entry = makeEntry();
    const result = renderSide(entry, ["word", "article"]);
    expect(result.lines).toEqual(["Tisch", "(der)"]);
  });

  it("renders english and bangla", () => {
    const entry = makeEntry();
    const result = renderSide(entry, ["english", "bangla"]);
    expect(result.lines).toEqual(["table", "টেবিল"]);
  });

  it("renders example sentence with quotes", () => {
    const entry = makeEntry();
    const result = renderSide(entry, ["exampleSentence"]);
    expect(result.lines).toEqual(['"Der Tisch ist aus Holz."']);
  });

  it("renders plural with label", () => {
    const entry = makeEntry();
    const result = renderSide(entry, ["plural"]);
    expect(result.lines).toEqual(["Plural: -e"]);
  });

  it("renders partizip II with label", () => {
    const entry = makeVerbEntry();
    const result = renderSide(entry, ["partizipII", "auxiliary"]);
    expect(result.lines).toEqual(["Partizip II: abgeschrieben", "Auxiliary: hat"]);
  });

  it("skips empty fields", () => {
    const entry = makeEntry({ synonyms: "", antonyms: "" });
    const result = renderSide(entry, ["synonyms", "antonyms", "word"]);
    expect(result.lines).toEqual(["Tisch"]);
  });

  it("skips null/undefined values", () => {
    const entry = makeEntry();
    const result = renderSide(entry, ["partizipII"]); // noun has no partizip
    expect(result.lines).toEqual([]);
  });

  it("renders word type", () => {
    const entry = makeEntry();
    const result = renderSide(entry, ["wordType"]);
    expect(result.lines).toEqual(["Type: noun"]);
  });

  it("skips tags field", () => {
    const entry = makeEntry({ tags: "Wohnen, Essen" });
    const result = renderSide(entry, ["tags"]);
    expect(result.lines).toEqual([]);
  });

  it("renders synonyms and antonyms with labels", () => {
    const entry = makeEntry({ synonyms: "der Schreibtisch", antonyms: "der Stuhl" });
    const result = renderSide(entry, ["synonyms", "antonyms"]);
    expect(result.lines).toEqual(["Syn: der Schreibtisch", "Ant: der Stuhl"]);
  });

  it("renders all fields together in order", () => {
    const entry = makeEntry();
    const result = renderSide(entry, ["word", "article", "plural", "english"]);
    expect(result.lines).toEqual(["Tisch", "(der)", "Plural: -e", "table"]);
  });
});

describe("PRESETS", () => {
  it("simple preset has 2 sides", () => {
    expect(PRESETS.simple.sides).toHaveLength(2);
  });

  it("deep preset has 3 sides", () => {
    expect(PRESETS.deep.sides).toHaveLength(3);
  });

  it("grammar preset has 4 sides", () => {
    expect(PRESETS.grammar.sides).toHaveLength(4);
  });

  it("minimal preset has 2 sides", () => {
    expect(PRESETS.minimal.sides).toHaveLength(2);
  });

  it("each side in presets uses known fields", () => {
    const knownFields = ALL_FIELDS.map((f) => f.key);
    for (const preset of Object.values(PRESETS)) {
      for (const side of preset.sides) {
        for (const field of side.fields) {
          expect(knownFields).toContain(field);
        }
      }
    }
  });

  it("DEFAULT_SETTINGS is simple preset", () => {
    expect(DEFAULT_SETTINGS).toBe(PRESETS.simple);
  });
});

describe("ALL_FIELDS", () => {
  it("includes all required fields", () => {
    const keys = ALL_FIELDS.map((f) => f.key);
    expect(keys).toContain("word");
    expect(keys).toContain("article");
    expect(keys).toContain("english");
    expect(keys).toContain("bangla");
    expect(keys).toContain("partizipII");
    expect(keys).toContain("auxiliary");
    expect(keys).toContain("exampleSentence");
    expect(keys).toContain("plural");
  });
});
