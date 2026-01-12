"use client";

import { useEffect, useMemo, useState, type FormEvent } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

const statusOptions = ["New", "In Progress", "Waiting Client", "Resolved"] as const;
const severityOptions = ["Low", "Medium", "High", "Critical"] as const;
const slaOptions = ["On Track", "At Risk", "Breached"] as const;

interface User {
  id: number;
  email: string;
  role: string;
}

interface TicketNote {
  id: number;
  body: string;
  author: string;
  created_at: string;
}

interface Ticket {
  id: number;
  title: string;
  description: string;
  status: (typeof statusOptions)[number];
  severity: (typeof severityOptions)[number];
  sla_status: (typeof slaOptions)[number];
  created_at: string;
  updated_at: string;
  assignee_id: number | null;
  assignee: User | null;
}

interface TicketDetail extends Ticket {
  notes: TicketNote[];
}

const highlights = [
  { label: "Active tickets", value: "24", note: "6 need escalation" },
  { label: "SLA compliance", value: "98%", note: "Last 7 days" },
  { label: "Queue backlog", value: "42", note: "+8 since yesterday" },
  { label: "CSAT", value: "4.7/5", note: "Trailing 30 days" }
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
  const [token, setToken] = useState<string | null>(null);
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [selectedTicket, setSelectedTicket] = useState<TicketDetail | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [newTicket, setNewTicket] = useState({
    title: "",
    description: "",
    status: "New",
    severity: "Medium",
    sla_status: "On Track",
    assignee_id: ""
  });

  const [noteBody, setNoteBody] = useState("");

  useEffect(() => {
    const authenticate = async () => {
      try {
        const params = new URLSearchParams();
        params.append("username", "admin@eagleops.io");
        params.append("password", "AdminPass123");
        const response = await fetch(`${API_BASE}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: params
        });
        if (!response.ok) {
          throw new Error("Unable to authenticate against the API.");
        }
        const data = await response.json();
        setToken(data.access_token);
      } catch (authError) {
        setError(
          authError instanceof Error ? authError.message : "Unable to reach API."
        );
        setLoading(false);
      }
    };

    authenticate();
  }, []);

  const fetchTickets = async (authToken: string) => {
    const response = await fetch(`${API_BASE}/tickets/`, {
      headers: { Authorization: `Bearer ${authToken}` }
    });
    if (!response.ok) {
      throw new Error("Unable to fetch tickets.");
    }
    return response.json();
  };

  const fetchUsers = async (authToken: string) => {
    const response = await fetch(`${API_BASE}/users/`, {
      headers: { Authorization: `Bearer ${authToken}` }
    });
    if (!response.ok) {
      throw new Error("Unable to fetch users.");
    }
    return response.json();
  };

  const fetchTicketDetail = async (ticketId: number, authToken: string) => {
    const response = await fetch(`${API_BASE}/tickets/${ticketId}`, {
      headers: { Authorization: `Bearer ${authToken}` }
    });
    if (!response.ok) {
      throw new Error("Unable to fetch ticket details.");
    }
    return response.json();
  };

  useEffect(() => {
    if (!token) {
      return;
    }

    const load = async () => {
      try {
        setLoading(true);
        const [ticketData, userData] = await Promise.all([
          fetchTickets(token),
          fetchUsers(token)
        ]);
        setTickets(ticketData);
        setUsers(userData);
        if (ticketData.length > 0) {
          const detail = await fetchTicketDetail(ticketData[0].id, token);
          setSelectedTicket(detail);
        } else {
          setSelectedTicket(null);
        }
      } catch (loadError) {
        setError(loadError instanceof Error ? loadError.message : "Failed to load.");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [token]);

  const selectTicket = async (ticketId: number) => {
    if (!token) {
      return;
    }
    try {
      setLoading(true);
      const detail = await fetchTicketDetail(ticketId, token);
      setSelectedTicket(detail);
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "Failed to load.");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTicket = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!token) {
      return;
    }

    const payload = {
      title: newTicket.title,
      description: newTicket.description,
      status: newTicket.status,
      severity: newTicket.severity,
      sla_status: newTicket.sla_status,
      assignee_id: newTicket.assignee_id ? Number(newTicket.assignee_id) : null
    };

    const response = await fetch(`${API_BASE}/tickets/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      setError("Failed to create ticket.");
      return;
    }

    const created = await response.json();
    const refreshed = await fetchTickets(token);
    setTickets(refreshed);
    setNewTicket({
      title: "",
      description: "",
      status: "New",
      severity: "Medium",
      sla_status: "On Track",
      assignee_id: ""
    });
    await selectTicket(created.id);
  };

  const handleUpdateTicket = async () => {
    if (!token || !selectedTicket) {
      return;
    }
    const response = await fetch(`${API_BASE}/tickets/${selectedTicket.id}`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        status: selectedTicket.status,
        severity: selectedTicket.severity,
        sla_status: selectedTicket.sla_status,
        assignee_id: selectedTicket.assignee_id
      })
    });

    if (!response.ok) {
      setError("Failed to update ticket.");
      return;
    }

    const refreshed = await fetchTickets(token);
    setTickets(refreshed);
    await selectTicket(selectedTicket.id);
  };

  const handleAddNote = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!token || !selectedTicket || !noteBody.trim()) {
      return;
    }
    const response = await fetch(`${API_BASE}/tickets/${selectedTicket.id}/notes`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ body: noteBody })
    });

    if (!response.ok) {
      setError("Failed to add note.");
      return;
    }

    setNoteBody("");
    await selectTicket(selectedTicket.id);
  };

  const activeCount = useMemo(
    () => tickets.filter((ticket) => ticket.status !== "Resolved").length,
    [tickets]
  );

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
        <div className="section-header">
          <div>
            <h2>Tickets</h2>
            <p className="section-subtitle">
              {activeCount} active tickets · data synced to FastAPI backend
            </p>
          </div>
          {loading && <span className="status-pill">Loading...</span>}
          {error && <span className="status-pill warning">{error}</span>}
        </div>

        <div className="ticket-grid">
          <div className="ticket-panel">
            <h3>Queue</h3>
            <div className="ticket-list">
              {tickets.map((ticket) => (
                <button
                  key={ticket.id}
                  className={`ticket-card ${
                    selectedTicket?.id === ticket.id ? "active" : ""
                  }`}
                  onClick={() => selectTicket(ticket.id)}
                  type="button"
                >
                  <div>
                    <h4>{ticket.title}</h4>
                    <p>{ticket.description}</p>
                  </div>
                  <div className="ticket-meta">
                    <span className={`status-pill ${ticket.status.replace(/\s+/g, "-")}`}>
                      {ticket.status}
                    </span>
                    <span className="status-pill outline">{ticket.severity}</span>
                    <span className={`status-pill sla ${ticket.sla_status.replace(/\s+/g, "-")}`}>
                      {ticket.sla_status}
                    </span>
                  </div>
                </button>
              ))}
              {tickets.length === 0 && !loading && (
                <p className="empty-state">No tickets available yet.</p>
              )}
            </div>
          </div>

          <div className="ticket-panel">
            <h3>Create ticket</h3>
            <form className="form" onSubmit={handleCreateTicket}>
              <label>
                Title
                <input
                  value={newTicket.title}
                  onChange={(event) =>
                    setNewTicket((prev) => ({ ...prev, title: event.target.value }))
                  }
                  placeholder="Short summary"
                  required
                />
              </label>
              <label>
                Description
                <textarea
                  rows={4}
                  value={newTicket.description}
                  onChange={(event) =>
                    setNewTicket((prev) => ({
                      ...prev,
                      description: event.target.value
                    }))
                  }
                  placeholder="Customer impact and key details"
                  required
                />
              </label>
              <div className="form-row">
                <label>
                  Status
                  <select
                    value={newTicket.status}
                    onChange={(event) =>
                      setNewTicket((prev) => ({
                        ...prev,
                        status: event.target.value as (typeof statusOptions)[number]
                      }))
                    }
                  >
                    {statusOptions.map((option) => (
                      <option key={option} value={option}>
                        {option}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  Severity
                  <select
                    value={newTicket.severity}
                    onChange={(event) =>
                      setNewTicket((prev) => ({
                        ...prev,
                        severity: event.target.value as (typeof severityOptions)[number]
                      }))
                    }
                  >
                    {severityOptions.map((option) => (
                      <option key={option} value={option}>
                        {option}
                      </option>
                    ))}
                  </select>
                </label>
              </div>
              <div className="form-row">
                <label>
                  SLA
                  <select
                    value={newTicket.sla_status}
                    onChange={(event) =>
                      setNewTicket((prev) => ({
                        ...prev,
                        sla_status: event.target.value as (typeof slaOptions)[number]
                      }))
                    }
                  >
                    {slaOptions.map((option) => (
                      <option key={option} value={option}>
                        {option}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  Assignee
                  <select
                    value={newTicket.assignee_id}
                    onChange={(event) =>
                      setNewTicket((prev) => ({
                        ...prev,
                        assignee_id: event.target.value
                      }))
                    }
                  >
                    <option value="">Unassigned</option>
                    {users.map((user) => (
                      <option key={user.id} value={user.id}>
                        {user.email} ({user.role})
                      </option>
                    ))}
                  </select>
                </label>
              </div>
              <button className="primary" type="submit">
                Create ticket
              </button>
            </form>
          </div>

          <div className="ticket-panel">
            <h3>Ticket detail</h3>
            {selectedTicket ? (
              <div className="detail">
                <div className="detail-header">
                  <div>
                    <h4>{selectedTicket.title}</h4>
                    <p>{selectedTicket.description}</p>
                  </div>
                  <div className="ticket-meta">
                    <span className={`status-pill ${selectedTicket.status.replace(/\s+/g, "-")}`}>
                      {selectedTicket.status}
                    </span>
                    <span className="status-pill outline">{selectedTicket.severity}</span>
                    <span
                      className={`status-pill sla ${selectedTicket.sla_status.replace(/\s+/g, "-")}`}
                    >
                      {selectedTicket.sla_status}
                    </span>
                  </div>
                </div>

                <div className="detail-body">
                  <div className="form-row">
                    <label>
                      Update status
                      <select
                        value={selectedTicket.status}
                        onChange={(event) =>
                          setSelectedTicket((prev) =>
                            prev
                              ? {
                                  ...prev,
                                  status: event.target.value as (typeof statusOptions)[number]
                                }
                              : prev
                          )
                        }
                      >
                        {statusOptions.map((option) => (
                          <option key={option} value={option}>
                            {option}
                          </option>
                        ))}
                      </select>
                    </label>
                    <label>
                      Severity
                      <select
                        value={selectedTicket.severity}
                        onChange={(event) =>
                          setSelectedTicket((prev) =>
                            prev
                              ? {
                                  ...prev,
                                  severity: event.target.value as (typeof severityOptions)[number]
                                }
                              : prev
                          )
                        }
                      >
                        {severityOptions.map((option) => (
                          <option key={option} value={option}>
                            {option}
                          </option>
                        ))}
                      </select>
                    </label>
                  </div>
                  <div className="form-row">
                    <label>
                      SLA status
                      <select
                        value={selectedTicket.sla_status}
                        onChange={(event) =>
                          setSelectedTicket((prev) =>
                            prev
                              ? {
                                  ...prev,
                                  sla_status: event.target.value as (typeof slaOptions)[number]
                                }
                              : prev
                          )
                        }
                      >
                        {slaOptions.map((option) => (
                          <option key={option} value={option}>
                            {option}
                          </option>
                        ))}
                      </select>
                    </label>
                    <label>
                      Assignee
                      <select
                        value={selectedTicket.assignee_id ?? ""}
                        onChange={(event) =>
                          setSelectedTicket((prev) =>
                            prev
                              ? {
                                  ...prev,
                                  assignee_id: event.target.value
                                    ? Number(event.target.value)
                                    : null
                                }
                              : prev
                          )
                        }
                      >
                        <option value="">Unassigned</option>
                        {users.map((user) => (
                          <option key={user.id} value={user.id}>
                            {user.email} ({user.role})
                          </option>
                        ))}
                      </select>
                    </label>
                  </div>
                  <button className="primary" type="button" onClick={handleUpdateTicket}>
                    Save updates
                  </button>
                </div>

                <div className="detail-section">
                  <h5>Timeline notes</h5>
                  <div className="notes">
                    {selectedTicket.notes.map((note) => (
                      <div className="note" key={note.id}>
                        <div>
                          <p>{note.body}</p>
                          <span>
                            {note.author} · {new Date(note.created_at).toLocaleString()}
                          </span>
                        </div>
                      </div>
                    ))}
                    {selectedTicket.notes.length === 0 && (
                      <p className="empty-state">No notes yet. Add an update below.</p>
                    )}
                  </div>
                  <form className="form" onSubmit={handleAddNote}>
                    <label>
                      Add note
                      <textarea
                        rows={3}
                        value={noteBody}
                        onChange={(event) => setNoteBody(event.target.value)}
                        placeholder="Share latest progress or customer update"
                      />
                    </label>
                    <button className="primary" type="submit">
                      Add timeline note
                    </button>
                  </form>
                </div>

                <div className="detail-section">
                  <h5>Attachments</h5>
                  <div className="attachments">
                    <p className="empty-state">
                      Attachment slots reserved. Uploads will appear here.
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <p className="empty-state">Select a ticket to view details.</p>
            )}
          </div>
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
