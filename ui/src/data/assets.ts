export type Asset = {
  id: string;
  name: string;
  role: string;
  criticality: "Low" | "Medium" | "High" | "Critical";
  riskScore: number;
  lastSeen: string;
  owner: string;
};

export const assets: Asset[] = [
  {
    id: "core-fw-01",
    name: "Core Firewall",
    role: "Perimeter Control",
    criticality: "Critical",
    riskScore: 92,
    lastSeen: "2 minutes ago",
    owner: "Network Ops"
  },
  {
    id: "db-cluster-02",
    name: "Primary DB Cluster",
    role: "Data Platform",
    criticality: "Critical",
    riskScore: 86,
    lastSeen: "6 minutes ago",
    owner: "Data Engineering"
  },
  {
    id: "win-app-14",
    name: "Windows App Server",
    role: "Line-of-business",
    criticality: "High",
    riskScore: 71,
    lastSeen: "12 minutes ago",
    owner: "Apps Team"
  },
  {
    id: "m365-tenant",
    name: "Microsoft 365",
    role: "Identity & Collaboration",
    criticality: "High",
    riskScore: 64,
    lastSeen: "5 minutes ago",
    owner: "Security"
  }
];

export const assetDetails = {
  "core-fw-01": {
    metadata: {
      location: "London DC-1",
      environment: "Production",
      owner: "Network Ops",
      lastPatch: "2024-08-03"
    },
    telemetry: {
      cpu: "62%",
      memory: "71%",
      uptime: "143 days"
    },
    recentEvents: [
      "Policy update deployed at 08:13 UTC",
      "New VPN peer added at 07:55 UTC"
    ],
    findings: [
      "Suspicious outbound traffic flagged (Evidence bundle EV-1834)",
      "EDR blocked unsigned binary execution"
    ],
    vulnerabilities: [
      "Edge TLS configuration at risk of downgrade",
      "Legacy cipher suite still enabled"
    ],
    patchState: "Pending maintenance window approval",
    defenceActions: [
      "Network quarantine policy applied",
      "SOC notified for monitoring escalation"
    ],
    tickets: [
      "PSA-1284: Recover stalled patch rings",
      "PSA-1291: Review firewall policy exceptions"
    ],
    compliancePosture: "2 controls require evidence refresh"
  },
  "db-cluster-02": {
    metadata: {
      location: "Manchester DC-2",
      environment: "Production",
      owner: "Data Engineering",
      lastPatch: "2024-08-06"
    },
    telemetry: {
      cpu: "41%",
      memory: "66%",
      uptime: "211 days"
    },
    recentEvents: [
      "Snapshot verified at 06:04 UTC",
      "Failover drill completed at 05:45 UTC"
    ],
    findings: [
      "Privileged login without MFA (Evidence bundle EV-1821)"
    ],
    vulnerabilities: [
      "Database engine minor update pending"
    ],
    patchState: "Scheduled for 2024-09-02",
    defenceActions: [
      "Temporary MFA enforcement added for service accounts"
    ],
    tickets: [
      "PSA-1272: Verify backup integrity"
    ],
    compliancePosture: "In tolerance"
  },
  "win-app-14": {
    metadata: {
      location: "Bristol DC-3",
      environment: "Production",
      owner: "Apps Team",
      lastPatch: "2024-08-01"
    },
    telemetry: {
      cpu: "53%",
      memory: "58%",
      uptime: "73 days"
    },
    recentEvents: [
      "Service restart completed at 06:42 UTC",
      "Maintenance check passed at 05:58 UTC"
    ],
    findings: [
      "Unsigned driver attempted execution (Evidence bundle EV-1819)"
    ],
    vulnerabilities: [
      "Legacy service account requires rotation"
    ],
    patchState: "Awaiting approval for September window",
    defenceActions: [
      "Application allow-list updated per policy"
    ],
    tickets: [
      "PSA-1298: Rotate service account credentials"
    ],
    compliancePosture: "Evidence refreshed for A.9 controls"
  },
  "m365-tenant": {
    metadata: {
      location: "Cloud - UK South",
      environment: "Production",
      owner: "Security",
      lastPatch: "Continuous SaaS updates"
    },
    telemetry: {
      cpu: "Managed service",
      memory: "Managed service",
      uptime: "SLA monitored"
    },
    recentEvents: [
      "Conditional access policy updated at 07:18 UTC",
      "Audit log export verified at 06:12 UTC"
    ],
    findings: [
      "Legacy auth protocol detected for two accounts"
    ],
    vulnerabilities: [
      "MFA adoption below target for guest users"
    ],
    patchState: "Vendor managed",
    defenceActions: [
      "Legacy auth blocked for new sign-ins"
    ],
    tickets: [
      "PSA-1301: Complete MFA adoption campaign"
    ],
    compliancePosture: "Exception logged for third-party integrations"
  }
};
