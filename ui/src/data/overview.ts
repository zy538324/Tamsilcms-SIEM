export type StatusLevel = "Healthy" | "Degraded" | "At Risk";

export const environmentStatus: { summary: StatusLevel; rationale: string; updatedAt: string } = {
  summary: "Healthy",
  rationale: "Patch backlog and elevated exposure on critical assets",
  updatedAt: "09:42 UTC"
};

export const assetPosture = {
  healthy: 842,
  degraded: 97,
  atRisk: 21
};

export const findingsSummary = [
  { category: "Endpoint", confidence: "High", count: 12 },
  { category: "Identity", confidence: "Medium", count: 9 },
  { category: "Network", confidence: "High", count: 6 },
  { category: "Cloud", confidence: "Low", count: 4 }
];

export const exposureTrend = [
  { label: "30 days", exposure: 28 },
  { label: "14 days", exposure: 24 },
  { label: "7 days", exposure: 21 },
  { label: "Today", exposure: 26 }
];

export const patchCompliance = {
  compliant: 78,
  scheduled: 14,
  overdue: 8
};

export const psaItems = [
  {
    id: "PSA-1284",
    title: "Recover stalled patch rings",
    slaHours: 5,
    status: "Awaiting approval"
  },
  {
    id: "PSA-1287",
    title: "Review containment for asset PT-GW-19",
    slaHours: 12,
    status: "In progress"
  }
];

export const complianceDrift = [
  {
    framework: "Cyber Essentials",
    drift: "2 controls out of tolerance",
    nextAudit: "2024-11-02"
  },
  {
    framework: "ISO 27001",
    drift: "Evidence missing for A.12.4",
    nextAudit: "2024-10-17"
  }
];
