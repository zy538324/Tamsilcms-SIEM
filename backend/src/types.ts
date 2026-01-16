import { z } from "zod";

export const logEventSchema = z.object({
  agent_id: z.string().uuid(),
  hostname: z.string().min(1).max(255),
  os_type: z.string().min(1).max(50),
  os_version: z.string().min(1).max(100),
  log_source: z.string().min(1).max(255),
  event_time: z.string().datetime({ offset: true }),
  event_level: z.string().min(1).max(20),
  event_id: z.string().min(1).max(50),
  message: z.string().min(1).max(4000),
});

export const ingestPayloadSchema = z.object({
  agent_id: z.string().uuid(),
  events: z.array(logEventSchema).min(1).max(500),
});

export type IngestPayload = z.infer<typeof ingestPayloadSchema>;
