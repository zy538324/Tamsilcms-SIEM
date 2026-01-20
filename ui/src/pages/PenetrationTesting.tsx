import SectionHeader from "../components/SectionHeader";

const PenetrationTesting = () => (
  <section className="page">
    <header className="page__header">
      <div>
        <h1>Penetration Testing</h1>
        <p className="page__subtitle">
          Validation and humility focused on what failed to detect or stop.
        </p>
      </div>
      <button className="ghost-button" type="button">
        Schedule test
      </button>
    </header>

    <div className="grid grid--two">
      <section className="card">
        <SectionHeader
          title="Scheduled tests"
          description="Planned tests with scope and evidence requirements."
        />
        <p className="muted">Schedule timeline placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Historical results"
          description="Outcomes and control gaps over time."
        />
        <p className="muted">Historical results placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Control effectiveness"
          description="Measure detection and response outcomes."
        />
        <p className="muted">Effectiveness dashboard placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Evidence bundles"
          description="Evidence ready for audit and remediation."
        />
        <p className="muted">Evidence bundle placeholder.</p>
      </section>
    </div>
  </section>
);

export default PenetrationTesting;
