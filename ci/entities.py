from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ContractorData:
    employee_id: str
    first_name: str
    last_name: str
    rate: int
    start_date: date
    holiday_days: float
