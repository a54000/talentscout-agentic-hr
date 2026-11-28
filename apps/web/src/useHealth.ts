import { useEffect, useState } from "react";

export type ServiceStatus = "checking" | "ok" | "down";

/** Polls a health endpoint once on mount. Replaced by TanStack Query in Sprint 1. */
export function useHealth(url: string, fetcher: typeof fetch = fetch): ServiceStatus {
  const [status, setStatus] = useState<ServiceStatus>("checking");
  useEffect(() => {
    let cancelled = false;
    fetcher(url)
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
      .then((body: { status?: string }) => !cancelled && setStatus(body.status === "ok" ? "ok" : "down"))
      .catch(() => !cancelled && setStatus("down"));
    return () => {
      cancelled = true;
    };
  }, [url, fetcher]);
  return status;
}
