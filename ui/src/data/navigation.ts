export type NavItem = {
  label: string;
  path: string;
  description: string;
};

export const primaryNavigation: NavItem[] = [
  {
    label: "Overview",
    path: "/overview",
    description: "Single pane of truth"
  },
  {
    label: "Assets",
    path: "/assets",
    description: "Asset anchor and posture"
  },
  {
    label: "RMM",
    path: "/rmm",
    description: "Operational health and control"
  },
  {
    label: "SIEM",
    path: "/siem",
    description: "Investigation and memory"
  },
  {
    label: "Detection & EDR",
    path: "/detection-edr",
    description: "Judgement and defence"
  },
  {
    label: "Vulnerabilities",
    path: "/vulnerabilities",
    description: "Exposure awareness"
  },
  {
    label: "Patch Management",
    path: "/patch-management",
    description: "Controlled change"
  },
  {
    label: "Penetration Testing",
    path: "/penetration-testing",
    description: "Validation and humility"
  },
  {
    label: "PSA / Workflows",
    path: "/psa-workflows",
    description: "Human accountability"
  },
  {
    label: "Compliance & Audit",
    path: "/compliance-audit",
    description: "Proof and evidence"
  },
  {
    label: "Administration",
    path: "/administration",
    description: "Platform configuration"
  }
];
