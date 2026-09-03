import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

type SpectrumChartProps = {
  frequency: number;
};

function SpectrumChart({ frequency }: SpectrumChartProps) {
  const data = Array.from({ length: 51 }, (_, index) => {
    const freq = 2400 + index * 2;

    const distance = Math.abs(freq - frequency);

    const signalStrength =
      -85 +
      Math.max(0, 55 - distance * 8) +
      Math.random() * 8;

    return {
      frequency: Number(freq.toFixed(1)),
      power: Number(signalStrength.toFixed(1)),
    };
  });

  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1d2936" />

        <XAxis
          dataKey="frequency"
          tick={{ fill: "#687583", fontSize: 10 }}
          tickFormatter={(value) => `${value}`}
        />

        <YAxis
          domain={[-90, -20]}
          tick={{ fill: "#687583", fontSize: 10 }}
          label={{
            value: "Power (dB)",
            angle: -90,
            position: "insideLeft",
            fill: "#687583",
            fontSize: 10,
          }}
        />

        <Tooltip
          contentStyle={{
            background: "#0d131b",
            border: "1px solid #1d2936",
            fontSize: "11px",
          }}
          labelFormatter={(value) => `${value} MHz`}
          formatter={(value) => [`${value} dB`, "Power"]}
        />

        <Line
          type="monotone"
          dataKey="power"
          stroke="#22d3ee"
          strokeWidth={2}
          dot={false}
          isAnimationActive={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default SpectrumChart;