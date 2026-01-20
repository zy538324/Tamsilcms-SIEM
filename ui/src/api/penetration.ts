import { fetchCoreService, resolveTransportBaseUrl } from "./coreServices";

export type PenTestApiResponse = {
  tests: Array<{
    test_id: string;
    tenant_id: string;
    test_type: string;
    method: string;
    status: string;
    created_at: string;
  }>;
};

export const fetchPenTests = async (signal?: AbortSignal): Promise<PenTestApiResponse> => {
  const baseUrl = resolveTransportBaseUrl();
  return fetchCoreService<PenTestApiResponse>("penetration", "/tests", signal, baseUrl);
};

export type PenTestDetailResponse = {
  status: string;
  test: {
    test_id: string;
    tenant_id: string;
    test_type: string;
    method: string;
    status: string;
    created_at: string;
    scope?: {
      assets?: string[];
      networks?: string[];
    };
  };
};

export const fetchPenTest = async (
  testId: string,
  signal?: AbortSignal
): Promise<PenTestDetailResponse> => {
  const baseUrl = resolveTransportBaseUrl();
  return fetchCoreService<PenTestDetailResponse>(
    "penetration",
    `/tests/${encodeURIComponent(testId)}`,
    signal,
    baseUrl
  );
};
