import { Link } from "react-router-dom";
import SectionHeader from "../components/SectionHeader";

const DetectionEdr = () => (
  <section className="page">
    <header className="page__header">
      <div>
        <h1>Detection &amp; EDR</h1>
        <p className="page__subtitle">
          Judgement and defence with explanations always visible.
        </p>
      </div>
      <Link className="ghost-button" to="/detection-edr">
        Review false positives
      </Link>
    </header>

    <div className="grid grid--two">
      <section className="card">
        <SectionHeader
          title="Findings list"
          description="Evidence-first detections with attribution."
        />
        <p className="muted">Findings queue placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Defence actions"
          description="Actions tied to policy and audit trails."
        />
        <p className="muted">Actions history and policy references.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="False positive review"
          description="Manual review with recorded decisions."
        />
        <p className="muted">Review queue placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Rule attribution"
          description="Rules linked to explainability notes."
        />
        <p className="muted">Rule map placeholder.</p>
      </section>
    </div>
  </section>
);

export default DetectionEdr;
