import SectionHeader from "../components/SectionHeader";

const Rmm = () => (
  <section className="page">
    <header className="page__header">
      <div>
        <h1>RMM</h1>
        <p className="page__subtitle">
          Operational health and control with telemetry-first context. Security alerts live elsewhere.
        </p>
      </div>
      <button className="ghost-button" type="button">
        View maintenance windows
      </button>
    </header>

    <div className="grid grid--two">
      <section className="card">
        <SectionHeader
          title="Telemetry dashboards"
          description="Availability, performance, and operational baselines."
        />
        <p className="muted">Placeholder for live telemetry widgets.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Asset availability"
          description="Uptime and outage insight linked to asset records."
        />
        <p className="muted">Asset availability board with drill-down.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Patch execution status"
          description="Policy-driven patch actions and outcomes."
        />
        <p className="muted">Execution history and blockers.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Script execution history"
          description="Approved scripts with traceable outcomes."
        />
        <p className="muted">Recent scripts with evidence bundle links.</p>
      </section>
    </div>
  </section>
);

export default Rmm;
