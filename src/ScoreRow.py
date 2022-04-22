class ScoreRow:
    def __init__(self, color):
        self.color = color
        self.closed = False

        # Create a new empty row for the score sheet
        # Inverted row for green and blue colors
        if color == "Green" or color == "Blue":
            self.values = {x: False for x in range(12, 1, -1)}
        else:
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
        latest_index = 0
        for key, v in self.values.items():
            if v:
                latest_index += 1

        values = list(self.values)

        if value == values[-1] and sum(self.values.values()) < 5:
            return False

        index = values.index(value)

        if index > latest_index and not self.closed:
            return True
        else:
            return False

    def fill_in_number(self, value):
        if self.is_allowed(value):
            self.values[value] = True

            if value == list(self.values)[-1]:
                self.closed = True

            return True
        else:
            return False
