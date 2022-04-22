import random


class Die:
    """A class representing a single die."""

    def __init__(self, color):
        """Initialize the die."""
        self.color = color

    def roll_die(self):
        """Return a random value between 1 and the number of sides."""
        return random.randint(1, 6)
