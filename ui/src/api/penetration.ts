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

const defaultBaseUrl = "/transport";

export const buildPenTestUrl = (path: string, baseUrl = defaultBaseUrl) =>
  `${baseUrl.replace(/\/$/, "")}${path}`;

export const fetchPenTests = async (signal?: AbortSignal): Promise<PenTestApiResponse> => {
  const baseUrl = import.meta.env.VITE_TRANSPORT_BASE_URL || defaultBaseUrl;
  const response = await fetch(buildPenTestUrl("/penetration/tests", baseUrl), {
    method: "GET",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-Forwarded-Proto": "https"
    },
    signal
  });

  if (!response.ok) {
    throw new Error(`Penetration tests unavailable (${response.status})`);
  }

  return response.json() as Promise<PenTestApiResponse>;
};
