import { useState, useEffect } from "preact/hooks";
import type { CardEntry } from "../data";
import { loadDeck } from "../data";

interface Props {
  deckId: string;
  deckName: string;
  onClose: () => void;
}

type SortKey = "word" | "article" | "wordType" | "english" | "bangla";
type SortDir = "asc" | "desc";

export function WordList({ deckId, deckName, onClose }: Props) {
  const [entries, setEntries] = useState<CardEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [sortKey, setSortKey] = useState<SortKey>("word");
  const [sortDir, setSortDir] = useState<SortDir>("asc");

  useEffect(() => {
    loadDeck(deckId)
      .then(setEntries)
      .finally(() => setLoading(false));
  }, [deckId]);

  const handleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortDir(sortDir === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setSortDir("asc");
    }
  };

  const filtered = entries.filter((e) => {
    if (!search) return true;
    const q = search.toLowerCase();
    return (
      e.word.toLowerCase().includes(q) ||
      e.english.toLowerCase().includes(q) ||
      e.bangla.includes(q)
    );
  });

  const sorted = [...filtered].sort((a, b) => {
    const av = (a[sortKey] || "").toLowerCase();
    const bv = (b[sortKey] || "").toLowerCase();
    const cmp = av.localeCompare(bv, "de");
    return sortDir === "asc" ? cmp : -cmp;
  });

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: 40 }}>
        <p>Loading words...</p>
      </div>
    );
  }

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <div>
          <h2 style={{ fontSize: "1.1rem" }}>{deckName}</h2>
          <span style={{ fontSize: "0.8rem", color: "#6b7280" }}>{filtered.length} words</span>
        </div>
        <button class="secondary" onClick={onClose} style={{ padding: "6px 14px", fontSize: "0.85rem" }}>
          Back
        </button>
      </div>

      <input
        type="text"
        placeholder="Search words..."
        value={search}
        onInput={(e) => setSearch((e.target as HTMLInputElement).value)}
        style={{
          width: "100%",
          padding: "10px 14px",
          borderRadius: 8,
          border: "1px solid #e5e7eb",
          fontSize: "0.9rem",
          marginBottom: 16,
          fontFamily: "inherit",
        }}
      />

      <div style={{ overflowX: "auto", borderRadius: 12, border: "1px solid #e5e7eb" }}>
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            fontSize: "0.85rem",
            background: "#fff",
          }}
        >
          <thead>
            <tr style={{ background: "#f9fafb", borderBottom: "2px solid #e5e7eb" }}>
              <SortHeader label="Word" field="word" current={sortKey} dir={sortDir} onClick={handleSort} />
              <SortHeader label="Article" field="article" current={sortKey} dir={sortDir} onClick={handleSort} />
              <SortHeader label="Type" field="wordType" current={sortKey} dir={sortDir} onClick={handleSort} />
              <SortHeader label="English" field="english" current={sortKey} dir={sortDir} onClick={handleSort} />
              <SortHeader label="Bangla" field="bangla" current={sortKey} dir={sortDir} onClick={handleSort} />
              <th style={{ padding: "10px 12px", textAlign: "left", fontWeight: 600, color: "#374151" }}>Plural</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((entry) => (
              <tr key={entry.id} style={{ borderBottom: "1px solid #f3f4f6" }}>
                <td style={{ padding: "10px 12px", fontWeight: 600 }}>{entry.word}</td>
                <td style={{ padding: "10px 12px", color: "#6b7280" }}>{entry.article}</td>
                <td style={{ padding: "10px 12px", color: "#6b7280" }}>{entry.wordType}</td>
                <td style={{ padding: "10px 12px" }}>{entry.english}</td>
                <td style={{ padding: "10px 12px" }}>{entry.bangla}</td>
                <td style={{ padding: "10px 12px", color: "#6b7280" }}>{entry.plural}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {sorted.length === 0 && (
        <div style={{ textAlign: "center", padding: 40, color: "#6b7280" }}>
          No words match your search.
        </div>
      )}
    </div>
  );
}

function SortHeader({
  label,
  field,
  current,
  dir,
  onClick,
}: {
  label: string;
  field: SortKey;
  current: SortKey;
  dir: SortDir;
  onClick: (key: SortKey) => void;
}) {
  const active = current === field;
  const arrow = active ? (dir === "asc" ? " ↑" : " ↓") : "";
  return (
    <th
      onClick={() => onClick(field)}
      style={{
        padding: "10px 12px",
        textAlign: "left",
        fontWeight: 600,
        color: active ? "#2563eb" : "#374151",
        cursor: "pointer",
        userSelect: "none",
        whiteSpace: "nowrap",
      }}
    >
      {label}{arrow}
    </th>
  );
}
