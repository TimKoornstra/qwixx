class ScoreRow:
    """
    A class for a row in the score sheet.

    Attributes
    ----------
    color : str
        The color of the row.
    closed : bool
        Indicates if the row is closed.
    values : dict[int, bool]
        Represents the numbers in the row and their statuses.
    """

    def __init__(self, color: str):
        """
        Initialize the ScoreRow.

        Parameters
        ----------
        color : str
            The color of the row.
        """
        self.color = color
        self.closed = False

        if color in ["Green", "Blue"]:
            self.values = {x: False for x in range(12, 1, -1)}
        else:
            self.values = {x: False for x in range(2, 13)}

    def __str__(self) -> str:
        """
        Returns a string representation of the ScoreRow.

        Returns
        -------
        str
            A string representation of the ScoreRow.
        """
        row = "".join([f"({value})" if self.values[value]
                      else f" {value} " for value in self.values])
        return f"Color: {self.color}\n{row}\nScore: {self.calculate_score()}"

    def calculate_score(self) -> int:
        """
        Calculates the score of the row.

        Returns
        -------
        int
            The score of the row.
        """
        count = sum(self.values.values())
        score = count * (count + 1) // 2

        # Add an extra point if the row is locked and has at least 5 crosses
        if self.closed and count >= 5:
            score += 1

        return score

    def is_allowed(self, value: int) -> bool:
        """
        Checks if the given value is allowed to be marked in the row.

        Parameters
        ----------
        value : int
            The value to be checked.

        Returns
        -------
        bool
            True if the value is allowed to be marked in the row, False
            otherwise.
        """
        # If the value is already marked or the row is closed, it's not allowed
        if value in self.values and self.values[value] or self.closed:
            return False

        latest_filled_value = next((v for v in reversed(
            self.values.keys()) if self.values[v]), None)

        # If no value has been marked yet, then the given value is allowed
        if latest_filled_value is None:
            return True

        # For Red and Yellow rows, the next value should be greater than the
        # latest filled value
        if self.color in ["Red", "Yellow"]:
            return value > latest_filled_value

        # For Green and Blue rows, the next value should be smaller than the
        # latest filled value
        if self.color in ["Green", "Blue"]:
            return value < latest_filled_value

        return False

    def fill_in_number(self, value: int) -> bool:
        """
        Marks the given value in the row.

        Parameters
        ----------
        value : int
            The value to be marked in the row.

        Returns
        -------
        bool
            True if the value is marked in the row, False otherwise.
        """
        if self.is_allowed(value):
            self.values[value] = True

            if value == list(self.values)[-1]:
                self.closed = True
            return True
        return False
