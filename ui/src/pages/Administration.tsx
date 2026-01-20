import { Link } from "react-router-dom";
import SectionHeader from "../components/SectionHeader";

const Administration = () => (
  <section className="page">
    <header className="page__header">
      <div>
        <h1>Administration</h1>
        <p className="page__subtitle">
          Platform configuration, identity, RBAC, and tenant controls.
        </p>
      </div>
      <Link className="ghost-button" to="/administration">
        Manage roles
      </Link>
    </header>

    <div className="grid grid--two">
      <section className="card">
        <SectionHeader
          title="Identity & RBAC"
          description="Roles, permissions, and audit trails."
        />
        <p className="muted">RBAC configuration placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Tenant configuration"
          description="Multi-tenant controls and isolation."
        />
        <p className="muted">Tenant settings placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="System health controls"
          description="Read-only mode and safety switches."
        />
        <p className="muted">Platform safety controls placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Integrations"
          description="Configured integrations with least privilege."
        />
        <p className="muted">Integration inventory placeholder.</p>
      </section>
    </div>
  </section>
);

export default Administration;
