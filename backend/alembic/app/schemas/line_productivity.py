from datetime import date
from decimal import Decimal
from typing import List

from pydantic import BaseModel


class LineProductivityItem(BaseModel):
    line_code: str
    product_code: str
    product_name: str | None = None
    lob: Decimal | None = None
    eb: Decimal | None = None
    labor_efficiency: Decimal | None = None
    target_end_time: str | None = None
    expected_end_time: str | None = None
    note: str | None = None
    standard_process_chart_count: int = 0


class LineProductivityListResponse(BaseModel):
    items: List[LineProductivityItem]
    total: int
    work_date: date | None = None
    data_source: str
    message: str | None = None
