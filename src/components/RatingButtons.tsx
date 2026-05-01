import type { Rating } from "../srs";

interface Props {
  onRate: (rating: Rating) => void;
}

export function RatingButtons({ onRate }: Props) {
  return (
    <div style={{ marginTop: 20 }}>
      {/* Primary: Again / Good — large, side by side */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 10 }}>
        <button
          onClick={() => onRate(1)}
          style={{
            padding: "16px 12px",
            borderRadius: 12,
            background: "#fef2f2",
            color: "#dc2626",
            border: "2px solid #fecaca",
            fontSize: "1rem",
            fontWeight: 700,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 2,
          }}
        >
          <span style={{ fontSize: "1.3rem" }}>↶</span>
          <span>Again</span>
          <span style={{ fontSize: "0.7rem", fontWeight: 400, opacity: 0.7 }}>key 1</span>
        </button>
        <button
          onClick={() => onRate(4)}
          style={{
            padding: "16px 12px",
            borderRadius: 12,
            background: "#f0fdf4",
            color: "#16a34a",
            border: "2px solid #bbf7d0",
            fontSize: "1rem",
            fontWeight: 700,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 2,
          }}
        >
          <span style={{ fontSize: "1.3rem" }}>✓</span>
          <span>Good</span>
          <span style={{ fontSize: "0.7rem", fontWeight: 400, opacity: 0.7 }}>key 4 / Space</span>
        </button>
      </div>

      {/* Secondary: Hard / Easy */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 8 }}>
        <button
          onClick={() => onRate(0)}
          style={{
            padding: "10px 6px",
            borderRadius: 10,
            background: "#f9fafb",
            color: "#6b7280",
            border: "1px solid #e5e7eb",
            fontSize: "0.8rem",
            fontWeight: 600,
          }}
        >
          Blackout
          <span style={{ display: "block", fontSize: "0.65rem", fontWeight: 400, opacity: 0.6 }}>key 0</span>
        </button>
        <button
          onClick={() => onRate(3)}
          style={{
            padding: "10px 6px",
            borderRadius: 10,
            background: "#fefce8",
            color: "#a16207",
            border: "1px solid #fef08a",
            fontSize: "0.8rem",
            fontWeight: 600,
          }}
        >
          Hard
          <span style={{ display: "block", fontSize: "0.65rem", fontWeight: 400, opacity: 0.6 }}>key 3</span>
        </button>
        <button
          onClick={() => onRate(5)}
          style={{
            padding: "10px 6px",
            borderRadius: 10,
            background: "#eff6ff",
            color: "#2563eb",
            border: "1px solid #bfdbfe",
            fontSize: "0.8rem",
            fontWeight: 600,
          }}
        >
          Easy
          <span style={{ display: "block", fontSize: "0.65rem", fontWeight: 400, opacity: 0.6 }}>key 5</span>
        </button>
      </div>
    </div>
  );
}
