import { Link, useParams } from "react-router-dom";
import SectionHeader from "../components/SectionHeader";
import { patchItems } from "../data/patch";

const PatchDetail = () => {
  const { patchId } = useParams();
  const patchItem = patchItems.find((item) => item.id === patchId);

  if (!patchItem) {
    return (
      <section className="page">
        <h1>Patch item not found</h1>
        <p className="page__subtitle">
          The selected patch record is unavailable. Please return to patch management.
        </p>
        <Link className="ghost-button" to="/patch-management">
          Back to patch dashboard
        </Link>
      </section>
    );
  }

  return (
    <section className="page">
      <header className="page__header">
        <div>
          <h1>{patchItem.id}</h1>
          <p className="page__subtitle">{patchItem.asset} · {patchItem.status}</p>
        </div>
        <Link className="ghost-button" to="/patch-management">
          View patch calendar
        </Link>
      </header>

      <div className="grid grid--two">
        <section className="card">
          <SectionHeader
            title="Patch status"
            description="Policy-driven status with ring and scheduling context."
          />
          <ul className="list list--compact">
            <li>
              <span>Ring</span>
              <strong>{patchItem.ring}</strong>
            </li>
            <li>
              <span>Last patch</span>
              <strong>{patchItem.lastPatch}</strong>
            </li>
            <li>
              <span>Next window</span>
              <strong>{patchItem.nextWindow}</strong>
            </li>
            <li>
              <span>Status</span>
              <strong>{patchItem.status}</strong>
            </li>
          </ul>
        </section>

        <section className="card">
          <SectionHeader
            title="Blockers"
            description="Failures and blockers highlighted above successes."
          />
          <p>{patchItem.blocker ?? "No blockers recorded."}</p>
          <Link className="ghost-button" to="/psa-workflows">
            Raise change ticket
          </Link>
        </section>
      </div>

      <section className="card">
        <SectionHeader
          title="Operational notes"
          description="Captured change context linked to assets and evidence."
        />
        <ul className="list">
          <li>
            <div>
              <strong>Asset owner informed</strong>
              <p>Change advisory notified via PSA.</p>
            </div>
            <span className="badge">Logged</span>
          </li>
          <li>
            <div>
              <strong>Maintenance window</strong>
              <p>{patchItem.nextWindow}</p>
            </div>
            <span className="badge">Scheduled</span>
          </li>
        </ul>
      </section>
    </section>
  );
};

export default PatchDetail;
