import { Link } from "react-router-dom";
import SectionHeader from "../components/SectionHeader";

const ComplianceAudit = () => (
  <section className="page">
    <header className="page__header">
      <div>
        <h1>Compliance &amp; Audit</h1>
        <p className="page__subtitle">
          Proof and evidence with drift visibility and audit-ready bundles.
        </p>
      </div>
      <Link className="ghost-button" to="/compliance-audit">
        Generate audit bundle
      </Link>
    </header>

    <div className="grid grid--two">
      <section className="card">
        <SectionHeader
          title="Framework posture"
          description="Framework readiness and exceptions."
        />
        <p className="muted">Framework posture placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Per-control evidence"
          description="Evidence per control with traceability."
        />
        <p className="muted">Control evidence placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Drift history"
          description="Time-series drift and exception timelines."
        />
        <p className="muted">Drift history placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Audit bundle generation"
          description="Automated, curated audit bundles."
        />
        <p className="muted">Audit bundle placeholder.</p>
      </section>
    </div>
  </section>
);

export default ComplianceAudit;
