import random


class Die:
    """
    A class to represent a single die.

    Attributes
    ----------
    color : str
        The color of the die.
    sides : int
        The number of sides of the die (default is 6).

    Methods
    -------
    roll() -> int
        Return a random value between 1 and the number of sides.
    """

    def __init__(self, color: str, sides: int = 6):
        """
        Initialize the die.

        Parameters
        ----------
        color : str
            The color of the die.
        sides : int, optional
            The number of sides of the die. Defaults to 6.
        """
        self.color = color
        self.sides = sides

    def roll(self) -> int:
        """
        Roll the die.

        Returns
        -------
        int
            A random value between 1 and the number of sides.
        """
        return random.randint(1, self.sides)
