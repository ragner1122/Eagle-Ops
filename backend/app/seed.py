from sqlalchemy.orm import Session

from .models import User, Ticket, Runbook, KnowledgeArticle, TelemetryMetric
from .auth import hash_password


def seed_data(db: Session) -> None:
    if db.query(User).first():
        return

    admin = User(
        email="admin@eagleops.io",
        hashed_password=hash_password("AdminPass123"),
        role="Admin",
    )
    analyst = User(
        email="analyst@eagleops.io",
        hashed_password=hash_password("AnalystPass123"),
        role="Analyst",
    )
    db.add_all([admin, analyst])
    db.flush()

    tickets = [
        Ticket(
            title="VPN access failing for field team",
            description="Users report timeouts when connecting from EU region.",
            status="Open",
            priority="High",
            assignee_id=analyst.id,
        ),
        Ticket(
            title="Billing portal intermittent 500s",
            description="Spike in 500s during peak load. Needs triage.",
            status="Investigating",
            priority="Medium",
            assignee_id=admin.id,
        ),
    ]

    runbooks = [
        Runbook(
            title="Database latency triage",
            steps="1. Check slow query log. 2. Scale read replicas. 3. Notify DBA.",
            owner="SRE Team",
        ),
        Runbook(
            title="Customer escalation workflow",
            steps="1. Capture impact. 2. Assign owner. 3. Provide ETA updates.",
            owner="Support Ops",
        ),
    ]

    articles = [
        KnowledgeArticle(
            title="Resetting MFA for locked accounts",
            summary="Guide for safely resetting MFA tokens and confirming identity.",
            tags="auth,accounts,mfa",
        ),
        KnowledgeArticle(
            title="Tracking incident status updates",
            summary="How to post timeline updates in the incident channel.",
            tags="incident,communications",
        ),
    ]

    telemetry = [
        TelemetryMetric(name="Queue backlog", value="42 tickets", status="Warning"),
        TelemetryMetric(name="First response SLA", value="98%", status="Healthy"),
        TelemetryMetric(name="API uptime", value="99.95%", status="Healthy"),
    ]

    db.add_all(tickets + runbooks + articles + telemetry)
    db.commit()
