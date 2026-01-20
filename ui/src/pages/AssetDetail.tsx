import { Link, useParams } from "react-router-dom";
import SectionHeader from "../components/SectionHeader";
import { assetDetails, assets } from "../data/assets";

const AssetDetail = () => {
  const { assetId } = useParams();
  const asset = assets.find((item) => item.id === assetId);
  const detail = assetId ? assetDetails[assetId as keyof typeof assetDetails] : undefined;

  if (!asset || !detail) {
    return (
      <section className="page">
        <h1>Asset not found</h1>
        <p className="page__subtitle">
          The selected asset is unavailable. Please return to the asset list.
        </p>
      </section>
    );
  }

  return (
    <section className="page">
      <header className="page__header">
        <div>
          <h1>{asset.name}</h1>
          <p className="page__subtitle">{asset.role} · {asset.criticality} criticality</p>
        </div>
        <Link className="ghost-button" to="/siem">
          Request full evidence bundle
        </Link>
      </header>

      <div className="grid grid--two">
        <section className="card">
          <SectionHeader
            title="Identity & metadata"
            description="Asset identity, ownership, and environment context."
          />
          <ul className="list list--compact">
            <li>
              <span>Location</span>
              <strong>{detail.metadata.location}</strong>
            </li>
            <li>
              <span>Environment</span>
              <strong>{detail.metadata.environment}</strong>
            </li>
            <li>
              <span>Owner</span>
              <strong>{detail.metadata.owner}</strong>
            </li>
            <li>
              <span>Last patch</span>
              <strong>{detail.metadata.lastPatch}</strong>
            </li>
          </ul>
        </section>

        <section className="card">
          <SectionHeader
            title="Health telemetry"
            description="Live operational telemetry in context."
          />
          <ul className="list list--compact">
            <li>
              <span>CPU</span>
              <strong>{detail.telemetry.cpu}</strong>
            </li>
            <li>
              <span>Memory</span>
              <strong>{detail.telemetry.memory}</strong>
            </li>
            <li>
              <span>Uptime</span>
              <strong>{detail.telemetry.uptime}</strong>
            </li>
          </ul>
        </section>

        <section className="card">
          <SectionHeader
            title="Recent events"
            description="Context and provenance for the latest operational activity."
          />
          <ul className="list">
            {detail.recentEvents.map((event) => (
              <li key={event}>{event}</li>
            ))}
          </ul>
        </section>

        <section className="card">
          <SectionHeader
            title="Findings"
            description="Evidence-led detections with traceability."
            actionLabel="Open detection workspace"
            actionPath="/detection-edr"
          />
          <ul className="list">
            {detail.findings.map((finding) => (
              <li key={finding}>{finding}</li>
            ))}
          </ul>
        </section>
      </div>

      <div className="grid grid--two">
        <section className="card">
          <SectionHeader
            title="Vulnerabilities"
            description="Exposure and exploitability in plain view."
            actionLabel="View remediation guidance"
            actionPath="/vulnerabilities"
          />
          <ul className="list">
            {detail.vulnerabilities.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>

        <section className="card">
          <SectionHeader
            title="Patch state"
            description="Policy-driven maintenance context."
          />
          <p>{detail.patchState}</p>
          <Link className="ghost-button" to="/patch-management">
            View maintenance window
          </Link>
        </section>

        <section className="card">
          <SectionHeader
            title="Defence actions"
            description="Traceable actions with policy attribution."
          />
          <ul className="list">
            {detail.defenceActions.map((action) => (
              <li key={action}>{action}</li>
            ))}
          </ul>
        </section>

        <section className="card">
          <SectionHeader
            title="Tickets"
            description="PSA evidence-backed actions."
          />
          <ul className="list">
            {detail.tickets.map((ticket) => (
              <li key={ticket}>{ticket}</li>
            ))}
          </ul>
        </section>
      </div>

      <section className="card">
        <SectionHeader
          title="Compliance posture"
          description="Control evidence and drift status for this asset."
        />
        <p>{detail.compliancePosture}</p>
      </section>
    </section>
  );
};

export default AssetDetail;
