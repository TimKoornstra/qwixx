import random

class Die:
    """
    A class to represent a single die.

    ...

    Attributes
    ----------
    color : str
        The color of the die.

    Methods
    -------
    roll_die()
        Return a random value between 1 and the number of sides.

    """

    def __init__(self, color):
        """
        Initialize the die.
        
        Parameters
        ----------
        color : str
            The color of the die.
        """
        self.color = color

    def roll_die(self):
        """
        Return a random value between 1 and the number of sides.
        """
        return random.randint(1, 6)
