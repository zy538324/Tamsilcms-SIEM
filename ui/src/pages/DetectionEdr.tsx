import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchFindings } from "../api/detection";
import SectionHeader from "../components/SectionHeader";
import type { DetectionFinding } from "../api/detection";
import { formatUtcTimestamp, toTitleCase } from "../utils/formatters";

const DetectionEdr = () => {
  const [findings, setFindings] = useState<DetectionFinding[]>([]);

  useEffect(() => {
    const controller = new AbortController();

    fetchFindings(controller.signal)
      .then((data) => setFindings(data))
      .catch(() => setFindings([]));

    return () => controller.abort();
  }, []);

  const recentFindings = findings.slice(0, 4);

  return (
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
          {recentFindings.length > 0 ? (
            <ul className="list">
              {recentFindings.map((finding) => (
                <li key={finding.finding_id}>
                  <div>
                    <strong>{toTitleCase(finding.finding_type)}</strong>
                    <p>{toTitleCase(finding.severity)} severity · {finding.state}</p>
                  </div>
                  <span className="badge">{formatUtcTimestamp(finding.creation_timestamp)}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="muted">Findings queue placeholder.</p>
          )}
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
};

export default DetectionEdr;
