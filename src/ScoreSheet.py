from ScoreRow import *


class ScoreSheet:
    def __init__(self, player_name):
        self.name = player_name

        # Create 4 rows for the score sheet
        self.rows = {
            "Red": ScoreRow("Red"),
            "Yellow": ScoreRow("Yellow"),
            "Green": ScoreRow("Green"),
            "Blue": ScoreRow("Blue"),
        }

        # Counter for failed attempts
        self.failed_attempts = 0

    def __str__(self):
        title = f"{self.name}'s Score Sheet\n"
        seperation = "=" * 45 + "\n"
        rows = ""
        for row in self.rows.values():
            rows += str(row) + "\n"

        failed = f"Failed attempts: {self.failed_attempts}\n"
        total = f"Total score: {self.calculate_score()}"

        return title + seperation + rows + seperation + failed + total

    def mark_row(self, row_name, value):
        # Mark the row with the given value
        self.rows[row_name].fill_in_number(value)

    def add_failed_attempt(self):
        self.failed_attempts += 1

    def calculate_score(self):
        return (
            sum(row.calculate_score() for row in self.rows.values())
            + self.failed_attempts * -5
        )
