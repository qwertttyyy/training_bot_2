from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Sportsman:
    name: str
    surname: str
    full_name: str = field(init=False)
    chat_id: int
    sheet_id: int
    archive_sheet_id: int
    morning_report_sent: bool
    training_report_sent: bool

    def __post_init__(self):
        self.full_name = f"{self.name} {self.surname}"


@dataclass
class MorningReport:
    health_score: Optional[int] = field(default=None)
    sleep_hours: Optional[float] = field(default=None)
    heart_rate: Optional[int] = field(default=None)
