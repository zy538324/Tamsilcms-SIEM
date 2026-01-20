import { Link } from "react-router-dom";
import DataTable from "../components/DataTable";
import SectionHeader from "../components/SectionHeader";
import { assets } from "../data/assets";

const Assets = () => (
  <section className="page">
    <header className="page__header">
      <div>
        <h1>Assets</h1>
        <p className="page__subtitle">
          The anchor of truth. Every capability pivots back to assets for
          evidence, health telemetry, and accountability.
        </p>
      </div>
      <button className="ghost-button" type="button">
        Request asset report
      </button>
    </header>

    <section className="card">
      <SectionHeader
        title="Asset list"
        description="Operational roles, criticality, risk posture, and last-seen telemetry."
      />
      <DataTable
        caption="Asset inventory"
        columns={[
          {
            header: "Asset",
            accessor: (asset) => asset.name
          },
          {
            header: "Role",
            accessor: (asset) => asset.role
          },
          {
            header: "Criticality",
            accessor: (asset) => asset.criticality
          },
          {
            header: "Risk Score",
            accessor: (asset) => asset.riskScore
          },
          {
            header: "Last Seen",
            accessor: (asset) => asset.lastSeen
          },
          {
            header: "Owner",
            accessor: (asset) => asset.owner
          },
          {
            header: "Detail",
            accessor: (asset) => (
              <Link className="text-link" to={`/assets/${asset.id}`}>
                View
              </Link>
            )
          }
        ]}
        rows={assets}
      />
    </section>
  </section>
);

export default Assets;
