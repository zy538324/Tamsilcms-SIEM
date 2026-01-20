import { Link, useParams } from "react-router-dom";
import SectionHeader from "../components/SectionHeader";
import { psaTickets } from "../data/psa";

const PsaTicketDetail = () => {
  const { ticketId } = useParams();
  const ticket = psaTickets.find((item) => item.id === ticketId);

  if (!ticket) {
    return (
      <section className="page">
        <h1>Ticket not found</h1>
        <p className="page__subtitle">
          The selected PSA ticket is unavailable. Please return to the workflow queue.
        </p>
        <Link className="ghost-button" to="/psa-workflows">
          Back to PSA dashboard
        </Link>
      </section>
    );
  }

  return (
    <section className="page">
      <header className="page__header">
        <div>
          <h1>{ticket.id}</h1>
          <p className="page__subtitle">{ticket.title}</p>
        </div>
        <Link className="ghost-button" to={`/assets/${ticket.linkedAsset}`}>
          View linked asset
        </Link>
      </header>

      <div className="grid grid--two">
        <section className="card">
          <SectionHeader
            title="Ticket context"
            description="Owner, priority, and SLA pressure for accountable decisions."
          />
          <ul className="list list--compact">
            <li>
              <span>Owner</span>
              <strong>{ticket.owner}</strong>
            </li>
            <li>
              <span>Priority</span>
              <strong>{ticket.priority}</strong>
            </li>
            <li>
              <span>Status</span>
              <strong>{ticket.status}</strong>
            </li>
            <li>
              <span>SLA remaining</span>
              <strong>{ticket.slaHoursRemaining} hours</strong>
            </li>
          </ul>
        </section>

        <section className="card">
          <SectionHeader
            title="Evidence bundle"
            description="Evidence is immutable and must be reviewed before action."
          />
          <p>
            Bundle reference <strong>{ticket.evidenceBundle}</strong>
          </p>
          <Link className="ghost-button" to="/siem">
            Open evidence in SIEM
          </Link>
        </section>
      </div>

      <section className="card">
        <SectionHeader
          title="Decision log"
          description="Maintain attributable decisions and approvals."
        />
        <ul className="list">
          <li>
            <div>
              <strong>Created</strong>
              <p>{ticket.createdAt} UTC</p>
            </div>
            <span className="badge">System generated</span>
          </li>
          <li>
            <div>
              <strong>Current state</strong>
              <p>{ticket.status}</p>
            </div>
            <span className="badge">Awaiting action</span>
          </li>
        </ul>
      </section>
    </section>
  );
};

export default PsaTicketDetail;
