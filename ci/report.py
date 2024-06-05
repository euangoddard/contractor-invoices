from calendar import monthrange, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY
from datetime import date
from pathlib import Path
from typing import Generator
from ci.entities import ContractorData, WorkingDays
import duckdb

WEEK_DAYS = frozenset((MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY))

HOLIDAYS_TABLE_NAME = "holidays"

RATES_TABLE_NAME = "rates"

DAYS_TABLE_NAME = "days"


def generate_report(year: int, month: int) -> None:
    contractor_data = _load_data()

    for item in contractor_data:
        working_days = _get_working_days_in_month(
            year,
            month,
            item.start_date,
            item.working_days,
        )
        days_worked = working_days - item.holiday_days
        print(
            f"Data for employee: {item.employee_id} ({item.first_name} {item.last_name})"
        )
        print(f" * Potential working days: {working_days}")
        print(f" * Took {item.holiday_days} days holiday")
        print(f" * Worked {days_worked} days")
        print(f" * Day rate: GBP {item.rate}")
        print(f" * Expected bill: GBP {item.rate * days_worked}")
        print("")


def _load_data() -> Generator[ContractorData, None, None]:
    _setup_table(_get_data_path("holidays.csv"), HOLIDAYS_TABLE_NAME)
    _setup_table(_get_data_path("rates.csv"), RATES_TABLE_NAME)
    _setup_table(_get_data_path("days.csv"), DAYS_TABLE_NAME)

    sql = f"""
SELECT 
    rates."Employee Id", 
    rates."First Name",
    rates."Last Name",
    rates."Salary Amount",
    rates."Salary Effective Date",
    COALESCE(
        (SELECT SUM("Holiday Duration (Days)") FROM {HOLIDAYS_TABLE_NAME} WHERE "Employee Id" = rates."Employee Id"), 
        0
    ),
    COALESCE(days.Mon, TRUE),
    COALESCE(days.Tue, TRUE),
    COALESCE(days.Wed, TRUE),
    COALESCE(days.Thu, TRUE),
    COALESCE(days.Fri, TRUE)
FROM {RATES_TABLE_NAME} LEFT JOIN {DAYS_TABLE_NAME} ON rates."Employee Id" = days."Employee Id" ORDER BY rates."First Name", rates."Last Name"
"""

    for row in duckdb.sql(sql).fetchall():
        yield ContractorData.from_data(row)


def _get_data_path(file_name: str) -> str:
    return str(Path(__file__).parent.parent / "data" / file_name)


def _setup_table(file_path: str, table_name: str) -> None:
    duckdb.sql(
        f'CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto("{file_path}")'
    )


def _get_working_days_in_month(
    year: int,
    month: int,
    start_date: date,
    contractor_work_days: WorkingDays,
) -> float:
    days_in_month = monthrange(year, month)[1]
    days = [date(year, month, day) for day in range(1, days_in_month + 1)]
    week_days_in_month = sum(
        [
            (
                1
                if d.weekday() in WEEK_DAYS
                and contractor_work_days.works_on(d.weekday())
                and start_date <= d
                else 0
            )
            for d in days
        ]
    )

    return float(week_days_in_month)
