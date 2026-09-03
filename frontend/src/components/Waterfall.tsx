import { useEffect, useState } from "react";

function Waterfall({
  frequency,
  power,
}: {
  frequency: number;
  power: number;
}) {
  const [rows, setRows] = useState<number[][]>([]);

  useEffect(() => {
    const interval = setInterval(() => {
      const newRow = Array.from({ length: 80 }, (_, index) => {
        const cellFrequency = 2400 + (index / 79) * 100;
        const distance = Math.abs(cellFrequency - frequency);

        const signalStrength =
        Math.max(0, 1 - distance / 8) * 0.9 +
        Math.random() * 0.15;

        return Math.min(1, signalStrength);
    });

      setRows((previousRows) => {
        const updatedRows = [...previousRows, newRow];

        if (updatedRows.length > 20) {
          updatedRows.shift();
        }

        return updatedRows;
      });
    }, 300);

    return () => clearInterval(interval);
  }, [frequency]);

  return (
  <div className="waterfall-wrapper">
    <div className="waterfall-time-label">TIME ↓</div>
    <div className="waterfall-container">
      {rows.map((row, rowIndex) => (
        <div className="waterfall-row" key={rowIndex}>
          {row.map((value, index) => (
            <div
              className="waterfall-cell"
              key={index}
              style={{
                opacity: 0.15 + value * 0.85,
                backgroundColor: "#22d3ee",
              }}
            />
          ))}
        </div>
      ))}
    </div>

    <div className="waterfall-axis">
      <span>2400</span>
      <span>2420</span>
      <span>2440</span>
      <span>2460</span>
      <span>2480</span>
      <span>2500 MHz</span>
    </div>
  </div>
);
}

export default Waterfall;