import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchAssets } from "../api/assets";
import { fetchAssetPatchState } from "../api/patch";
import SectionHeader from "../components/SectionHeader";
import { assetDetails, assets } from "../data/assets";
import type { Asset } from "../data/assets";
import { formatUtcTimestamp } from "../utils/formatters";

const buildDefaultDetail = (asset: Asset) => ({
  metadata: {
    location: "Unknown",
    environment: "Unknown",
    owner: asset.owner,
    lastPatch: "Unavailable"
  },
  telemetry: {
    cpu: "Unavailable",
    memory: "Unavailable",
    uptime: "Unavailable"
  },
  recentEvents: ["No recent events recorded."],
  findings: ["No findings recorded."],
  vulnerabilities: ["No vulnerability data recorded."],
  patchState: "Patch state unavailable",
  defenceActions: ["No defence actions recorded."],
  tickets: ["No tickets linked."],
  compliancePosture: "Compliance posture unavailable"
});

const AssetDetail = () => {
  const { assetId } = useParams();
  const fallbackAsset = assets.find((item) => item.id === assetId);
  const fallbackDetail = assetId ? assetDetails[assetId as keyof typeof assetDetails] : undefined;
  const [asset, setAsset] = useState<Asset | undefined>(fallbackAsset);
  const [detail, setDetail] = useState<typeof fallbackDetail>(fallbackDetail);

  useEffect(() => {
    if (!assetId) {
      return undefined;
    }
    const controller = new AbortController();

    fetchAssets(controller.signal)
      .then((response) => {
        const matched = response.find((item) => item.id === assetId);
        if (matched) {
          setAsset(matched);
        }
      })
      .catch(() => {
        setAsset(fallbackAsset);
      });

    return () => controller.abort();
  }, [assetId, fallbackAsset]);

  useEffect(() => {
    if (!assetId) {
      return undefined;
    }
    const controller = new AbortController();

    fetchAssetPatchState(assetId, controller.signal)
      .then((state) => {
        const baseDetail = fallbackDetail ?? (asset ? buildDefaultDetail(asset) : undefined);
        if (!baseDetail) {
          return;
        }
        const updatedState = state.status === "patch_blocked"
          ? `Patch blocked: ${state.reason ?? "No reason recorded"} · ${formatUtcTimestamp(state.recorded_at)}`
          : `Normal patch state · ${formatUtcTimestamp(state.recorded_at)}`;
        setDetail({
          ...baseDetail,
          patchState: updatedState
        });
      })
      .catch(() => {
        setDetail(fallbackDetail ?? (asset ? buildDefaultDetail(asset) : undefined));
      });

    return () => controller.abort();
  }, [asset, assetId, fallbackDetail]);

  const resolvedDetail = detail ?? (asset ? buildDefaultDetail(asset) : undefined);

  if (!asset || !resolvedDetail) {
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
          <strong>{resolvedDetail.metadata.location}</strong>
            </li>
            <li>
              <span>Environment</span>
          <strong>{resolvedDetail.metadata.environment}</strong>
            </li>
            <li>
              <span>Owner</span>
          <strong>{resolvedDetail.metadata.owner}</strong>
            </li>
            <li>
              <span>Last patch</span>
          <strong>{resolvedDetail.metadata.lastPatch}</strong>
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
          <strong>{resolvedDetail.telemetry.cpu}</strong>
            </li>
            <li>
              <span>Memory</span>
          <strong>{resolvedDetail.telemetry.memory}</strong>
            </li>
            <li>
              <span>Uptime</span>
          <strong>{resolvedDetail.telemetry.uptime}</strong>
            </li>
          </ul>
        </section>

        <section className="card">
          <SectionHeader
            title="Recent events"
            description="Context and provenance for the latest operational activity."
          />
          <ul className="list">
          {resolvedDetail.recentEvents.map((event) => (
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
          {resolvedDetail.findings.map((finding) => (
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
          {resolvedDetail.vulnerabilities.map((item) => (
            <li key={item}>{item}</li>
          ))}
          </ul>
        </section>

        <section className="card">
          <SectionHeader
            title="Patch state"
            description="Policy-driven maintenance context."
          />
          <p>{resolvedDetail.patchState}</p>
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
          {resolvedDetail.defenceActions.map((action) => (
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
          {resolvedDetail.tickets.map((ticket) => (
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
        <p>{resolvedDetail.compliancePosture}</p>
      </section>
    </section>
  );
};

export default AssetDetail;
