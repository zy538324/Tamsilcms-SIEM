export type TelemetryStatus = "Healthy" | "Degraded" | "At Risk";

export type TelemetryNode = {
  assetId: string;
  name: string;
  uptimeDays: number;
  patchRing: string;
  availability: number;
  status: TelemetryStatus;
};

export type MaintenanceWindow = {
  id: string;
  scope: string;
  window: string;
  owner: string;
  status: "Scheduled" | "In Progress" | "Completed" | "Blocked";
};

export type ScriptExecution = {
  id: string;
  scriptName: string;
  executedBy: string;
  status: "Succeeded" | "Failed" | "Needs Review";
  executedAt: string;
};

export const telemetryNodes: TelemetryNode[] = [
  {
    assetId: "core-fw-01",
    name: "Core Firewall",
    uptimeDays: 143,
    patchRing: "Ring 0",
    availability: 99.92,
    status: "Degraded"
  },
  {
    assetId: "db-cluster-02",
    name: "Primary DB Cluster",
    uptimeDays: 211,
    patchRing: "Ring 1",
    availability: 99.98,
    status: "Healthy"
  },
  {
    assetId: "win-app-14",
    name: "Windows App Server",
    uptimeDays: 73,
    patchRing: "Ring 2",
    availability: 98.4,
    status: "At Risk"
  },
  {
    assetId: "m365-tenant",
    name: "Microsoft 365",
    uptimeDays: 365,
    patchRing: "SaaS",
    availability: 99.99,
    status: "Healthy"
  }
];

export const maintenanceWindows: MaintenanceWindow[] = [
  {
    id: "MW-4401",
    scope: "Core Firewall",
    window: "2024-08-17 22:00-23:30 UTC",
    owner: "Network Ops",
    status: "Scheduled"
  },
  {
    id: "MW-4404",
    scope: "App Servers (Ring 2)",
    window: "2024-08-18 20:00-22:00 UTC",
    owner: "RMM Lead",
    status: "Blocked"
  },
  {
    id: "MW-4406",
    scope: "DB Cluster",
    window: "2024-08-19 01:00-02:00 UTC",
    owner: "Data Engineering",
    status: "Scheduled"
  }
];

export const scriptExecutions: ScriptExecution[] = [
  {
    id: "SC-1902",
    scriptName: "Validate endpoint encryption",
    executedBy: "RMM Automation",
    status: "Succeeded",
    executedAt: "2024-08-15 08:12"
  },
  {
    id: "SC-1907",
    scriptName: "Collect endpoint logs for incident EV-1842",
    executedBy: "SOC Tier 2",
    status: "Needs Review",
    executedAt: "2024-08-15 06:44"
  },
  {
    id: "SC-1911",
    scriptName: "Restart app services for Win-App-14",
    executedBy: "RMM Lead",
    status: "Failed",
    executedAt: "2024-08-14 23:11"
  }
];

export const rmmMetrics = {
  availability: 99.2,
  assetsAtRisk: 12,
  maintenanceWindows: 3,
  scriptsNeedingReview: 2
};
