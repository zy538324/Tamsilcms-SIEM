import type { Asset } from "../data/assets";
import { fetchAgents, fetchRiskScores } from "./identity";
import { formatRelativeTime, mapRiskScoreToCriticality } from "../utils/formatters";

// Build asset records by combining identity agents with risk scores.
export const fetchAssets = async (signal?: AbortSignal): Promise<Asset[]> => {
  const [agents, riskScores] = await Promise.all([
    fetchAgents(signal),
    fetchRiskScores(signal)
  ]);

  const riskScoreMap = new Map(riskScores.map((score) => [score.identity_id, score.score]));

  return agents.map((agent) => {
    const score = Math.round(riskScoreMap.get(agent.identity_id) ?? 0);
    return {
      id: agent.identity_id,
      name: agent.hostname || agent.identity_id,
      role: agent.os || "Managed Agent",
      criticality: mapRiskScoreToCriticality(score),
      riskScore: score,
      lastSeen: formatRelativeTime(agent.last_seen_at),
      owner: agent.trust_state === "trusted" ? "Security" : "Identity Ops"
    };
  });
};
