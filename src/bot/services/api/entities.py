from dataclasses import dataclass, field


@dataclass
class Sportsman:
    name: str
    surname: str
    fullname: str = field(init=False)
    chat_id: int
    sheet_id: int
    archive_sheet_id: int
    morning_reminder_sent: bool
    evening_reminder_sent: bool

    def __post_init__(self):
        self.fullname = f"{self.name} {self.surname}"
