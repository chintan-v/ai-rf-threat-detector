import "./App.css";
import { useEffect, useState } from "react";
import { getSignal } from "./api";
import SpectrumChart from "./components/SpectrumChart";
import ThreatScoreChart from "./components/ThreatScoreChart";
import Waterfall from "./components/Waterfall";

function App() {
    const [signalData, setSignalData] = useState<any>(null);
    const [detectedSignals, setDetectedSignals] = useState<any[]>([]);
    const [alerts, setAlerts] = useState<any[]>([]);
    const [signalsDetected, setSignalsDetected] = useState(0);
    const [highPriorityCount, setHighPriorityCount] = useState(0);

    const [systemStatus, setSystemStatus] = useState("ONLINE");
    const [isMonitoring, setIsMonitoring] = useState(true);

  useEffect(() => {
  const fetchSignal = () => {
    if (!isMonitoring) return;
    getSignal()
      .then((data) => {
        console.log("Backend response:", data);

        setSignalData(data);

        setDetectedSignals((prev) => [
          data,
         ...prev,
        ].slice(0, 10));

        if (data.alert?.alert) {
          setAlerts((prev) => [
            data,
              ...prev,
          ].slice(0, 5));
        }

        setSignalsDetected((count) => count + 1);

        if (data.threat?.priority === "HIGH") {
          setHighPriorityCount((count) => count + 1);
        }
      })
      .catch((error) => {
        console.error("Backend connection failed:", error);
      });
  };

  fetchSignal();

  const interval = setInterval(fetchSignal, 2000);

  return () => clearInterval(interval);
}, [isMonitoring]);

  const signal = signalData?.signal;
  const classification = signalData?.classification;
  const threat = signalData?.threat;
  const prediction = signalData?.prediction;

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div>
          <h1>AI RF MONITORING SYSTEM</h1>
          <p>Adaptive Spectrum Intelligence Dashboard</p>
        </div>

        <div className="system-controls">
  <button
  className="control-btn activate-btn"
  onClick={() => {
    setSystemStatus("ONLINE");
    setIsMonitoring(true);
  }}
>
  ACTIVATE
</button>

<button
  className="control-btn pause-btn"
  onClick={() => {
    setSystemStatus("PAUSED");
    setIsMonitoring(false);
  }}
>
  PAUSE
</button>

<button
  className="control-btn terminate-btn"
  onClick={() => {
  setSystemStatus("TERMINATED");
  setIsMonitoring(false);

  setSignalData(null);
  setSignalsDetected(0);
  setHighPriorityCount(0);
  setDetectedSignals([]);
  setAlerts([]);
}}
>
  TERMINATE
</button>

  <div className="system-status">
  <span className="status-dot"></span>
  SYSTEM {systemStatus}
</div>
</div>    
      </header>

      {/* Main Dashboard */}
      <main className="dashboard">

        {/* Top Statistics */}
        <section className="stats-grid">

          <div className="stat-card">
            <span className="stat-label">SIGNALS DETECTED</span>
            <strong>{signalsDetected}</strong>
            <small>Live observations</small>
          </div>

          <div className="stat-card">
            <span className="stat-label">HIGH PRIORITY</span>
            <strong>{highPriorityCount}</strong>
            <small>Requires attention</small>
          </div>

          <div className="stat-card">
            <span className="stat-label">AI ACCURACY</span>
            <strong>99.5%</strong>
            <small>Classifier confidence</small>
          </div>

          <div className="stat-card">
            <span className="stat-label">CURRENT FREQUENCY</span>
            <strong>{signal?.frequency_mhz?.toFixed(1) ?? "--"}</strong>
            <small>MHz</small>
          </div>

        </section>

        {/* Main Content */}
        <section className="main-grid">

          {/* Spectrum */}
          <div className="panel spectrum-panel">
            <div className="panel-header">
              <div>
                <h2>LIVE SPECTRUM</h2>
                <p>Simulated RF activity</p>
              </div>

              <span className="live-badge">● LIVE</span>
            </div>

            <div className="spectrum-placeholder">
              {signal?.frequency_mhz != null && (
                <SpectrumChart frequency={signal.frequency_mhz} />
              )}
            </div>

            <div className="waterfall-section">
               <h3>LIVE WATERFALL</h3>
              <Waterfall
                frequency={signal?.frequency_mhz ?? 2450}
                power={signal?.power_db ?? -80}
              />
          </div>
          <div className="threat-chart-section">
  <div className="panel-header">
    <div>
      <h2>THREAT SCORE TIMELINE</h2>
      <p>AI priority score across recent observations</p>
    </div>
  </div>

  <div className="threat-chart-container">
    <ThreatScoreChart signals={detectedSignals} />
  </div>
</div>
          </div>

          {/* Threat Status */}
          <div className="panel threat-panel">
            <div className="panel-header">
              <div>
                <h2>THREAT STATUS</h2>
                <p>Current observation</p>
              </div>
            </div>

            <div className="threat-score">
              <strong>{threat?.threat_score?.toFixed(0) ?? "--"}</strong>
              <span>/ 100</span>
            </div>

            <div className="threat-level">
              {threat?.priority ?? "--"} PRIORITY
            </div>

            <div className="threat-details">
              <div>
                <span>Classification</span>
                <strong>{classification?.predicted_class ?? "--"}</strong>
              </div>

              <div>
                <span>Confidence</span>
                <strong>
                  {classification?.confidence != null
                    ? `${classification.confidence}%`
                    : "--"}
                </strong>
              </div>

              <div className="signal-parameters">
                <div className="score-breakdown">
  <h3>SCORE BREAKDOWN</h3>

  <div className="score-row">
    <span>Classification</span>
    <strong>+{threat?.score_breakdown?.classification ?? 0}</strong>
  </div>

  <div className="score-row">
    <span>AI Confidence</span>
    <strong>+{threat?.score_breakdown?.confidence?.toFixed(2) ?? "0.00"}</strong>
  </div>

  <div className="score-row">
    <span>Signal Power</span>
    <strong>+{threat?.score_breakdown?.power?.toFixed(2) ?? "0.00"}</strong>
  </div>

  <div className="score-row">
    <span>Frequency Variation</span>
    <strong>+{threat?.score_breakdown?.frequency_variation?.toFixed(2) ?? "0.00"}</strong>
  </div>

  <div className="score-row">
    <span>Bandwidth</span>
    <strong>+{threat?.score_breakdown?.bandwidth?.toFixed(2) ?? "0.00"}</strong>
  </div>
</div>
  <h3>SIGNAL PARAMETERS</h3>

  <div className="parameter-grid">

    <div>
  <span>Frequency</span>
  <strong>
    {signal?.frequency_mhz?.toFixed(2) ?? "--"} MHz
  </strong>
</div>
    <div>
      <span>Power</span>
      <strong>{signal?.power_db?.toFixed(2) ?? "--"} dB</strong>
    </div>

    <div>
      <span>Bandwidth</span>
      <strong>{signal?.bandwidth_mhz?.toFixed(2) ?? "--"} MHz</strong>
    </div>

    <div>
      <span>Pulse Width</span>
      <strong>{signal?.pulse_width_ms?.toFixed(2) ?? "--"} ms</strong>
    </div>

    <div>
      <span>Pulse Interval</span>
      <strong>{signal?.pulse_interval_ms?.toFixed(2) ?? "--"} ms</strong>
    </div>

    <div>
      <span>Frequency Variation</span>
      <strong>{signal?.frequency_variation_mhz?.toFixed(2) ?? "--"} MHz</strong>
    </div>

    <div>
      <span>Duration</span>
      <strong>{signal?.duration_sec?.toFixed(2) ?? "--"} sec</strong>
    </div>

    <div>
      <span>Spectral Entropy</span>
      <strong>{signal?.spectral_entropy?.toFixed(3) ?? "--"}</strong>
    </div>
  </div>
</div>

              
            </div>
          </div>

        </section>

        {/* Bottom Section */}
        <section className="bottom-grid">

          {/* Detected Emitters */}
          <div className="panel emitter-panel">
            <div className="panel-header">
              <div>
                <h2>DETECTED SIGNALS</h2>
                <p>Recent simulated observations</p>
              </div>
            </div>

            <table>
              <thead>
                <tr>
                  <th>Frequency</th>
                  <th>Classification</th>
                  <th>Confidence</th>
                  <th>Threat Score</th>
                  <th>Priority</th>
                </tr>
              </thead>

              <tbody>
                {detectedSignals.map((item, index) => (
                  <tr key={index}>
                    <td>{item.signal?.frequency_mhz?.toFixed(1)} MHz</td>
<td>{item.classification?.predicted_class}</td>
<td>{item.classification?.confidence}%</td>
<td>{item.threat?.threat_score?.toFixed(0)}</td>
<td>
  <span className={`priority ${item.threat?.priority?.toLowerCase()}`}>
    {item.threat?.priority}
  </span>
</td>
                   </tr>
                  ))}
              </tbody>
            </table>
          </div>

          {/* AI Recommendation */}
          <div className="panel recommendation-panel">
            <div className="panel-header">
              <div>
                <h2>AI SCAN RECOMMENDATION</h2>
                <p>Adaptive monitoring prediction</p>
              </div>
            </div>

            <div className="recommendation">

  <div className="recommendation-flow">

    <div className="recommendation-step">
      <span>CURRENT FREQUENCY</span>
      <strong>
        {signal?.frequency_mhz != null
          ? `${signal.frequency_mhz.toFixed(1)} MHz`
          : "--"}
      </strong>
    </div>

    <div className="recommendation-arrow">
      →
    </div>

    <div className="recommendation-step">
      <span>AI PREDICTION</span>
      <strong>
        {prediction?.next_frequency_mhz != null
          ? `${prediction.next_frequency_mhz.toFixed(1)} MHz`
          : "--"}
      </strong>
    </div>

    <div className="recommendation-step">
  <span>OBSERVATIONS USED</span>
  <strong>
    {prediction?.history_size ?? "--"}
  </strong>
</div>

  </div>

  <p>
    The AI analyzes recent simulated frequency observations
    and predicts the next frequency region to monitor.
  </p>

</div>
          </div>

        </section>

        {/* Alerts */}
        <section className="panel alerts-panel">
          <div className="panel-header">
            <div>
              <h2>ALERTS</h2>
              <p>Suspicious simulated observations</p>
            </div>

            <span className="alert-count">
                {alerts.length} ALERTS
            </span>
          </div>

          {alerts.map((item, index) => (
 <div
  className={`alert ${item.alert?.severity?.toLowerCase()}`}
  key={index}
>
    <span className={`alert-icon ${item.alert?.severity?.toLowerCase()}`}>
  {item.alert?.severity}
</span>

    <div>
      <strong>{item.alert?.message}</strong>

      <p>
  {item.signal?.frequency_mhz?.toFixed(1)} MHz •{" "}
  {item.classification?.predicted_class} •{" "}
  Confidence: {item.classification?.confidence}% •{" "}
  Threat Score: {item.threat?.threat_score?.toFixed(0)}
</p>
    </div>

    <span className="alert-time">
      {index === 0 ? "NOW" : `${index * 2}s ago`}
    </span>
  </div>
))}
        </section>

      </main>

      <footer>
        SOFTWARE-ONLY SIMULATION • AI-BASED RF MONITORING
      </footer>
    </div>
  );
}

export default App;
