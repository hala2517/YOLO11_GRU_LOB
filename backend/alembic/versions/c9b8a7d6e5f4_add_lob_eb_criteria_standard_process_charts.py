"""add lob eb criteria and standard process charts

Revision ID: c9b8a7d6e5f4
Revises: b4e6d1a2c9f0
Create Date: 2026-06-02 14:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c9b8a7d6e5f4"
down_revision: Union[str, Sequence[str], None] = "b4e6d1a2c9f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "lob_eb_criteria",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("site_id", sa.Integer(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("line_code", sa.String(length=50), nullable=True),
        sa.Column("product_code", sa.String(length=100), nullable=True),
        sa.Column("lob_target", sa.Numeric(precision=6, scale=2), nullable=False),
        sa.Column("lob_warning", sa.Numeric(precision=6, scale=2), nullable=False),
        sa.Column("eb_target", sa.Numeric(precision=6, scale=2), nullable=False),
        sa.Column("eb_warning", sa.Numeric(precision=6, scale=2), nullable=False),
        sa.Column("takt_time_limit", sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], name=op.f("fk_lob_eb_criteria_created_by_users"), ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["site_id"], ["sites.id"], name=op.f("fk_lob_eb_criteria_site_id_sites"), ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lob_eb_criteria")),
        sa.UniqueConstraint("site_id", "line_code", "product_code", "is_active", name="uq_lob_eb_criteria_scope_active"),
    )
    op.create_index("ix_lob_eb_criteria_is_active", "lob_eb_criteria", ["is_active"], unique=False)
    op.create_index("ix_lob_eb_criteria_line_code", "lob_eb_criteria", ["line_code"], unique=False)
    op.create_index("ix_lob_eb_criteria_product_code", "lob_eb_criteria", ["product_code"], unique=False)
    op.create_index("ix_lob_eb_criteria_site_id", "lob_eb_criteria", ["site_id"], unique=False)

    op.create_table(
        "standard_process_charts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("line_code", sa.String(length=50), nullable=False),
        sa.Column("product_code", sa.String(length=100), nullable=False),
        sa.Column("product_name", sa.String(length=255), nullable=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("version", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("owner_department", sa.String(length=100), nullable=True),
        sa.Column("effective_from", sa.Date(), nullable=True),
        sa.Column("effective_to", sa.Date(), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], name=op.f("fk_standard_process_charts_created_by_users"), ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_standard_process_charts")),
        sa.UniqueConstraint("line_code", "product_code", "version", name="uq_standard_process_charts_line_product_version"),
    )
    op.create_index("ix_standard_process_charts_is_deleted", "standard_process_charts", ["is_deleted"], unique=False)
    op.create_index("ix_standard_process_charts_line_code", "standard_process_charts", ["line_code"], unique=False)
    op.create_index("ix_standard_process_charts_product_code", "standard_process_charts", ["product_code"], unique=False)
    op.create_index("ix_standard_process_charts_status", "standard_process_charts", ["status"], unique=False)

    op.create_table(
        "standard_process_chart_steps",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("chart_id", sa.Integer(), nullable=False),
        sa.Column("step_no", sa.Integer(), nullable=False),
        sa.Column("process_name", sa.String(length=200), nullable=False),
        sa.Column("worker_label", sa.String(length=100), nullable=True),
        sa.Column("standard_worker_count", sa.Integer(), nullable=True),
        sa.Column("standard_time", sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column("route_description", sa.Text(), nullable=True),
        sa.Column("machine_name", sa.String(length=200), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["chart_id"], ["standard_process_charts.id"], name=op.f("fk_standard_process_chart_steps_chart_id_standard_process_charts"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_standard_process_chart_steps")),
        sa.UniqueConstraint("chart_id", "step_no", name="uq_standard_process_chart_steps_chart_step"),
    )
    op.create_index("ix_standard_process_chart_steps_chart_id", "standard_process_chart_steps", ["chart_id"], unique=False)

    op.create_table(
        "standard_process_chart_layouts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("chart_id", sa.Integer(), nullable=False),
        sa.Column("layout_type", sa.String(length=50), nullable=False),
        sa.Column("width", sa.Integer(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False),
        sa.Column("nodes", sa.JSON(), nullable=True),
        sa.Column("edges", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["chart_id"], ["standard_process_charts.id"], name=op.f("fk_standard_process_chart_layouts_chart_id_standard_process_charts"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_standard_process_chart_layouts")),
        sa.UniqueConstraint("chart_id", "layout_type", name="uq_standard_process_chart_layouts_chart_type"),
    )
    op.create_index("ix_standard_process_chart_layouts_chart_id", "standard_process_chart_layouts", ["chart_id"], unique=False)

    op.create_table(
        "standard_process_chart_attachments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("chart_id", sa.Integer(), nullable=False),
        sa.Column("file_url", sa.String(length=1000), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=True),
        sa.Column("file_type", sa.String(length=50), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["chart_id"], ["standard_process_charts.id"], name=op.f("fk_standard_process_chart_attachments_chart_id_standard_process_charts"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_standard_process_chart_attachments")),
    )
    op.create_index("ix_standard_process_chart_attachments_chart_id", "standard_process_chart_attachments", ["chart_id"], unique=False)
    op.create_index("ix_standard_process_chart_attachments_sort_order", "standard_process_chart_attachments", ["sort_order"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_standard_process_chart_attachments_sort_order", table_name="standard_process_chart_attachments")
    op.drop_index("ix_standard_process_chart_attachments_chart_id", table_name="standard_process_chart_attachments")
    op.drop_table("standard_process_chart_attachments")
    op.drop_index("ix_standard_process_chart_layouts_chart_id", table_name="standard_process_chart_layouts")
    op.drop_table("standard_process_chart_layouts")
    op.drop_index("ix_standard_process_chart_steps_chart_id", table_name="standard_process_chart_steps")
    op.drop_table("standard_process_chart_steps")
    op.drop_index("ix_standard_process_charts_status", table_name="standard_process_charts")
    op.drop_index("ix_standard_process_charts_product_code", table_name="standard_process_charts")
    op.drop_index("ix_standard_process_charts_line_code", table_name="standard_process_charts")
    op.drop_index("ix_standard_process_charts_is_deleted", table_name="standard_process_charts")
    op.drop_table("standard_process_charts")
    op.drop_index("ix_lob_eb_criteria_site_id", table_name="lob_eb_criteria")
    op.drop_index("ix_lob_eb_criteria_product_code", table_name="lob_eb_criteria")
    op.drop_index("ix_lob_eb_criteria_line_code", table_name="lob_eb_criteria")
    op.drop_index("ix_lob_eb_criteria_is_active", table_name="lob_eb_criteria")
    op.drop_table("lob_eb_criteria")
