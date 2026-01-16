import crypto from "crypto";
import { config } from "./config.js";

const ITERATIONS = 200_000;
const KEY_LENGTH = 32;
const DIGEST = "sha256";

export const hashApiKey = (apiKey: string): string => {
  const salt = crypto.randomBytes(16).toString("hex");
  const digest = crypto.pbkdf2Sync(`${apiKey}${config.apiKeyPepper}`, salt, ITERATIONS, KEY_LENGTH, DIGEST);
  return `pbkdf2_sha256$${ITERATIONS}$${salt}$${digest.toString("hex")}`;
};

export const verifyApiKey = (apiKey: string, storedHash: string): boolean => {
  const parts = storedHash.split("$");
  if (parts.length !== 4) {
    return false;
  }

  const [, iterations, salt, hash] = parts;
  if (Number(iterations) !== ITERATIONS) {
    return false;
  }

  const digest = crypto.pbkdf2Sync(`${apiKey}${config.apiKeyPepper}`, salt, ITERATIONS, KEY_LENGTH, DIGEST);
  return crypto.timingSafeEqual(Buffer.from(hash, "hex"), digest);
};
