"""remove amr collision alert and recognition types

Revision ID: 9c1f2a7b8d3e
Revises: eeb3fb42cb28
Create Date: 2026-06-02 10:42:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9c1f2a7b8d3e"
down_revision: Union[str, Sequence[str], None] = "eeb3fb42cb28"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove AMR collision enum values from existing PostgreSQL databases."""
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return

    op.execute("UPDATE alert_thresholds SET alert_type = 'custom' WHERE alert_type = 'amr_collision'")
    op.execute("UPDATE alert_logs SET alert_type = 'custom' WHERE alert_type = 'amr_collision'")
    op.execute("UPDATE recognition_logs SET recognition_type = 'custom' WHERE recognition_type = 'amr'")

    op.execute("ALTER TYPE alert_type RENAME TO alert_type_old")
    op.execute("CREATE TYPE alert_type AS ENUM ('helmet_color', 'unauthorized_person', 'intrusion', 'custom')")
    op.execute(
        "ALTER TABLE alert_thresholds ALTER COLUMN alert_type TYPE alert_type "
        "USING alert_type::text::alert_type"
    )
    op.execute(
        "ALTER TABLE alert_logs ALTER COLUMN alert_type TYPE alert_type "
        "USING alert_type::text::alert_type"
    )
    op.execute("DROP TYPE alert_type_old")

    op.execute("ALTER TYPE recognition_type RENAME TO recognition_type_old")
    op.execute(
        "CREATE TYPE recognition_type AS ENUM ('worker', 'helmet', 'action', 'intrusion', 'custom')"
    )
    op.execute(
        "ALTER TABLE recognition_logs ALTER COLUMN recognition_type TYPE recognition_type "
        "USING recognition_type::text::recognition_type"
    )
    op.execute("DROP TYPE recognition_type_old")


def downgrade() -> None:
    """Reintroduce removed enum values for rollback compatibility."""
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return

    op.execute("ALTER TYPE alert_type RENAME TO alert_type_old")
    op.execute(
        "CREATE TYPE alert_type AS ENUM "
        "('amr_collision', 'helmet_color', 'unauthorized_person', 'intrusion', 'custom')"
    )
    op.execute(
        "ALTER TABLE alert_thresholds ALTER COLUMN alert_type TYPE alert_type "
        "USING alert_type::text::alert_type"
    )
    op.execute(
        "ALTER TABLE alert_logs ALTER COLUMN alert_type TYPE alert_type "
        "USING alert_type::text::alert_type"
    )
    op.execute("DROP TYPE alert_type_old")

    op.execute("ALTER TYPE recognition_type RENAME TO recognition_type_old")
    op.execute(
        "CREATE TYPE recognition_type AS ENUM "
        "('worker', 'helmet', 'amr', 'action', 'intrusion', 'custom')"
    )
    op.execute(
        "ALTER TABLE recognition_logs ALTER COLUMN recognition_type TYPE recognition_type "
        "USING recognition_type::text::recognition_type"
    )
    op.execute("DROP TYPE recognition_type_old")
