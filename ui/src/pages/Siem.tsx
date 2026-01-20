import SectionHeader from "../components/SectionHeader";

const Siem = () => (
  <section className="page">
    <header className="page__header">
      <div>
        <h1>SIEM</h1>
        <p className="page__subtitle">
          Investigation and memory focused on reconstruction, not reaction.
        </p>
      </div>
      <button className="ghost-button" type="button">
        Export evidence
      </button>
    </header>

    <div className="grid grid--two">
      <section className="card">
        <SectionHeader
          title="Event search"
          description="Query events with cancellation and provenance."
        />
        <p className="muted">Search bar and filters (placeholder).</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Timeline reconstruction"
          description="Narrative view of incident chains."
        />
        <p className="muted">Timeline workspace with evidence links.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Correlation views"
          description="Link signals without severity inflation."
        />
        <p className="muted">Correlation graph placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Evidence export"
          description="Bundle logs, artefacts, and commentary."
        />
        <p className="muted">Export queue and audit trail.</p>
      </section>
    </div>
  </section>
);

export default Siem;
