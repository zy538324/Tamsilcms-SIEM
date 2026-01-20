import { Link } from "react-router-dom";
import SectionHeader from "../components/SectionHeader";

const PatchManagement = () => (
  <section className="page">
    <header className="page__header">
      <div>
        <h1>Patch Management</h1>
        <p className="page__subtitle">
          Controlled change with policy-driven scheduling and clear blockers.
        </p>
      </div>
      <Link className="ghost-button" to="/patch-management">
        View patch policy
      </Link>
    </header>

    <div className="grid grid--two">
      <section className="card">
        <SectionHeader
          title="Patch compliance"
          description="Compliance overview without panic actions."
        />
        <p className="muted">Compliance dashboard placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Upcoming schedules"
          description="Next windows with clear dependencies."
        />
        <p className="muted">Schedule calendar placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Failures and blockers"
          description="Failures highlighted more than successes."
        />
        <p className="muted">Failure list placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Reboot tracking"
          description="Pending reboots across critical assets."
        />
        <p className="muted">Reboot queue placeholder.</p>
      </section>
    </div>
  </section>
);

export default PatchManagement;
