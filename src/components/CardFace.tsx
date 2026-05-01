import { useRef, useCallback, useState } from "preact/hooks";
import type { CardFaceData } from "../cards";

export type SwipeDirection = "left" | "right" | "up" | "down" | null;

interface Props {
  sides: CardFaceData[]; // All sides, 0-indexed
  currentSide: number; // Which side is shown
  isLastSide: boolean; // Is this the last side (rating available)?
  onNextSide: () => void; // Advance to next side
  onSwipeRate?: (direction: SwipeDirection) => void; // Rate on last side swipe
  onTapFlip?: () => void; // Tap to flip was replaced by onNextSide
}

const SWIPE_THRESHOLD = 80;

export function CardFace({ sides, currentSide, isLastSide, onNextSide, onSwipeRate }: Props) {
  const face = sides[currentSide] ?? { lines: ["..."] };
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [dragging, setDragging] = useState(false);
  const startRef = useRef({ x: 0, y: 0 });
  const totalSides = sides.length;

  const getDirection = useCallback((x: number, y: number): SwipeDirection => {
    if (Math.abs(x) > Math.abs(y)) return x > 0 ? "right" : "left";
    return y < 0 ? "up" : "down";
  }, []);

  const handleStart = useCallback((clientX: number, clientY: number) => {
    startRef.current = { x: clientX, y: clientY };
    setDragging(true);
  }, []);

  const handleMove = useCallback((clientX: number, clientY: number) => {
    if (!dragging) return;
    setOffset({ x: clientX - startRef.current.x, y: clientY - startRef.current.y });
  }, [dragging]);

  const handleEnd = useCallback(() => {
    if (!dragging) return;
    setDragging(false);

    const absX = Math.abs(offset.x);
    const absY = Math.abs(offset.y);
    const dir = getDirection(offset.x, offset.y);

    if (Math.max(absX, absY) > SWIPE_THRESHOLD) {
      if (isLastSide && onSwipeRate) {
        // On last side: swipe = rate
        setOffset({ x: offset.x * 3, y: offset.y * 3 });
        setTimeout(() => {
          setOffset({ x: 0, y: 0 });
          onSwipeRate(dir);
        }, 200);
      } else {
        // Not last side: swipe = advance
        setOffset({ x: offset.x * 3, y: offset.y * 3 });
        setTimeout(() => {
          setOffset({ x: 0, y: 0 });
          onNextSide();
        }, 200);
      }
    } else if (Math.max(absX, absY) > 10) {
      // Short swipe = tap = advance
      onNextSide();
      setOffset({ x: 0, y: 0 });
    } else {
      setOffset({ x: 0, y: 0 });
    }
  }, [dragging, offset, isLastSide, onSwipeRate, onNextSide, getDirection]);

  // Overlay during swipe on last side
  let overlayColor = "transparent";
  let overlayText = "";
  if (dragging && isLastSide) {
    const dir = getDirection(offset.x, offset.y);
    if (dir === "right") { overlayColor = `rgba(22,163,74,${Math.min(Math.abs(offset.x) / 200, 0.6)})`; overlayText = "Good"; }
    else if (dir === "left") { overlayColor = `rgba(220,38,38,${Math.min(Math.abs(offset.x) / 200, 0.6)})`; overlayText = "Again"; }
    else if (dir === "up") { overlayColor = `rgba(37,99,235,${Math.min(Math.abs(offset.y) / 200, 0.6)})`; overlayText = "Easy"; }
    else if (dir === "down") { overlayColor = `rgba(202,138,4,${Math.min(Math.abs(offset.y) / 200, 0.6)})`; overlayText = "Hard"; }
  }

  const transform = dragging
    ? `translate(${offset.x}px, ${offset.y}px) rotate(${offset.x * 0.05}deg)`
    : "none";

  return (
    <div
      onClick={dragging ? undefined : onNextSide}
      onTouchStart={(e) => {
        const t = e.touches[0];
        handleStart(t.clientX, t.clientY);
      }}
      onTouchMove={(e) => {
        const t = e.touches[0];
        handleMove(t.clientX, t.clientY);
      }}
      onTouchEnd={handleEnd}
      onMouseDown={(e) => handleStart(e.clientX, e.clientY)}
      onMouseMove={(e) => {
        if (dragging) { e.preventDefault(); handleMove(e.clientX, e.clientY); }
      }}
      onMouseUp={handleEnd}
      onMouseLeave={handleEnd}
      style={{
        minHeight: 220,
        padding: "32px 28px",
        background: "#fff",
        borderRadius: 16,
        boxShadow: dragging
          ? "0 8px 30px rgba(0,0,0,0.18)"
          : "0 2px 8px rgba(0,0,0,0.1)",
        border: "1px solid #e5e7eb",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        cursor: dragging ? "grabbing" : "pointer",
        userSelect: "none",
        transform,
        transition: dragging ? "none" : "transform 0.25s ease, box-shadow 0.2s",
        position: "relative",
        overflow: "hidden",
        touchAction: "none",
      }}
    >
      {/* Swipe overlay (only on last side) */}
      {isLastSide && dragging && overlayText && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: overlayColor,
            borderRadius: 16,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "1.2rem",
            fontWeight: 700,
            color: "#fff",
            pointerEvents: "none",
          }}
        >
          {overlayText}
        </div>
      )}

      {/* Side indicator */}
      <div
        style={{
          fontSize: "0.7rem",
          color: "#9ca3af",
          marginBottom: 12,
          textTransform: "uppercase",
          letterSpacing: 1,
        }}
      >
        {totalSides > 1 && `Side ${currentSide + 1} of ${totalSides} · `}
        {isLastSide
          ? "Swipe → Good · ← Again · ↑ Easy · ↓ Hard"
          : "Tap or swipe to continue"}
      </div>

      {/* Side dots */}
      {totalSides > 1 && (
        <div style={{ display: "flex", gap: 6, marginBottom: 16 }}>
          {sides.map((_, i) => (
            <div
              key={i}
              style={{
                width: 8,
                height: 8,
                borderRadius: "50%",
                background: i === currentSide ? "#2563eb" : "#d1d5db",
                transition: "background 0.2s",
              }}
            />
          ))}
        </div>
      )}

      {/* Content */}
      {face.lines.map((line, i) => (
        <div
          key={i}
          style={{
            fontSize: i === 0 ? "1.6rem" : "1rem",
            fontWeight: i === 0 ? 700 : 400,
            marginTop: i > 0 ? 8 : 0,
            color: i === 0 ? "#111" : "#4b5563",
            maxWidth: "100%",
            wordBreak: "break-word",
            pointerEvents: "none",
          }}
        >
          {line}
        </div>
      ))}
    </div>
  );
}
