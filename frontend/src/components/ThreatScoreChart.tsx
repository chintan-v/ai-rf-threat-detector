import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

type ThreatScoreChartProps = {
  signals: any[];
};

function ThreatScoreChart({ signals }: ThreatScoreChartProps) {
  const data = [...signals]
    .reverse()
    .map((item, index) => ({
      observation: index + 1,
      score: item.threat?.threat_score ?? 0,
    }));

  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data}>
        <CartesianGrid
          strokeDasharray="3 3"
          stroke="#1d2936"
        />

        <XAxis
          dataKey="observation"
          tick={{ fill: "#687583", fontSize: 10 }}
          label={{
            value: "Observation",
            position: "insideBottom",
            offset: -5,
            fill: "#687583",
            fontSize: 10,
          }}
        />

        <YAxis
          domain={[0, 100]}
          tick={{ fill: "#687583", fontSize: 10 }}
          label={{
            value: "Threat Score",
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
          formatter={(value) => [
            `${Number(value).toFixed(1)}`,
            "Threat Score",
          ]}
        />

        <ReferenceLine
  y={75}
  stroke="#ff4d4d"
  strokeDasharray="6 4"
  label={{ value: "HIGH", position: "right" }}
/>

<ReferenceLine
  y={45}
  stroke="#f5c542"
  strokeDasharray="6 4"
  label={{ value: "MEDIUM", position: "right" }}
/>
        <Line
          type="monotone"
          dataKey="score"
          stroke="#22d3ee"
          strokeWidth={2}
          dot={false}
          isAnimationActive={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default ThreatScoreChart;