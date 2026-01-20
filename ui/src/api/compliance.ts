import { fetchCoreService } from "./coreServices";

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
  // Auditing service exposes frameworks/controls via `/frameworks` and `/controls`.
  // Fetch frameworks for now; mapping endpoints can be added later.
  const response = await fetchCoreService<any>("auditing", "/frameworks", signal);
  // Attempt to coerce to the expected shape when possible, otherwise return empty list.
  if (Array.isArray(response)) {
    return response.map((f: any) => ({ control_id: f.id || "", framework: f.name || "", mapped_control: "" , mapped_at: new Date().toISOString()}));
  }
  return [];
};
