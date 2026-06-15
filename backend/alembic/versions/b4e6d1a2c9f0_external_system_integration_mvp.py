"""external system integration mvp

Revision ID: b4e6d1a2c9f0
Revises: 9c1f2a7b8d3e
Create Date: 2026-06-02 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b4e6d1a2c9f0"
down_revision: Union[str, Sequence[str], None] = "9c1f2a7b8d3e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "external_event_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("source_system", sa.String(length=100), nullable=False),
        sa.Column("event_id", sa.String(length=100), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("schema_version", sa.String(length=20), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column(
            "processed_status",
            sa.Enum("pending", "processing", "success", "failed", name="external_event_status"),
            nullable=False,
        ),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("retry_count", sa.Integer(), nullable=False),
        sa.Column("related_entity_type", sa.String(length=100), nullable=True),
        sa.Column("related_entity_id", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_external_event_logs")),
        sa.UniqueConstraint("source_system", "event_id", name="uq_external_event_logs_source_event"),
    )
    op.create_index(
        "ix_external_event_logs_event_type", "external_event_logs", ["event_type"], unique=False
    )
    op.create_index(
        "ix_external_event_logs_processed_status",
        "external_event_logs",
        ["processed_status"],
        unique=False,
    )
    op.create_index(
        "ix_external_event_logs_received_at",
        "external_event_logs",
        ["received_at"],
        unique=False,
    )

    op.create_table(
        "stream_sessions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("camera_id", sa.Integer(), nullable=False),
        sa.Column("stream_type", sa.String(length=20), nullable=False),
        sa.Column("path", sa.String(length=255), nullable=False),
        sa.Column("playback_url", sa.Text(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("starting", "running", "stopped", "failed", name="stream_session_status"),
            nullable=False,
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_accessed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("stopped_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["camera_id"],
            ["cameras.id"],
            name=op.f("fk_stream_sessions_camera_id_cameras"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_stream_sessions")),
    )
    op.create_index("ix_stream_sessions_camera_id", "stream_sessions", ["camera_id"], unique=False)
    op.create_index(
        "ix_stream_sessions_last_accessed_at", "stream_sessions", ["last_accessed_at"], unique=False
    )
    op.create_index("ix_stream_sessions_status", "stream_sessions", ["status"], unique=False)

    op.create_table(
        "cctv_command_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("camera_id", sa.Integer(), nullable=True),
        sa.Column("nvr_id", sa.Integer(), nullable=True),
        sa.Column("command_type", sa.String(length=50), nullable=False),
        sa.Column("request_payload", sa.JSON(), nullable=True),
        sa.Column("response_payload", sa.JSON(), nullable=True),
        sa.Column("status", sa.Enum("success", "failed", name="cctv_command_status"), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("requested_by", sa.Integer(), nullable=True),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["camera_id"],
            ["cameras.id"],
            name=op.f("fk_cctv_command_logs_camera_id_cameras"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["nvr_id"],
            ["nvrs.id"],
            name=op.f("fk_cctv_command_logs_nvr_id_nvrs"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["requested_by"],
            ["users.id"],
            name=op.f("fk_cctv_command_logs_requested_by_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cctv_command_logs")),
    )
    op.create_index("ix_cctv_command_logs_camera_id", "cctv_command_logs", ["camera_id"], unique=False)
    op.create_index(
        "ix_cctv_command_logs_command_type", "cctv_command_logs", ["command_type"], unique=False
    )
    op.create_index("ix_cctv_command_logs_nvr_id", "cctv_command_logs", ["nvr_id"], unique=False)
    op.create_index(
        "ix_cctv_command_logs_requested_at", "cctv_command_logs", ["requested_at"], unique=False
    )
    op.create_index("ix_cctv_command_logs_status", "cctv_command_logs", ["status"], unique=False)

    op.add_column("ai_models", sa.Column("file_path", sa.String(length=500), nullable=True))
    op.add_column("ai_models", sa.Column("file_size_bytes", sa.BigInteger(), nullable=True))
    op.add_column("ai_models", sa.Column("mAP", sa.Numeric(precision=6, scale=4), nullable=True))
    op.add_column("ai_models", sa.Column("precision", sa.Numeric(precision=6, scale=4), nullable=True))
    op.add_column("ai_models", sa.Column("recall", sa.Numeric(precision=6, scale=4), nullable=True))
    op.add_column(
        "ai_models",
        sa.Column("is_deployed", sa.Boolean(), server_default=sa.false(), nullable=False),
    )
    op.add_column("ai_models", sa.Column("trained_at", sa.DateTime(timezone=True), nullable=True))

    op.add_column(
        "training_jobs",
        sa.Column("progress", sa.Integer(), server_default="0", nullable=False),
    )
    op.add_column("training_jobs", sa.Column("external_job_id", sa.String(length=100), nullable=True))
    op.add_column("training_jobs", sa.Column("source_system", sa.String(length=100), nullable=True))
    op.add_column("training_jobs", sa.Column("raw_events", sa.JSON(), nullable=True))
    op.create_index(
        "ix_training_jobs_external_job_id", "training_jobs", ["external_job_id"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_training_jobs_external_job_id", table_name="training_jobs")
    op.drop_column("training_jobs", "raw_events")
    op.drop_column("training_jobs", "source_system")
    op.drop_column("training_jobs", "external_job_id")
    op.drop_column("training_jobs", "progress")

    op.drop_column("ai_models", "trained_at")
    op.drop_column("ai_models", "is_deployed")
    op.drop_column("ai_models", "recall")
    op.drop_column("ai_models", "precision")
    op.drop_column("ai_models", "mAP")
    op.drop_column("ai_models", "file_size_bytes")
    op.drop_column("ai_models", "file_path")

    op.drop_index("ix_cctv_command_logs_status", table_name="cctv_command_logs")
    op.drop_index("ix_cctv_command_logs_requested_at", table_name="cctv_command_logs")
    op.drop_index("ix_cctv_command_logs_nvr_id", table_name="cctv_command_logs")
    op.drop_index("ix_cctv_command_logs_command_type", table_name="cctv_command_logs")
    op.drop_index("ix_cctv_command_logs_camera_id", table_name="cctv_command_logs")
    op.drop_table("cctv_command_logs")

    op.drop_index("ix_stream_sessions_status", table_name="stream_sessions")
    op.drop_index("ix_stream_sessions_last_accessed_at", table_name="stream_sessions")
    op.drop_index("ix_stream_sessions_camera_id", table_name="stream_sessions")
    op.drop_table("stream_sessions")

    op.drop_index("ix_external_event_logs_received_at", table_name="external_event_logs")
    op.drop_index("ix_external_event_logs_processed_status", table_name="external_event_logs")
    op.drop_index("ix_external_event_logs_event_type", table_name="external_event_logs")
    op.drop_table("external_event_logs")
