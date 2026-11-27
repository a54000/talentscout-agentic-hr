import request from "supertest";
import { describe, expect, it } from "vitest";
import { createApp } from "../src/app.js";
import { loadConfig } from "../src/config.js";

const app = createApp(loadConfig({ NODE_ENV: "test", LOG_LEVEL: "silent" }));

describe("api skeleton", () => {
  it("reports health", async () => {
    const res = await request(app).get("/api/v1/health");
    expect(res.status).toBe(200);
    expect(res.body).toMatchObject({ status: "ok", service: "api" });
  });

  it("sets security headers and hides the framework", async () => {
    const res = await request(app).get("/api/v1/health");
    expect(res.headers["x-powered-by"]).toBeUndefined();
    expect(res.headers["x-content-type-options"]).toBe("nosniff");
  });

  it("returns problem+json for unknown routes", async () => {
    const res = await request(app).get("/api/v1/does-not-exist");
    expect(res.status).toBe(404);
    expect(res.headers["content-type"]).toContain("application/problem+json");
    expect(res.body).toMatchObject({ status: 404, title: "Not Found" });
  });

  it("rejects invalid configuration at startup", () => {
    expect(() => loadConfig({ PORT: "not-a-number" })).toThrow();
  });
});
