const highlights = [
  { label: "Active tickets", value: "24", note: "6 need escalation" },
  { label: "SLA compliance", value: "98%", note: "Last 7 days" },
  { label: "Queue backlog", value: "42", note: "+8 since yesterday" },
  { label: "CSAT", value: "4.7/5", note: "Trailing 30 days" }
];

const tickets = [
  {
    title: "VPN access failing for field team",
    detail: "EU region timeouts reported",
    status: "Open",
    priority: "High"
  },
  {
    title: "Billing portal intermittent 500s",
    detail: "Spike during peak load",
    status: "Investigating",
    priority: "Medium"
  }
];

const runbooks = [
  {
    title: "Database latency triage",
    detail: "Scale read replicas & check slow queries"
  },
  {
    title: "Customer escalation workflow",
    detail: "Capture impact, assign owner, post ETA"
  }
];

const knowledge = [
  {
    title: "Resetting MFA for locked accounts",
    detail: "Verify identity, rotate token, confirm login"
  },
  {
    title: "Tracking incident status updates",
    detail: "Post timeline updates every 30 minutes"
  }
];

const telemetry = [
  { name: "API uptime", value: "99.95%", status: "Healthy" },
  { name: "First response SLA", value: "98%", status: "Healthy" },
  { name: "Queue backlog", value: "42 tickets", status: "Warning" }
];

export default function Home() {
  return (
    <main>
      <header>
        <div>
          <h1>EAGLE SupportOps</h1>
          <p>Tier-1 support operations command center</p>
        </div>
        <span className="badge">Enterprise Light</span>
      </header>

      <section className="grid">
        {highlights.map((item) => (
          <div className="card" key={item.label}>
            <h3>{item.label}</h3>
            <p style={{ fontSize: "22px", fontWeight: 700 }}>{item.value}</p>
            <p>{item.note}</p>
          </div>
        ))}
      </section>

      <section className="section">
        <h2>Ticketing &amp; Triage</h2>
        <div className="list">
          {tickets.map((ticket) => (
            <div className="list-item" key={ticket.title}>
              <h4>{ticket.title}</h4>
              <p>{ticket.detail}</p>
              <p>
                <strong>Status:</strong> {ticket.status} · <strong>Priority:</strong>{" "}
                {ticket.priority}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="section">
        <h2>Runbooks</h2>
        <div className="list">
          {runbooks.map((runbook) => (
            <div className="list-item" key={runbook.title}>
              <h4>{runbook.title}</h4>
              <p>{runbook.detail}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="section">
        <h2>Knowledge Base</h2>
        <div className="list">
          {knowledge.map((article) => (
            <div className="list-item" key={article.title}>
              <h4>{article.title}</h4>
              <p>{article.detail}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="section">
        <h2>Telemetry Dashboard</h2>
        <div className="grid">
          {telemetry.map((metric) => (
            <div className="card" key={metric.name}>
              <h3>{metric.name}</h3>
              <p style={{ fontSize: "18px", fontWeight: 600 }}>{metric.value}</p>
              <p>{metric.status}</p>
            </div>
          ))}
        </div>
      </section>

      <footer>
        Seed demo data available via the FastAPI backend. Login with
        admin@eagleops.io / AdminPass123 or analyst@eagleops.io / AnalystPass123.
      </footer>
    </main>
  );
}
