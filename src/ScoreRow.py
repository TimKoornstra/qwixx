class ScoreRow:
    def __init__(self, color):
        self.color = color
        self.closed = False

        # Create a new empty row for the score sheet
        self.values = {x: False for x in range(2, 13)}

    def __str__(self):
        row = ""
        for value in self.values:
            if self.values[value]:
                row += f"({value})"
            else:
                row += f" {value} "
            row += "-"

        return f"Color: {self.color}\n{row[:-1]} \nScore: {self.calculate_score()}"

    def calculate_score(self):
        # Count the number of True values in the values dictionary
        amount_in_row = sum(self.values.values())
        score_lookup = {
            0: 0,
            1: 1,
            2: 3,
            3: 6,
            4: 10,
            5: 15,
            6: 21,
            7: 28,
            8: 36,
            9: 45,
            10: 55,
            11: 66,
            12: 78,
            13: 91,
        }

        return score_lookup[
            amount_in_row + 1
            if amount_in_row >= 5 and self.values[12] == True
            else amount_in_row
        ]

    def is_allowed(self, value):
        # Find the latest value in the row that is True
        latest_value = 1
        for key, v in self.values.items():
            if v:
                latest_value = key

        if value == 12 and sum(self.values.values()) < 5:
            return False

        if value > latest_value and not self.closed:
            return True
        else:
            return False

    def fill_in_number(self, value):
        if self.is_allowed(value):
            self.values[value] = True

            if value == 12:
                self.closed = True

            return True
        else:
            return False
