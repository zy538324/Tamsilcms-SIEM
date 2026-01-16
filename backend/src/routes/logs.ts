import { FastifyInstance, FastifyReply, FastifyRequest } from "fastify";

import { pool } from "../db.js";

interface LogsRequest extends FastifyRequest {
  Querystring: {
    agent_id?: string;
    log_source?: string;
    event_level?: string;
    search?: string;
    start_time?: string;
    end_time?: string;
    limit?: string;
    offset?: string;
  };
}

export const registerLogRoutes = async (app: FastifyInstance) => {
  app.get("/logs", async (request: LogsRequest, reply: FastifyReply) => {
    const limit = Math.min(Number(request.query.limit || 100), 500);
    const offset = Math.max(Number(request.query.offset || 0), 0);

    const filters: string[] = [];
    const values: Array<string | number> = [];

    if (request.query.agent_id) {
      values.push(request.query.agent_id);
      filters.push(`agent_id = $${values.length}`);
    }
    if (request.query.log_source) {
      values.push(request.query.log_source);
      filters.push(`log_source = $${values.length}`);
    }
    if (request.query.event_level) {
      values.push(request.query.event_level.toUpperCase());
      filters.push(`event_level = $${values.length}`);
    }
    if (request.query.search) {
      values.push(`%${request.query.search}%`);
      filters.push(`message ILIKE $${values.length}`);
    }
    if (request.query.start_time) {
      values.push(request.query.start_time);
      filters.push(`event_time >= $${values.length}`);
    }
    if (request.query.end_time) {
      values.push(request.query.end_time);
      filters.push(`event_time <= $${values.length}`);
    }

    values.push(limit, offset);

    const whereClause = filters.length ? `WHERE ${filters.join(" AND ")}` : "";

    const result = await pool.query(
      `SELECT id, agent_id, log_source, event_time, received_at, event_level, event_id, message
       FROM logs
       ${whereClause}
       ORDER BY event_time DESC
       LIMIT $${values.length - 1} OFFSET $${values.length}`,
      values
    );

    return reply.send(result.rows);
  });
};
