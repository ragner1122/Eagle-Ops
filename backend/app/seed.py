from sqlalchemy.orm import Session

from .models import User, Ticket, TicketNote, Runbook, KnowledgeArticle, TelemetryMetric
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
            status="In Progress",
            severity="High",
            sla_status="At Risk",
            assignee_id=analyst.id,
        ),
        Ticket(
            title="Billing portal intermittent 500s",
            description="Spike in 500s during peak load. Needs triage.",
            status="New",
            severity="Medium",
            sla_status="On Track",
            assignee_id=admin.id,
        ),
        Ticket(
            title="Customer cannot reset MFA",
            description="Reset flow errors after token rotation. Needs manual reset.",
            status="Waiting Client",
            severity="Low",
            sla_status="On Track",
            assignee_id=analyst.id,
        ),
        Ticket(
            title="Priority escalation: outage in APAC",
            description="APAC customers report service outage. War room active.",
            status="Resolved",
            severity="Critical",
            sla_status="Breached",
            assignee_id=admin.id,
        ),
    ]

    runbooks = [
        Runbook(
            title="Database latency triage",
            project_type="Database tuning",
            client="Northwind Health",
            site="us-east-1",
            version="v14.2",
            window="02:00-04:00 UTC",
            rollback_plan_required=True,
            pre_check="Confirm replica lag metrics and capture slow query samples.",
            steps="1. Scale read replicas. 2. Apply index updates. 3. Notify DBA for review.",
            rollback="Revert indexing changes and restore replica count if latency persists.",
            validation="Monitor query latency for 30 minutes and verify read pool health.",
            comms="Update #db-ops and send summary to client stakeholders.",
            owner="SRE Team",
        ),
        Runbook(
            title="Customer escalation workflow",
            project_type="Escalation process",
            client="Globex Retail",
            site="eu-west-2",
            version="v3.9",
            window="Business hours",
            rollback_plan_required=False,
            pre_check="Confirm escalation criteria and ticket severity with support lead.",
            steps="1. Capture impact. 2. Assign owner. 3. Provide ETA updates.",
            rollback="No rollback required; document follow-up actions.",
            validation="Ensure stakeholder updates are logged and ticket status is updated.",
            comms="Post updates in escalation channel and email client liaison.",
            owner="Support Ops",
        ),
    ]

    articles = [
        KnowledgeArticle(
            title="Resetting MFA for locked accounts",
            content="Guide for safely resetting MFA tokens, confirming identity, and documenting the reset.",
            tags="auth,accounts,mfa",
            created_by=admin.email,
        ),
        KnowledgeArticle(
            title="Tracking incident status updates",
            content="How to post timeline updates in the incident channel and share stakeholder comms.",
            tags="incident,communications",
            created_by=analyst.email,
        ),
    ]

    telemetry = [
        TelemetryMetric(name="Queue backlog", value="42 tickets", status="Warning"),
        TelemetryMetric(name="First response SLA", value="98%", status="Healthy"),
        TelemetryMetric(name="API uptime", value="99.95%", status="Healthy"),
    ]

    db.add_all(tickets + runbooks + articles + telemetry)
    db.flush()

    notes = [
        TicketNote(
            ticket_id=tickets[0].id,
            body="Gathered traceroutes from EU region; escalating to network team.",
            author=analyst.email,
        ),
        TicketNote(
            ticket_id=tickets[1].id,
            body="Waiting on billing service logs from engineering.",
            author=admin.email,
        ),
        TicketNote(
            ticket_id=tickets[3].id,
            body="Confirmed mitigation deployed. Monitoring for 30 minutes.",
            author=admin.email,
        ),
    ]
    db.add_all(notes)
    db.commit()
