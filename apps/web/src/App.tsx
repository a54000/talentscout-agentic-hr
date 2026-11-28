import { useHealth, type ServiceStatus } from "./useHealth";

const label: Record<ServiceStatus, string> = { checking: "Checking…", ok: "Online", down: "Offline" };

export function App({ fetcher }: { fetcher?: typeof fetch }) {
  const api = useHealth("/api/v1/health", fetcher);
  return (
    <main className="shell">
      <header>
        <h1>TalentScout</h1>
        <p className="tagline">Agentic Recruitment Command Centre</p>
      </header>
      <section aria-labelledby="status-heading" className="card">
        <h2 id="status-heading">Platform status</h2>
        <dl>
          <dt>API</dt>
          <dd data-status={api}>{label[api]}</dd>
        </dl>
        <p className="note">Walking skeleton (Sprint 0). Requirement intake arrives in Sprint 1.</p>
      </section>
    </main>
  );
}
