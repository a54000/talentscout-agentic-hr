import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { App } from "./App";

const respond = (body: unknown, ok = true) =>
  vi.fn().mockResolvedValue({ ok, status: ok ? 200 : 503, json: async () => body }) as unknown as typeof fetch;

describe("App", () => {
  it("shows the API as online when health is ok", async () => {
    render(<App fetcher={respond({ status: "ok" })} />);
    expect(await screen.findByText("Online")).toBeInTheDocument();
  });

  it("shows the API as offline when the health call fails", async () => {
    render(<App fetcher={respond({}, false)} />);
    expect(await screen.findByText("Offline")).toBeInTheDocument();
  });
});
