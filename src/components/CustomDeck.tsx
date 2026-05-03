import { useState, useEffect } from "preact/hooks";
import { loadAllEntries, getLookupMap, matchWords, extractWords } from "../custom-words";
import type { CardEntry } from "../data";
import type { MatchResult, NoMatch } from "../custom-words";

interface Props {
  onStartStudy: (entries: CardEntry[]) => void;
}

export function CustomDeck({ onStartStudy }: Props) {
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [text, setText] = useState("");
  const [results, setResults] = useState<{
    matches: MatchResult[];
    unmatched: NoMatch[];
  } | null>(null);
  const [searchError, setSearchError] = useState<string | null>(null);

  useEffect(() => {
    loadAllEntries()
      .then(() => setLoading(false))
      .catch((e) => {
        setLoadError(e.message ?? "Failed to load dictionary");
        setLoading(false);
      });
  }, []);

  const handleFind = () => {
    setSearchError(null);
    const words = extractWords(text);
    if (words.length === 0) {
      setSearchError("Enter at least one word.");
      return;
    }
    try {
      const lookup = getLookupMap();
      setResults(matchWords(words, lookup));
    } catch (e: any) {
      setSearchError(e.message ?? "Failed to match words");
    }
  };

  const handleStudy = () => {
    if (results && results.matches.length > 0) {
      // Deduplicate by ID in case partial matching returns same entry for different words
      const seen = new Set<string>();
      const entries: CardEntry[] = [];
      for (const m of results.matches) {
        if (!seen.has(m.entry.id)) {
          seen.add(m.entry.id);
          entries.push(m.entry);
        }
      }
      onStartStudy(entries);
    }
  };

  if (loading) {
    return <p style={{ textAlign: "center", padding: 40, color: "#6b7280" }}>Loading dictionary…</p>;
  }

  if (loadError) {
    return (
      <div style={{ textAlign: "center", padding: 40 }}>
        <p style={{ color: "#dc2626" }}>{loadError}</p>
      </div>
    );
  }

  return (
    <div>
      <p style={{ color: "#6b7280", marginBottom: 12, fontSize: "0.9rem" }}>
        Paste words separated by commas, semicolons, or newlines. We'll find matching
        entries from the dictionary.
      </p>

      <textarea
        value={text}
        onInput={(e) => {
          setText((e.target as HTMLTextAreaElement).value);
          setResults(null);
          setSearchError(null);
        }}
        placeholder={`Haus, gehen, Apfel
Zahn
sich waschen`}
        rows={8}
        style={{
          width: "100%",
          padding: 12,
          borderRadius: 8,
          border: "1px solid #d1d5db",
          fontSize: "0.95rem",
          fontFamily: "monospace",
          resize: "vertical",
          boxSizing: "border-box",
        }}
      />

      {searchError && (
        <p style={{ color: "#dc2626", marginTop: 8, fontSize: "0.85rem" }}>{searchError}</p>
      )}

      <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
        <button class="primary" onClick={handleFind} style={{ fontSize: "0.95rem" }}>
          Find Words
        </button>
      </div>

      {results && (
        <div style={{ marginTop: 20 }}>
          {results.matches.length > 0 && (
            <div style={{ marginBottom: 16 }}>
              <div
                style={{
                  padding: "12px 16px",
                  background: "#f0fdf4",
                  borderRadius: 8,
                  border: "1px solid #bbf7d0",
                  marginBottom: 12,
                }}
              >
                <strong>{results.matches.length}</strong> word
                {results.matches.length !== 1 ? "s" : ""} matched
              </div>

              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.85rem" }}>
                <thead>
                  <tr style={{ borderBottom: "2px solid #e5e7eb", textAlign: "left" }}>
                    <th style={{ padding: "6px 8px" }}>Word</th>
                    <th style={{ padding: "6px 8px" }}>Article</th>
                    <th style={{ padding: "6px 8px" }}>English</th>
                    <th style={{ padding: "6px 8px" }}>Bangla</th>
                    <th style={{ padding: "6px 8px" }}>Type</th>
                  </tr>
                </thead>
                <tbody>
                  {results.matches.slice(0, 20).map((m) => (
                    <tr key={m.entry.id} style={{ borderBottom: "1px solid #f3f4f6" }}>
                      <td style={{ padding: "5px 8px", fontWeight: 500 }}>{m.entry.word}</td>
                      <td style={{ padding: "5px 8px", color: "#6b7280" }}>{m.entry.article}</td>
                      <td style={{ padding: "5px 8px" }}>{m.entry.english}</td>
                      <td style={{ padding: "5px 8px" }}>{m.entry.bangla}</td>
                      <td style={{ padding: "5px 8px", color: "#6b7280", fontSize: "0.8rem" }}>
                        {m.entry.wordType}
                      </td>
                    </tr>
                  ))}
                  {results.matches.length > 20 && (
                    <tr>
                      <td colSpan={5} style={{ padding: "8px", textAlign: "center", color: "#9ca3af", fontSize: "0.8rem" }}>
                        … and {results.matches.length - 20} more
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}

          {results.unmatched.length > 0 && (
            <div
              style={{
                padding: "12px 16px",
                background: "#fef2f2",
                borderRadius: 8,
                border: "1px solid #fecaca",
                marginBottom: 12,
              }}
            >
              <strong style={{ color: "#dc2626" }}>{results.unmatched.length}</strong> word
              {results.unmatched.length !== 1 ? "s" : ""} not found:{" "}
              <span style={{ color: "#6b7280" }}>
                {results.unmatched.map((u) => u.word).join(", ")}
              </span>
            </div>
          )}

          {results.matches.length > 0 && (
            <button class="primary" onClick={handleStudy} style={{ fontSize: "0.95rem" }}>
              Study These Words
            </button>
          )}
        </div>
      )}
    </div>
  );
}
