from ScoreRow import ScoreRow


class ScoreSheet:
    """
    A class representing a player's score sheet in the Qwixx game.

    Attributes
    ----------
    name : str
        The name of the player.
    rows : dict[str, ScoreRow]
        A dictionary of ScoreRow objects representing each colored row.
    failed_attempts : int
        The number of failed attempts.
    """

    def __init__(self, player_name: str):
        self.name = player_name
        self.rows = {
            "Red": ScoreRow("Red"),
            "Yellow": ScoreRow("Yellow"),
            "Green": ScoreRow("Green"),
            "Blue": ScoreRow("Blue"),
        }
        self.failed_attempts = 0

    def __str__(self) -> str:
        """
        Returns a string representation of the ScoreSheet.

        Returns
        -------
        str
            A string representation of the ScoreSheet.
        """
        title = f"{self.name}'s Score Sheet\n"
        separation = "=" * 45 + "\n"
        rows = "\n".join([str(row) for row in self.rows.values()])
        failed = f"Failed attempts: {self.failed_attempts}\n"
        total = f"Total score: {self.calculate_score()}"
        return title + separation + rows + "\n" + separation + failed + total

    def mark_row(self, row_name: str, value: int) -> bool:
        """
        Marks the specified row with the given value if allowed.

        Parameters
        ----------
        row_name : str
            The name of the row.
        value : int
            The value to mark in the row.

        Returns
        -------
        bool
            True if the marking was successful, False otherwise.
        """
        return self.rows[row_name].fill_in_number(value)

    def add_failed_attempt(self) -> None:
        """Increments the number of failed attempts by 1."""
        self.failed_attempts += 1

    def calculate_score(self) -> int:
        """
        Calculates the total score based on the rows and failed attempts.

        Returns
        -------
        int
            The total score.
        """
        return sum(row.calculate_score() for row in self.rows.values()) \
            - (self.failed_attempts * 5)
