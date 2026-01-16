import Fastify from "fastify";
import cors from "@fastify/cors";
import helmet from "@fastify/helmet";
import rateLimit from "@fastify/rate-limit";

import { config } from "./config.js";
import { registerAgentRoutes } from "./routes/agents.js";
import { registerLogRoutes } from "./routes/logs.js";
import { registerIngestRoutes } from "./routes/ingest.js";

const app = Fastify({ logger: { level: config.logLevel } });

await app.register(cors, {
  origin: [config.dashboardOrigin],
  methods: ["GET", "POST"],
});

await app.register(helmet, { global: true });
await app.register(rateLimit, { max: 120, timeWindow: "1 minute" });

app.get("/health", async () => ({ status: "ok" }));

await app.register(registerIngestRoutes, { prefix: "/api/v1" });
await app.register(registerAgentRoutes, { prefix: "/api/v1" });
await app.register(registerLogRoutes, { prefix: "/api/v1" });

app.setErrorHandler((error, _request, reply) => {
  app.log.error(error);
  reply.status(500).send({ error: "Internal server error" });
});

app.listen({ port: config.port, host: "0.0.0.0" });
