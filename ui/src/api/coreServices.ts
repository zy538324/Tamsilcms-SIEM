// Centralised helper to connect UI pages to core-services through the transport gateway.
const defaultBaseUrl = "/transport";

// Allow runtime overrides for different environments (e.g. Docker, Cloud Run).
export const resolveTransportBaseUrl = () =>
  import.meta.env.VITE_TRANSPORT_BASE_URL || defaultBaseUrl;

// Guard against accidental double slashes and untrusted path inputs.
const sanitisePath = (path: string) => path.replace(/^\/+/, "");

// Build a transport-aware URL for a core-service endpoint.
export const buildCoreServiceUrl = (service: string, path: string, baseUrl = defaultBaseUrl) => {
  const normalisedBase = baseUrl.replace(/\/$/, "");
  const normalisedService = sanitisePath(service).replace(/\/$/, "");
  const normalisedPath = path ? `/${sanitisePath(path)}` : "";
  return `${normalisedBase}/${normalisedService}${normalisedPath}`;
};

// Fetch helper with secure defaults (HTTPS enforcement header and cookies).
export const fetchCoreService = async <T>(
  service: string,
  path: string,
  signal?: AbortSignal,
  baseUrl = defaultBaseUrl
): Promise<T> => {
  const response = await fetch(buildCoreServiceUrl(service, path, baseUrl), {
    method: "GET",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-Forwarded-Proto": "https"
    },
    signal
  });

  if (!response.ok) {
    throw new Error(`${service} service unavailable (${response.status})`);
  }

  return response.json() as Promise<T>;
};
