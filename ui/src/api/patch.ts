import { fetchCoreService, resolveTransportBaseUrl } from "./coreServices";

export type ComplianceSummaryResponse = {
  tenant_id: string;
  compliant: number;
  pending: number;
  failed: number;
};

export type AssetPatchStateResponse = {
  tenant_id: string;
  asset_id: string;
  status: "normal" | "patch_blocked";
  reason?: string | null;
  recorded_at: string;
};

// Patch management service for compliance posture and asset-level state.
export const fetchComplianceSummary = async (
  tenantId: string,
  signal?: AbortSignal
): Promise<ComplianceSummaryResponse> => {
  const baseUrl = resolveTransportBaseUrl();
  return fetchCoreService<ComplianceSummaryResponse>(
    "patch",
    `/compliance/${encodeURIComponent(tenantId)}`,
    signal,
    baseUrl
  );
};

export const fetchAssetPatchState = async (
  assetId: string,
  signal?: AbortSignal
): Promise<AssetPatchStateResponse> => {
  const baseUrl = resolveTransportBaseUrl();
  return fetchCoreService<AssetPatchStateResponse>(
    "patch",
    `/assets/${encodeURIComponent(assetId)}/state`,
    signal,
    baseUrl
  );
};
