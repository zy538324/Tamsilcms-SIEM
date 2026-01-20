import { fetchCoreService, resolveTransportBaseUrl } from "./coreServices";

export type FrameworkMapping = {
  control_id: string;
  framework: string;
  mapped_control: string;
  mapped_at: string;
};

export type FrameworkMappingListResponse = {
  mappings: FrameworkMapping[];
};

// Compliance service surfaces framework mappings and audit-ready evidence.
export const fetchFrameworkMappings = async (signal?: AbortSignal): Promise<FrameworkMapping[]> => {
  const baseUrl = resolveTransportBaseUrl();
  const response = await fetchCoreService<FrameworkMappingListResponse>(
    "compliance",
    "/frameworks/mappings",
    signal,
    baseUrl
  );
  return response.mappings;
};
