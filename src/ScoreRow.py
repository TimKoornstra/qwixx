class ScoreRow:
    """
    A class for a row in the score sheet.

    Parameters
    ----------
    color : str
        The color of the row.
    
    Methods
    -------
    __str__()
        Returns a string representation of the row.
    is_allowed(value : int)
        Returns True if the value is allowed in the row.
    fill_in_number(value : int)
        Fills in the given value in the row.
    calculate_score()
        Calculates the score of the row.    
    """

    def __init__(self, color : str):
        """
        A constructor for the ScoreRow class.

        Parameters
        ----------
        color : str
            The color of the row.
        
        Returns
        -------
        None
        """

        self.color = color
        self.closed = False

        # Create a new empty row for the score sheet
        # Inverted row for green and blue colors
        if color == "Green" or color == "Blue":
            self.values = {x: False for x in range(12, 1, -1)}
        else:
            self.values = {x: False for x in range(2, 13)}
        
    def __str__(self):
        """
        Returns a string representation of the row.

        Returns
        -------
        str
            A string representation of the row.
        """
       
        row = ""
        for value in self.values:
            if self.values[value]:
                row += f"({value})"
            else:
                row += f" {value} "
            row += "-"

        return f"Color: {self.color}\n{row[:-1]} \nScore: {self.calculate_score()}"

    def calculate_score(self):
        """
        Calculates the score of the row.

        Returns
        -------
        int
            The score of the row.
        """

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

    def is_allowed(self, value : int):
        """
        Checks if the given value is allowed in the row.

        Parameters
        ----------
        value : int
            The value to check.
        
        Returns
        -------
        bool
            True if the value is allowed in the row.
        """

        # Find the index of the latest value in the row that is True
        latest_index = 0
        i = 0
        for _, v in self.values.items():
            if v:
                latest_index = i
            i += 1

        values = list(self.values)

        # If the value is the latest value in the row and the amount of True values in the row is less than 5
        if value == values[-1] and sum(self.values.values()) < 5:
            return False

        index = values.index(value)
        
        # If the index of the value is greater than the index of the latest value in the row that is True and the row is not closed
        if index > latest_index and not self.closed:
            return True
        else:
            return False

    def fill_in_number(self, value : int):
        """
        Fills in the given value in the row.

        Parameters
        ----------
        value : int
            The value to fill in.
            
        Returns
        -------
        None
        """

        if self.is_allowed(value):
            self.values[value] = True

            if value == list(self.values)[-1]:
                self.closed = True

            return True
        else:
            return False
