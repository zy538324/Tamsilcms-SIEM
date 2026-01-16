import dotenv from "dotenv";

dotenv.config();

export const config = {
  port: Number(process.env.PORT || 8080),
  databaseUrl: process.env.DATABASE_URL || "",
  dashboardOrigin: process.env.DASHBOARD_ORIGIN || "http://localhost:8000",
  apiKeyPepper: process.env.API_KEY_PEPPER || "",
  logLevel: process.env.LOG_LEVEL || "info",
};

if (!config.databaseUrl) {
  throw new Error("DATABASE_URL is required");
}

if (!config.apiKeyPepper) {
  throw new Error("API_KEY_PEPPER is required");
}
