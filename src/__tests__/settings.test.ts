import { describe, it, expect } from "vitest";
import { renderSide, PRESETS, DEFAULT_SETTINGS, ALL_FIELDS, type CardSettings, type CardSideConfig } from "../cards";
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

describe("Settings validation", () => {
  it("DEFAULT_SETTINGS matches simple preset", () => {
    expect(DEFAULT_SETTINGS).toBe(PRESETS.simple);
  });

  it("all presets have at least 1 side", () => {
    for (const preset of Object.values(PRESETS)) {
      expect(preset.sides.length).toBeGreaterThanOrEqual(1);
    }
  });

  it("all presets have at least 1 field per side", () => {
    for (const preset of Object.values(PRESETS)) {
      for (const side of preset.sides) {
        expect(side.fields.length).toBeGreaterThan(0);
      }
    }
  });

  it("all preset sides produce non-empty rendered output", () => {
    const entry = makeEntry();
    for (const preset of Object.values(PRESETS)) {
      for (const side of preset.sides) {
        const result = renderSide(entry, side.fields);
        expect(result.lines.length).toBeGreaterThan(0);
      }
    }
  });

  it("all ALL_FIELDS keys are valid CardEntry keys", () => {
    const entry = makeEntry();
    for (const field of ALL_FIELDS) {
      expect(field.key in entry).toBe(true);
    }
  });

  it("all ALL_FIELDS keys produce output in renderSide when value exists", () => {
    const entry = makeEntry({
      partizipII: "abgeschrieben",
      auxiliary: "hat",
      synonyms: "der Schreibtisch",
      antonyms: "der Stuhl",
    });
    for (const field of ALL_FIELDS) {
      const result = renderSide(entry, [field.key]);
      if (field.key === "tags") continue; // tags is intentionally skipped
      expect(
        result.lines.length,
        `Field "${field.key}" should render at least 1 line`
      ).toBeGreaterThanOrEqual(1);
    }
  });

  it("tags field is rendered as empty (skipped)", () => {
    const entry = makeEntry({ tags: "Essen, Wohnen" });
    const result = renderSide(entry, ["tags"]);
    expect(result.lines).toEqual([]);
  });
});

describe("Custom settings scenarios", () => {
  it("renders all fields in a single side", () => {
    const entry = makeEntry({
      partizipII: "abgeschrieben",
      auxiliary: "hat",
      synonyms: "kopieren",
      antonyms: "original",
    });
    const allKeys = ALL_FIELDS.map((f) => f.key).filter((k) => k !== "tags");
    const result = renderSide(entry, allKeys);
    // Should have 11 fields rendered (all ALL_FIELDS except tags)
    expect(result.lines.length).toBe(11);
  });

  it("renders empty side with no fields as empty", () => {
    const result = renderSide(makeEntry(), []);
    expect(result.lines).toEqual([]);
  });

  it("renders word-only side", () => {
    const result = renderSide(makeEntry(), ["word"]);
    expect(result.lines).toEqual(["Tisch"]);
  });

  it("renders translation-only side", () => {
    const result = renderSide(makeEntry(), ["english", "bangla"]);
    expect(result.lines).toEqual(["table", "টেবিল"]);
  });

  it("custom 5-side settings each produce output", () => {
    const customSettings: CardSettings = {
      name: "Custom",
      sides: [
        { label: "Word", fields: ["word"] },
        { label: "Article", fields: ["article", "plural"] },
        { label: "Meaning", fields: ["english", "bangla"] },
        { label: "Grammar", fields: ["partizipII", "auxiliary", "wordType"] },
        { label: "Sentence", fields: ["exampleSentence", "synonyms", "antonyms"] },
      ],
    };
    const entry = makeEntry({
      partizipII: "abgeschrieben",
      auxiliary: "hat",
      synonyms: "kopieren",
      antonyms: "original",
    });
    for (const side of customSettings.sides) {
      const result = renderSide(entry, side.fields);
      expect(result.lines.length).toBeGreaterThan(0);
    }
  });

  it("handles verb entry with grammar preset", () => {
    const verbEntry = makeEntry({
      word: "abschreiben",
      article: "",
      plural: "",
      wordType: "verb",
      english: "to copy",
      partizipII: "abgeschrieben",
      auxiliary: "hat",
      exampleSentence: "Er hat die Hausaufgaben abgeschrieben.",
    });
    const grammarPreset = PRESETS.grammar;
    expect(grammarPreset.sides.length).toBe(4);

    const side1 = renderSide(verbEntry, grammarPreset.sides[0].fields);
    expect(side1.lines).toEqual(["abschreiben"]); // word only, no article since empty

    const side3 = renderSide(verbEntry, grammarPreset.sides[2].fields);
    expect(side3.lines).toContain("Partizip II: abgeschrieben");
    expect(side3.lines).toContain("Auxiliary: hat");
    expect(side3.lines).toContain("Type: verb");
  });

  it("renders empty article correctly (no parentheses shown)", () => {
    const entry = makeEntry({ article: "" });
    const result = renderSide(entry, ["article"]);
    expect(result.lines).toEqual([]); // empty article is skipped
  });

  it("preset names are unique", () => {
    const names = Object.values(PRESETS).map((p) => p.name);
    expect(new Set(names).size).toBe(names.length);
  });

  it("all presets are immutable copies of each other", () => {
    // Verify PRESETS objects don't share references
    const simple = PRESETS.simple;
    const deep = PRESETS.deep;
    expect(simple.sides).not.toBe(deep.sides);
    expect(simple.sides[0]).not.toBe(deep.sides[0]);
  });
});
