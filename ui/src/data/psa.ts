export type TicketStatus = "New" | "In Progress" | "Awaiting Approval" | "Blocked" | "Resolved";
export type TicketPriority = "Low" | "Medium" | "High" | "Critical";

export type Ticket = {
  id: string;
  title: string;
  owner: string;
  priority: TicketPriority;
  status: TicketStatus;
  slaHoursRemaining: number;
  createdAt: string;
  linkedAsset: string;
  evidenceBundle: string;
};

export const psaTickets: Ticket[] = [
  {
    id: "PSA-1306",
    title: "Contain credential reuse on finance endpoints",
    owner: "SOC Tier 2",
    priority: "Critical",
    status: "In Progress",
    slaHoursRemaining: 3,
    createdAt: "2024-08-15 09:12",
    linkedAsset: "win-app-14",
    evidenceBundle: "EV-1842"
  },
  {
    id: "PSA-1308",
    title: "Approve emergency patch window for Core Firewall",
    owner: "Change Advisory",
    priority: "High",
    status: "Awaiting Approval",
    slaHoursRemaining: 6,
    createdAt: "2024-08-15 07:30",
    linkedAsset: "core-fw-01",
    evidenceBundle: "EV-1834"
  },
  {
    id: "PSA-1311",
    title: "Review M365 legacy authentication exceptions",
    owner: "Identity Ops",
    priority: "Medium",
    status: "New",
    slaHoursRemaining: 18,
    createdAt: "2024-08-14 17:55",
    linkedAsset: "m365-tenant",
    evidenceBundle: "EV-1850"
  },
  {
    id: "PSA-1314",
    title: "Validate backup integrity for DB Cluster",
    owner: "Data Engineering",
    priority: "High",
    status: "Blocked",
    slaHoursRemaining: 9,
    createdAt: "2024-08-14 14:10",
    linkedAsset: "db-cluster-02",
    evidenceBundle: "EV-1821"
  },
  {
    id: "PSA-1317",
    title: "Close remediation task for asset patch lag",
    owner: "RMM Lead",
    priority: "Low",
    status: "Resolved",
    slaHoursRemaining: 0,
    createdAt: "2024-08-13 11:02",
    linkedAsset: "win-app-14",
    evidenceBundle: "EV-1802"
  }
];

export const psaMetrics = {
  openTickets: 24,
  awaitingApproval: 5,
  breachedSla: 2,
  meanTimeToResolveHours: 11.4
};

export const psaWorkload = [
  { owner: "SOC Tier 1", active: 6, overdue: 1 },
  { owner: "SOC Tier 2", active: 8, overdue: 0 },
  { owner: "Change Advisory", active: 3, overdue: 1 },
  { owner: "Identity Ops", active: 4, overdue: 0 }
];
