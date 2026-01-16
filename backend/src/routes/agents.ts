import { FastifyInstance, FastifyReply, FastifyRequest } from "fastify";

import { pool } from "../db.js";

interface AgentsRequest extends FastifyRequest {
  Querystring: {
    limit?: string;
    offset?: string;
  };
}

export const registerAgentRoutes = async (app: FastifyInstance) => {
  app.get("/agents", async (request: AgentsRequest, reply: FastifyReply) => {
    const limit = Math.min(Number(request.query.limit || 50), 200);
    const offset = Math.max(Number(request.query.offset || 0), 0);

    const result = await pool.query(
      `SELECT agents.id,
              agents.hostname,
              agents.os_type,
              agents.os_version,
              agents.created_at,
              MAX(logs.received_at) AS last_seen,
              COUNT(logs.id) AS log_count
       FROM agents
       LEFT JOIN logs ON logs.agent_id = agents.id
       GROUP BY agents.id
       ORDER BY last_seen DESC NULLS LAST, agents.created_at DESC
       LIMIT $1 OFFSET $2`,
      [limit, offset]
    );

    return reply.send(result.rows);
  });
};
