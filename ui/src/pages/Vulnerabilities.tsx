import { Link } from "react-router-dom";
import SectionHeader from "../components/SectionHeader";

const Vulnerabilities = () => (
  <section className="page">
    <header className="page__header">
      <div>
        <h1>Vulnerabilities</h1>
        <p className="page__subtitle">
          Exposure awareness with exploitability foregrounded. CVE counts are secondary.
        </p>
      </div>
      <Link className="ghost-button" to="/vulnerabilities">
        Review risk acceptances
      </Link>
    </header>

    <div className="grid grid--two">
      <section className="card">
        <SectionHeader
          title="Exposure-first views"
          description="Exposure scoring and attack path analysis."
        />
        <p className="muted">Exposure map placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Vulnerability lifecycle"
          description="Lifecycle states with evidence-driven transitions."
        />
        <p className="muted">Lifecycle board placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Risk acceptance"
          description="Documented decisions and expiry reminders."
        />
        <p className="muted">Risk acceptance workflow placeholder.</p>
      </section>
      <section className="card">
        <SectionHeader
          title="Remediation guidance"
          description="Prioritised guidance tied to assets."
        />
        <p className="muted">Guidance list placeholder.</p>
      </section>
    </div>
  </section>
);

export default Vulnerabilities;
