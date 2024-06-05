from dataclasses import dataclass
from datetime import date
from calendar import MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY


@dataclass(frozen=True)
class WorkingDays:
    mon: bool
    tue: bool
    wed: bool
    thu: bool
    fri: bool

    def works_on(self, day: int) -> bool:
        if day == MONDAY:
            return self.mon
        if day == TUESDAY:
            return self.tue
        if day == WEDNESDAY:
            return self.wed
        if day == THURSDAY:
            return self.thu
        if day == FRIDAY:
            return self.fri
        return False


@dataclass(frozen=True)
class ContractorData:
    employee_id: str
    first_name: str
    last_name: str
    rate: int
    start_date: date
    holiday_days: float
    working_days: WorkingDays

    @staticmethod
    def from_data(data: tuple) -> "ContractorData":
        return ContractorData(
            data[0],
            data[1],
            data[2],
            data[3],
            data[4],
            data[5],
            WorkingDays(*data[6:]),
        )
