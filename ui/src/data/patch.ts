export type PatchStatus = "Compliant" | "Scheduled" | "Overdue" | "Failed";

export type PatchItem = {
  id: string;
  asset: string;
  ring: string;
  status: PatchStatus;
  lastPatch: string;
  nextWindow: string;
  blocker?: string;
};

export type PatchSchedule = {
  id: string;
  window: string;
  scope: string;
  owner: string;
  readiness: "Ready" | "Needs Approval" | "Blocked";
};

export type PatchMetrics = {
  compliant: number;
  scheduled: number;
  overdue: number;
  failures: number;
};

export const patchItems: PatchItem[] = [
  {
    id: "PT-901",
    asset: "Core Firewall",
    ring: "Ring 0",
    status: "Scheduled",
    lastPatch: "2024-08-03",
    nextWindow: "2024-08-17 22:00 UTC",
    blocker: "Change approval pending"
  },
  {
    id: "PT-904",
    asset: "Windows App Server",
    ring: "Ring 2",
    status: "Overdue",
    lastPatch: "2024-07-10",
    nextWindow: "2024-08-18 20:00 UTC",
    blocker: "Restart dependency in progress"
  },
  {
    id: "PT-907",
    asset: "Primary DB Cluster",
    ring: "Ring 1",
    status: "Compliant",
    lastPatch: "2024-08-06",
    nextWindow: "2024-09-02 01:00 UTC"
  },
  {
    id: "PT-910",
    asset: "Microsoft 365",
    ring: "SaaS",
    status: "Compliant",
    lastPatch: "Rolling",
    nextWindow: "Managed"
  },
  {
    id: "PT-912",
    asset: "Jump Host",
    ring: "Ring 1",
    status: "Failed",
    lastPatch: "2024-08-12",
    nextWindow: "2024-08-19 02:00 UTC",
    blocker: "Insufficient disk space"
  }
];

export const patchSchedules: PatchSchedule[] = [
  {
    id: "PS-3101",
    window: "2024-08-17 22:00 UTC",
    scope: "Ring 0 critical assets",
    owner: "Change Advisory",
    readiness: "Needs Approval"
  },
  {
    id: "PS-3104",
    window: "2024-08-18 20:00 UTC",
    scope: "Ring 2 endpoints",
    owner: "RMM Lead",
    readiness: "Blocked"
  },
  {
    id: "PS-3106",
    window: "2024-08-19 01:00 UTC",
    scope: "Ring 1 databases",
    owner: "Data Engineering",
    readiness: "Ready"
  }
];

export const patchMetrics: PatchMetrics = {
  compliant: 78,
  scheduled: 14,
  overdue: 8,
  failures: 3
};
