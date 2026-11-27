import cors from "cors";
import express from "express";
import rateLimit from "express-rate-limit";
import helmet from "helmet";
import { pinoHttp } from "pino-http";
import type { Config } from "./config.js";
import { errorHandler, notFound } from "./middleware/errors.js";
import { healthRouter } from "./routes/health.js";

export function createApp(config: Config) {
  const app = express();
  app.disable("x-powered-by");
  app.use(helmet());
  app.use(cors({ origin: config.CORS_ORIGINS.split(",").map((o) => o.trim()), credentials: true }));
  app.use(express.json({ limit: "200kb" }));
  app.use(pinoHttp({ level: config.LOG_LEVEL, redact: ["req.headers.authorization", "req.headers.cookie"] }));
  app.use("/api", rateLimit({ windowMs: 60_000, limit: 120, standardHeaders: "draft-8", legacyHeaders: false }));

  app.use("/api/v1/health", healthRouter);

  app.use(notFound);
  app.use(errorHandler);
  return app;
}
