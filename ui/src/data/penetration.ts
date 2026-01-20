export type PenTestStatus = "Planned" | "Running" | "Completed" | "Blocked" | "Aborted";

export type PenTest = {
  id: string;
  tenant: string;
  name: string;
  testType: string;
  method: string;
  window: string;
  status: PenTestStatus;
  scope: string;
  evidenceCount: number;
};

export const penTests: PenTest[] = [
  {
    id: "PT-2024-081",
    tenant: "Palmertech Primary",
    name: "External perimeter validation",
    testType: "Perimeter",
    method: "Detection-only",
    window: "2024-08-16 22:00-23:00 UTC",
    status: "Planned",
    scope: "Core Firewall, VPN gateways",
    evidenceCount: 0
  },
  {
    id: "PT-2024-082",
    tenant: "Palmertech Primary",
    name: "Identity resilience exercise",
    testType: "Identity",
    method: "Assumed breach",
    window: "2024-08-14 20:00-21:00 UTC",
    status: "Completed",
    scope: "M365 tenant, IAM policies",
    evidenceCount: 14
  },
  {
    id: "PT-2024-083",
    tenant: "Palmertech Primary",
    name: "Endpoint response drill",
    testType: "Endpoint",
    method: "Detection-only",
    window: "2024-08-15 18:00-19:30 UTC",
    status: "Running",
    scope: "Ring 2 endpoints",
    evidenceCount: 6
  },
  {
    id: "PT-2024-084",
    tenant: "Palmertech Primary",
    name: "Database lateral movement",
    testType: "Lateral Movement",
    method: "Adversary simulation",
    window: "2024-08-13 01:00-03:00 UTC",
    status: "Blocked",
    scope: "DB Cluster",
    evidenceCount: 2
  }
];

export const penetrationMetrics = {
  scheduled: 3,
  running: 1,
  blocked: 1,
  evidenceBundles: 24
};
