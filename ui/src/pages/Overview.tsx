import MetricCard from "../components/MetricCard";
import SectionHeader from "../components/SectionHeader";
import StatusPill from "../components/StatusPill";
import {
  assetPosture,
  complianceDrift,
  environmentStatus,
  exposureTrend,
  findingsSummary,
  patchCompliance,
  psaItems
} from "../data/overview";

const Overview = () => (
  <section className="page">
    <header className="page__header">
      <div>
        <h1>Overview</h1>
        <p className="page__subtitle">
          A single pane of truth showing environment health, active threats, risk
          movement, and silent failures.
        </p>
      </div>
      <div className="page__status">
        <span className="eyebrow">Environment Status</span>
        <StatusPill status={environmentStatus.summary} />
        <p className="muted">Updated {environmentStatus.updatedAt}</p>
      </div>
    </header>

    <div className="grid grid--metrics">
      <MetricCard
        title="Asset posture"
        value={`${assetPosture.healthy} healthy`}
        subtitle={`${assetPosture.degraded} degraded · ${assetPosture.atRisk} at risk`}
        accent="success"
      />
      <MetricCard
        title="Active findings"
        value={`${findingsSummary.reduce((total, item) => total + item.count, 0)} open`}
        subtitle="High confidence and category view below"
        accent="warning"
      />
      <MetricCard
        title="Exposure trend"
        value={`${exposureTrend[exposureTrend.length - 1].exposure}%`}
        subtitle="Exposure level over 30 days"
        accent="risk"
      />
      <MetricCard
        title="Patch compliance"
        value={`${patchCompliance.compliant}% compliant`}
        subtitle={`${patchCompliance.overdue}% overdue · ${patchCompliance.scheduled}% scheduled`}
      />
    </div>

    <div className="grid grid--two">
      <section className="card">
        <SectionHeader
          title="Asset posture summary"
          description="Health of assets across criticality bands, with action paths into assets."
          actionLabel="View assets"
          actionPath="/assets"
        />
        <div className="stat-stack">
          <div>
            <span className="stat-value">{assetPosture.healthy}</span>
            <span className="stat-label">Healthy</span>
          </div>
          <div>
            <span className="stat-value">{assetPosture.degraded}</span>
            <span className="stat-label">Degraded</span>
          </div>
          <div>
            <span className="stat-value">{assetPosture.atRisk}</span>
            <span className="stat-label">At Risk</span>
          </div>
        </div>
        <p className="muted">Drill down to assets to investigate health drivers.</p>
      </section>

      <section className="card">
        <SectionHeader
          title="Active findings summary"
          description="Confidence and category split of live detections."
          actionLabel="Open detections"
          actionPath="/detection-edr"
        />
        <ul className="list">
          {findingsSummary.map((finding) => (
            <li key={`${finding.category}-${finding.confidence}`}>
              <strong>{finding.category}</strong>
              <span>{finding.confidence} confidence</span>
              <span className="badge">{finding.count}</span>
            </li>
          ))}
        </ul>
      </section>

      <section className="card">
        <SectionHeader
          title="Vulnerability exposure trend"
          description="Exposure-focused view to avoid CVE count distortion."
          actionLabel="View vulnerabilities"
          actionPath="/vulnerabilities"
        />
        <div className="trend">
          {exposureTrend.map((point) => (
            <div key={point.label} className="trend__point">
              <span className="trend__value">{point.exposure}%</span>
              <span className="trend__label">{point.label}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="card">
        <SectionHeader
          title="Patch compliance status"
          description="Policy-driven schedules and blockers with no emergency buttons."
          actionLabel="Review patching"
          actionPath="/patch-management"
        />
        <div className="stat-stack">
          <div>
            <span className="stat-value">{patchCompliance.compliant}%</span>
            <span className="stat-label">Compliant</span>
          </div>
          <div>
            <span className="stat-value">{patchCompliance.scheduled}%</span>
            <span className="stat-label">Scheduled</span>
          </div>
          <div>
            <span className="stat-value">{patchCompliance.overdue}%</span>
            <span className="stat-label">Overdue</span>
          </div>
        </div>
      </section>
    </div>

    <div className="grid grid--two">
      <section className="card">
        <SectionHeader
          title="Open PSA items"
          description="SLA pressure and decision queues grounded in evidence."
          actionLabel="Open workflow queue"
          actionPath="/psa-workflows"
        />
        <ul className="list">
          {psaItems.map((item) => (
            <li key={item.id}>
              <div>
                <strong>{item.id}</strong>
                <p>{item.title}</p>
              </div>
              <div className="list__meta">
                <span>{item.status}</span>
                <span className="badge badge--warning">{item.slaHours}h SLA</span>
              </div>
            </li>
          ))}
        </ul>
      </section>

      <section className="card">
        <SectionHeader
          title="Compliance drift indicators"
          description="Evidence-focused drift showing where proof is missing."
          actionLabel="Review compliance"
          actionPath="/compliance-audit"
        />
        <ul className="list">
          {complianceDrift.map((item) => (
            <li key={item.framework}>
              <div>
                <strong>{item.framework}</strong>
                <p>{item.drift}</p>
              </div>
              <span className="badge">Audit {item.nextAudit}</span>
            </li>
          ))}
        </ul>
      </section>
    </div>
  </section>
);

export default Overview;
