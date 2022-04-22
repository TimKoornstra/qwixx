from ScoreRow import *

class ScoreSheet:
    """
    A class for the score sheet (a player).

    Attributes
    ----------
    name : str
        The name of the player.
    rows : dict
        A dictionary of ScoreRow objects.
    failed_attempts : int
        The number of failed attempts.
    
    Methods
    -------
    __str__()
        Returns a string representation of the score sheet.
    mark_row(row_name : str, value : int)
        Marks the row with the given value.
    add_failed_attempt()
        Adds a failed attempt to the score sheet.
    calculate_score()
        Calculates the total score of the score sheet.    
    """

    def __init__(self, player_name):
        """
        A constructor for the ScoreSheet class.

        Parameters
        ----------
        player_name : str
            The name of the player.
        
        Returns
        -------
        None
        """

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
        """
        Returns a string representation of the score sheet.

        Returns
        -------
        str
            A string representation of the score sheet.
        """

        title = f"{self.name}'s Score Sheet\n"
        seperation = "=" * 45 + "\n"
        rows = ""
        for row in self.rows.values():
            rows += str(row) + "\n"

        failed = f"Failed attempts: {self.failed_attempts}\n"
        total = f"Total score: {self.calculate_score()}"

        return title + seperation + rows + seperation + failed + total

    def mark_row(self, row_name : str, value : int):
        """
        Marks the row with the given value.

        Parameters
        ----------
        row_name : str
            The name of the row.
        value : int
            The value to mark in the row.

        Returns
        -------
        None
        """
        # Mark the row with the given value
        self.rows[row_name].fill_in_number(value)

    def add_failed_attempt(self):
        """
        Adds a failed attempt to the score sheet.

        Returns
        -------
        None
        """
        self.failed_attempts += 1

    def calculate_score(self):
        """
        Calculates the total score of the score sheet.

        Returns
        -------
        int
            The total score of the score sheet.
        """

        return (
            sum(row.calculate_score() for row in self.rows.values())
            + self.failed_attempts * -5
        )
