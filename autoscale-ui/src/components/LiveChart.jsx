import React, { useEffect, useState } from "react";
import axios from "axios";
import LiveChart from "./LiveChart";
import "../styles/dashboard.css";

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [decision, setDecision] = useState(null);
  const [history, setHistory] = useState([]);

  const fetchData = async () => {
    try {
      const resMetrics = await axios.get("http://127.0.0.1:8000/metrics");
      const resDecision = await axios.get("http://127.0.0.1:8000/scale");

      setMetrics(resMetrics.data);
      setDecision(resDecision.data);

      setHistory((prev) => [
        ...prev.slice(-10),
        {
          time: new Date().toLocaleTimeString(),
          cpu: resMetrics.data?.cpu || 0,
          memory: resMetrics.data?.memory || 0,
        },
      ]);
    } catch (error) {
      console.error("API Error:", error);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard">
      <h1>🚀 Auto Scaling Dashboard</h1>

      <div className="card-container">
        <div className="card">
          <h3>CPU</h3>
          <p>{metrics?.cpu ?? 0}%</p>
        </div>

        <div className="card">
          <h3>Memory</h3>
          <p>{metrics?.memory ?? 0}%</p>
        </div>

        <div className="card">
          <h3>Requests/sec</h3>
          <p>{metrics?.requests_per_sec ?? 0}</p>
        </div>

        <div className="card">
          <h3>Predicted Load</h3>
          <p>{decision?.predicted_rps ?? "Loading..."}</p>
        </div>

        <div className="card">
          <h3>Decision</h3>
          <p>{decision?.action ?? "Waiting..."}</p>
        </div>

        <div className="card">
          <h3>Servers</h3>
          <p>{decision?.servers ?? "-"}</p>
        </div>
      </div>

      <h2>📈 Live Metrics</h2>
      {history.length > 0 ? (
        <LiveChart data={history} />
      ) : (
        <p>Loading chart...</p>
      )}
    </div>
  );
};

export default Dashboard;