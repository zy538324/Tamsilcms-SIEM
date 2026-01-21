// Centralised helper to connect UI pages to core-services.
// Default behaviour is to route via the transport gateway (`/transport`).
// For dev and testing you can override any service with an explicit Vite env var,
// e.g. `VITE_PSA_BASE_URL`, `VITE_EDR_BASE_URL`, `VITE_INGESTION_BASE_URL`.
const defaultTransportBase = "/transport";

const sanitisePath = (path: string) => path.replace(/^\/+/, "");

const envBaseFor = (service: string): string | undefined => {
  // e.g. detection -> VITE_DETECTION_BASE_URL, edr -> VITE_EDR_BASE_URL
  const upper = service.replace(/[^A-Za-z0-9]/g, "_").toUpperCase();
  return import.meta.env[`VITE_${upper}_BASE_URL`] as string | undefined;
};

export const resolveTransportBaseUrl = () => import.meta.env.VITE_TRANSPORT_BASE_URL || defaultTransportBase;

export const resolveServiceBaseUrl = (service: string) => {
  // prefer explicit per-service env var, then fall back to transport gateway
  const explicit = envBaseFor(service);
  if (explicit) return explicit;
  if (service === "identity" && import.meta.env.DEV) {
    return "http://localhost:8085";
  }
  return resolveTransportBaseUrl();
};

export const buildCoreServiceUrl = (service: string, path: string, baseUrl?: string) => {
  const base = baseUrl || resolveServiceBaseUrl(service);
  const normalisedBase = base.replace(/\/$/, "");
  const normalisedService = sanitisePath(service).replace(/\/$/, "");
  const normalisedPath = path ? `/${sanitisePath(path)}` : "";
  const isAbsoluteBase = /^https?:\/\//i.test(normalisedBase);
  if (isAbsoluteBase && service === "identity") {
    return `${normalisedBase}${normalisedPath}`;
  }
  // If base already points to a specific service root, avoid duplicating service in path.
  if (normalisedBase.endsWith(`/${normalisedService}`)) {
    return `${normalisedBase}${normalisedPath}`;
  }
  return `${normalisedBase}/${normalisedService}${normalisedPath}`;
};

export const fetchCoreService = async <T>(
  service: string,
  path: string,
  signal?: AbortSignal,
  baseUrl?: string
): Promise<T> => {
  const url = buildCoreServiceUrl(service, path, baseUrl);
  const response = await fetch(url, {
    method: "GET",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-Forwarded-Proto": "https",
    },
    signal,
  });

  if (!response.ok) {
    throw new Error(`${service} service unavailable (${response.status})`);
  }

  return response.json() as Promise<T>;
};
