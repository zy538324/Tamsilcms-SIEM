import { fetchCoreService, resolveTransportBaseUrl } from "./coreServices";

export type DetectionFinding = {
  finding_id: string;
  finding_type: string;
  severity: "low" | "medium" | "high" | "critical";
  confidence_score: number;
  explanation_text: string;
  creation_timestamp: string;
  state: "open" | "superseded" | "dismissed" | "escalated";
  context_snapshot: {
    asset: {
      asset_id: string;
      hostname?: string;
      environment?: string;
      criticality?: string;
    };
  };
};

export type FindingListResponse = {
  findings: DetectionFinding[];
};

// Detection service feeds the SIEM and detection views.
export const fetchFindings = async (signal?: AbortSignal): Promise<DetectionFinding[]> => {
  const baseUrl = resolveTransportBaseUrl();
  const response = await fetchCoreService<FindingListResponse>(
    "detection",
    "/findings?limit=100",
    signal,
    baseUrl
  );
  return response.findings;
};
