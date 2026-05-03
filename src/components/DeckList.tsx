import { useState } from "preact/hooks";
import type { DeckIndex, DeckInfo } from "../data";
import { getCustomDeckInfo } from "../custom-words";

interface Props {
  index: DeckIndex;
  onSelectDeck: (deckId: string) => void;
  onCustomDeck?: () => void;
}

export function DeckList({ index, onSelectDeck, onCustomDeck }: Props) {
  const customInfo = getCustomDeckInfo();
  const [filter, setFilter] = useState<string>("all");

  const categories = [...new Set(index.decks.map((d) => d.category))];
  const filtered =
    filter === "all" ? index.decks : index.decks.filter((d) => d.category === filter);

  return (
    <div>
      <div style={{ display: "flex", gap: 6, marginBottom: 20, flexWrap: "wrap" }}>
        <FilterChip label="All" active={filter === "all"} onClick={() => setFilter("all")} />
        {categories.map((cat) => (
          <FilterChip
            key={cat}
            label={cat}
            active={filter === cat}
            onClick={() => setFilter(cat)}
          />
        ))}
      </div>

      <div style={{ display: "grid", gap: 12 }}>
        {onCustomDeck && (
          <div
            onClick={onCustomDeck}
            style={{
              padding: "16px 20px",
              background: "#f0fdf4",
              borderRadius: 12,
              cursor: "pointer",
              boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
              border: "1px solid #bbf7d0",
              transition: "box-shadow 0.15s",
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.12)")
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.boxShadow = "0 1px 3px rgba(0,0,0,0.08)")
            }
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <h3 style={{ fontSize: "1rem", marginBottom: 2 }}>{customInfo.name} ✎</h3>
                <p style={{ fontSize: "0.8rem", color: "#6b7280" }}>
                  {customInfo.cardCount} cards · {customInfo.description}
                </p>
              </div>
              <span style={{ fontSize: "1.4rem", color: "#86efac" }}>→</span>
            </div>
          </div>
        )}
        {filtered.map((deck) => (
          <DeckCard key={deck.id} deck={deck} onClick={() => onSelectDeck(deck.id)} />
        ))}
      </div>
    </div>
  );
}

function FilterChip({
  label,
  active,
  onClick,
}: {
  label: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: "4px 14px",
        borderRadius: 20,
        fontSize: "0.85rem",
        fontWeight: 500,
        background: active ? "#2563eb" : "#e5e7eb",
        color: active ? "#fff" : "#374151",
      }}
    >
      {label}
    </button>
  );
}

function DeckCard({ deck, onClick }: { deck: DeckInfo; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      style={{
        padding: "16px 20px",
        background: "#fff",
        borderRadius: 12,
        cursor: "pointer",
        boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
        border: "1px solid #e5e7eb",
        transition: "box-shadow 0.15s",
      }}
      onMouseEnter={(e) =>
        (e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.12)")
      }
      onMouseLeave={(e) =>
        (e.currentTarget.style.boxShadow = "0 1px 3px rgba(0,0,0,0.08)")
      }
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h3 style={{ fontSize: "1rem", marginBottom: 2 }}>{deck.name}</h3>
          <p style={{ fontSize: "0.8rem", color: "#6b7280" }}>
            {deck.cardCount} cards · {deck.description}
          </p>
        </div>
        <span style={{ fontSize: "1.4rem", color: "#d1d5db" }}>→</span>
      </div>
    </div>
  );
}
