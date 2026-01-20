import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import DataTable from "../components/DataTable";
import MetricCard from "../components/MetricCard";
import SectionHeader from "../components/SectionHeader";
import { psaMetrics, psaTickets, psaWorkload } from "../data/psa";

const statusOptions = ["All", "New", "In Progress", "Awaiting Approval", "Blocked", "Resolved"] as const;
type StatusOption = (typeof statusOptions)[number];

const PsaWorkflows = () => (
  <PsaWorkspace />
);

const PsaWorkspace = () => {
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState<StatusOption>("All");

  const filteredTickets = useMemo(() => {
    const lowerQuery = query.trim().toLowerCase();
    return psaTickets.filter((ticket) => {
      const matchesQuery =
        !lowerQuery ||
        ticket.title.toLowerCase().includes(lowerQuery) ||
        ticket.id.toLowerCase().includes(lowerQuery) ||
        ticket.owner.toLowerCase().includes(lowerQuery);
      const matchesStatus = statusFilter === "All" || ticket.status === statusFilter;
      return matchesQuery && matchesStatus;
    });
  }, [query, statusFilter]);

  return (
    <section className="page">
      <header className="page__header">
        <div>
          <h1>PSA / Workflows</h1>
          <p className="page__subtitle">
            Human accountability with evidence-backed ticketing and approvals.
          </p>
        </div>
        <Link className="ghost-button" to="/psa-workflows">
          View approval queue
        </Link>
      </header>

      <div className="grid grid--metrics">
        <MetricCard
          title="Open tickets"
          value={psaMetrics.openTickets}
          subtitle="Active items requiring action"
          accent="warning"
        />
        <MetricCard
          title="Awaiting approval"
          value={psaMetrics.awaitingApproval}
          subtitle="Decision queue"
        />
        <MetricCard
          title="SLA breaches"
          value={psaMetrics.breachedSla}
          subtitle="Immediate escalation required"
          accent="risk"
        />
        <MetricCard
          title="MTTR"
          value={`${psaMetrics.meanTimeToResolveHours}h`}
          subtitle="Mean time to resolve"
          accent="success"
        />
      </div>

      <section className="card">
        <SectionHeader
          title="Ticket queue"
          description="Tickets derived from system truth, filtered by SLA pressure."
        />
        <div className="filter-bar">
          <label className="filter-bar__item">
            <span className="eyebrow">Search tickets</span>
            <input
              className="text-input"
              type="search"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search by ticket, title, or owner"
              aria-label="Search tickets"
            />
          </label>
          <label className="filter-bar__item">
            <span className="eyebrow">Status</span>
            <select
              className="text-input"
              value={statusFilter}
              onChange={(event) => setStatusFilter(event.target.value as StatusOption)}
            >
              {statusOptions.map((status) => (
                <option key={status} value={status}>
                  {status}
                </option>
              ))}
            </select>
          </label>
        </div>
        <DataTable
          caption="Evidence-backed tickets"
          columns={[
            {
              header: "Ticket",
              accessor: (ticket) => (
                <Link className="text-link" to={`/psa-workflows/${ticket.id}`}>
                  {ticket.id}
                </Link>
              )
            },
            { header: "Title", accessor: (ticket) => ticket.title },
            { header: "Owner", accessor: (ticket) => ticket.owner },
            { header: "Priority", accessor: (ticket) => ticket.priority },
            { header: "Status", accessor: (ticket) => ticket.status },
            {
              header: "SLA (hrs)",
              accessor: (ticket) => (
                <span className={ticket.slaHoursRemaining <= 4 ? "sla-risk" : ""}>
                  {ticket.slaHoursRemaining}
                </span>
              )
            },
            { header: "Evidence", accessor: (ticket) => ticket.evidenceBundle }
          ]}
          rows={filteredTickets}
        />
      </section>

      <div className="grid grid--two">
        <section className="card">
          <SectionHeader
            title="SLA pressure indicators"
            description="Teams under pressure, with escalation signals."
          />
          <ul className="list">
            {psaWorkload.map((team) => (
              <li key={team.owner}>
                <div>
                  <strong>{team.owner}</strong>
                  <p>{team.active} active tickets</p>
                </div>
                <span className={team.overdue > 0 ? "badge badge--warning" : "badge"}>
                  {team.overdue} overdue
                </span>
              </li>
            ))}
          </ul>
        </section>

        <section className="card">
          <SectionHeader
            title="Approval actions"
            description="Decisions attributable to named roles."
          />
          <ul className="list">
            {psaTickets
              .filter((ticket) => ticket.status === "Awaiting Approval")
              .map((ticket) => (
                <li key={ticket.id}>
                  <div>
                    <strong>{ticket.id}</strong>
                    <p>{ticket.title}</p>
                  </div>
                  <Link className="text-link" to={`/psa-workflows/${ticket.id}`}>
                    View ticket
                  </Link>
                </li>
              ))}
          </ul>
        </section>
      </div>
    </section>
  );
};

export default PsaWorkflows;
