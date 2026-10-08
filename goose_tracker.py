from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date
import json
from pathlib import Path
from typing import List
        

@dataclass
class GooseRecord:
    """Details about one goose that was hunted."""

    weight_lb: float
    length_in: float
    location: str
    gun: str
    caliber: str
    hunt_date: str

    def __post_init__(self) -> None:
        if self.weight_lb <= 0 or self.length_in <= 0:
            raise ValueError("Weight and length must be greater than zero.")
        if not self.location.strip():
            raise ValueError("Location is required.")
        if not self.gun.strip():
            raise ValueError("Gun is required.")
        if not self.caliber.strip():
            raise ValueError("Caliber is required.")


class GooseTracker:
    """Stores goose hunting records in a JSON file."""

    def __init__(self, file_path: str | Path = "goose_records.json") -> None:
        self.file_path = Path(file_path)
        self.records: List[GooseRecord] = self._load()

    def _load(self) -> List[GooseRecord]:
        if not self.file_path.exists():
            return []

        try:
            data = json.loads(self.file_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

        return [GooseRecord(**record) for record in data]

    def add_record(
        self,
        weight_lb: float,
        length_in: float,
        location: str,
        gun: str,
        caliber: str,
        hunt_date: str | date | None = None,
    ) -> GooseRecord:
        record = GooseRecord(
            weight_lb=float(weight_lb),
            length_in=float(length_in),
            location=location.strip(),
            gun=gun.strip(),
            caliber=caliber.strip(),
            hunt_date=(hunt_date.isoformat() if isinstance(hunt_date, date) else (hunt_date or date.today().isoformat())),
        )
        self.records.append(record)
        self.save()
        return record

    def save(self) -> None:
        self.file_path.write_text(
            json.dumps([asdict(record) for record in self.records], indent=2),
            encoding="utf-8",
        )

    def list_records(self) -> List[GooseRecord]:
        return list(self.records)

    def total_count(self) -> int:
        return len(self.records)

    def average_weight(self) -> float:
        if not self.records:
            return 0.0
        return sum(record.weight_lb for record in self.records) / len(self.records)


def main() -> None:
    tracker = GooseTracker()
    print("Goose Tracker")
    print("1. Add goose record")
    print("2. List records")
    print("3. Show statistics")
    print("4. Exit")

    while True:
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            try:
                weight = float(input("Weight (lb): "))
                length = float(input("Length (in): "))
                location = input("Location: ")
                gun = input("Gun: ")
                caliber = input("Caliber: ")
                date_value = input("Hunt date (YYYY-MM-DD, leave blank for today): ").strip()
                tracker.add_record(
                    weight,
                    length,
                    location,
                    gun,
                    caliber,
                    None if not date_value else date_value,
                )
                print("Record added.")
            except ValueError:
                print("Please enter valid numeric values.")
        elif choice == "2":
            if not tracker.records:
                print("No records saved.")
            for record in tracker.records:
                print(
                    f"{record.hunt_date}: {record.weight_lb} lb, "
                    f"{record.length_in} in, {record.location}, "
                    f"{record.gun} ({record.caliber})"
                )
        elif choice == "3":
            print(f"Total geese: {tracker.total_count()}")
            print(f"Average weight: {tracker.average_weight():.2f} lb")
        elif choice == "4":
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
