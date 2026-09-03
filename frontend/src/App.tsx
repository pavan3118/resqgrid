import "./App.css";
import MapView from "./components/MapView";

function App() {
  return (
    <div className="dashboard">
      <header className="topbar">
        <div>
          <h1>🚨 ResQGrid</h1>
          <p>Real-Time Emergency Dispatch</p>
        </div>

        <div className="system-status">
          <span className="status-dot"></span>
          SYSTEM ONLINE
        </div>
      </header>

      <main className="dashboard-grid">
        <aside className="sidebar">
          <section className="panel">
            <h2>Incidents</h2>

            <div className="stat critical">
              <span>Critical</span>
              <strong>1</strong>
            </div>

            <div className="stat high">
              <span>High</span>
              <strong>2</strong>
            </div>

            <div className="stat medium">
              <span>Medium</span>
              <strong>0</strong>
            </div>
          </section>

          <section className="panel">
            <h2>Responders</h2>

            <div className="stat available">
              <span>Available</span>
              <strong>1</strong>
            </div>

            <div className="stat busy">
              <span>Busy</span>
              <strong>2</strong>
            </div>

            <div className="stat offline">
              <span>Offline</span>
              <strong>0</strong>
            </div>
          </section>
        </aside>

        <section className="map-container">
          <MapView />
        </section>
      </main>
    </div>
  );
}

export default App;