from Die import Die
from ScoreSheet import ScoreSheet

import random


class Qwixx:
    """
    A class to represent a Qwixx game.

    Attributes
    ----------
    n_players : int
        The number of players in the game.
    players : List[ScoreSheet]
        The score sheets of the players in the game.
    dice : Dict[str, Die]
        The dice used in the game, mapped by color.
    enabled_colors : Dict[str, bool]
        Indicates which colors are still active in the game.
    """

    def __init__(self, n_players: int, *player_names: str):
        """
        Initializes a Qwixx game.

        Parameters
        ----------
        n_players : int
            Number of players in the game.
        *player_names : str
            Names of the players.

        Raises
        ------
        ValueError
            If the number of players does not match the number of names
            provided.
        """

        if player_names and len(player_names) != n_players:
            raise ValueError(
                "Number of players must match the number of names provided.")

        self.n_players = n_players
        self.players = [ScoreSheet(name) for name in player_names] if \
            player_names else [ScoreSheet(f"Player {i+1}") for i in
                               range(n_players)]
        self.dice = {
            "Red": Die("Red"),
            "Yellow": Die("Yellow"),
            "Green": Die("Green"),
            "Blue": Die("Blue"),
            "White1": Die("White"),
            "White2": Die("White")
        }
        self.enabled_colors = {"Red": True, "Yellow": True,
                               "Green": True, "Blue": True}

    def play(self):
        """
        Play the game.

        Returns
        -------
        None
        """
        # Random start player
        current_player = random.randint(0, self.n_players - 1)

        while not self.is_game_over():
            self.turn(current_player)
            current_player = (current_player + 1) % self.n_players

        print()
        print("==========================")
        print("Game over!\n")
        print("Final score sheets:")

        # Print the final score sheet
        for player in self.players:
            print(player)
            print()

        # Calculate the scores for each player and store them in a dictionary
        scores = {}
        for player in self.players:
            scores[player.name] = player.calculate_score()

        # Sort the scores in descending order
        sorted_scores = sorted(
            scores.items(), key=lambda x: x[1], reverse=True)

        print()
        # Print the scores
        print("Scores:")
        for name, score in sorted_scores:
            print(f"{name}: {score}")

        print()

        # Print the winner
        print(f"Winner: {sorted_scores[0][0]}!")

    def turn(self, player_number: int):
        """
        Play a turn for the player with the given number.

        Parameters
        ----------
        player_number : int
            the number of the current player.

        Returns
        -------
        None
        """

        # A turn:
        # 1. Roll the dice
        # 2. Choose which dice to keep if any
        # 3. Update the score sheet
        # 4. Let the other players mark the score sheet using the white dice

        # Roll the dice
        roll = self.roll_dice()

        # Let the current player go first
        white_combos, colored_combos = self.allowed_combinations(
            roll, player_number)

        # Print the allowed white combinations
        print(
            f"{self.players[player_number].name} can mark the following using "
            "the white dice: "
        )
        self.print_roll(white_combos)

        # Print the allowed combinations
        print(
            f"{self.players[player_number].name} can mark the following using "
            "other combinations: "
        )
        self.print_roll(colored_combos)

        # Show the player their score sheet
        print(self.players[player_number])

        closed_rows = []

        # Ask the player to choose a combination
        while True:
            white_color = None
            white_number = None
            colored_color = None
            colored_number = None

            print(f"{self.players[player_number].name}, choose an action: ")
            try:
                action = int(
                    input(
                        "1. Mark the score sheet using the white dice\n2. "
                        "Mark the score sheet using the colored dice\n3. Mark "
                        "the score sheet with the white dice followed by the "
                        "colored dice\n4. Add a failed attempt\n"
                    )
                )
            except ValueError:
                print("Invalid input.")
                continue
            if action not in [1, 2, 3, 4]:
                print("Invalid choice. Try again.\n")
                continue

            print()

            if action == 1 or action == 3:
                # Mark the score sheet using the white dice
                white_combo = input(
                    "Choose a combination that uses the white dice:\n")
                split_number = white_combo.split(" ")

                if (
                    split_number[0] not in white_combos.keys()
                    or int(split_number[1]) not in
                    white_combos[split_number[0]]
                ):
                    print("Invalid choice. Try again.\n")
                    continue

                white_color = split_number[0]
                white_number = int(split_number[1])

            if action == 2 or action == 3:
                # Mark the score sheet using the colored dice
                colored_combo = input(
                    "Choose a combination that uses the colored dice:\n"
                )
                split_number = colored_combo.split(" ")

                if (
                    split_number[0] not in colored_combos.keys()
                    or int(split_number[1]) not in
                    colored_combos[split_number[0]]
                ):
                    print("Invalid choice. Try again.\n")
                    continue

                colored_color = split_number[0]
                colored_number = int(split_number[1])

            if action == 3:
                if white_color == colored_color and \
                    ((colored_number <= white_number and
                      (colored_color == "Red" or colored_color == "Yellow"))
                        or (colored_number >= white_number and
                     (colored_color == "Green" or colored_color == "Blue"))):
                    print(
                        "This is not possible since the white number goes "
                        "first and the colored number comes after the white "
                        "number.\n"
                    )
                    continue

            closed_rows = self.play_action(
                int(action),
                player_number,
                white_color,
                white_number,
                colored_color,
                colored_number,
            )

            break

        print()

        if self.is_game_over():
            return

        # Ask the other players to mark the score sheet using the white dice
        for i in range(self.n_players):
            print("------------------------------------------------------")

            if i is not player_number:
                # List the possible white combinations
                white_combos, _ = self.allowed_combinations(roll, i)

                if len(white_combos) == 0:
                    print(
                        f"{self.players[i].name} cannot mark the score sheet "
                        "using the white dice."
                    )
                    continue

                print(
                    f"{self.players[i].name}, you can mark the score sheet "
                    "using the white dice\n"
                )

                print(self.players[i])
                print()
                print("Your possible choices: ")
                self.print_roll(white_combos)

                # Ask the player to choose a combination
                while True:
                    want_to = input(
                        "Would you like to mark the score sheet using the "
                        "white dice? (y/n)\n"
                    )
                    if want_to.lower() == "y":
                        white_combo = input(
                            "Choose a combination that uses the white dice:\n"
                        )
                        split_number = white_combo.split(" ")

                        if (
                            split_number[0] not in white_combos.keys()
                            or int(split_number[1]) not in
                            white_combos[split_number[0]]
                        ):
                            print("Invalid choice. Try again.\n")
                            continue

                        self.play_action(
                            1, i, split_number[0], int(
                                split_number[1]), None, None
                        )
                        break

                    elif want_to.lower() == "n":
                        break
                    else:
                        print("Invalid choice. Try again.\n")
                        continue

                # If the first player "closed" a row, close it for the other
                # players
                if closed_rows:
                    for row in closed_rows:
                        self.players[i].rows[row].closed = True

    def is_game_over(self) -> bool:
        """Checks if the game has ended based on game rules."""
        if any(player.failed_attempts >= 4 for player in self.players):
            return True
        return sum(self.enabled_colors.values()) <= 2

    def play_action(
        self,
        choice: int,
        player_number: int,
        white_color: str = None,
        white_number: int = None,
        colored_color: str = None,
        colored_number: int = None,
    ):
        """
        Play an action.

        Parameters
        ----------
        choice : int
            The action to be played.
        player_number : int
            The player number.
        white_color : str
            The chosen color for the white dice.
        white_number : int
            The number of the white dice.
        colored_color : str
            The chosen color for the colored dice.
        colored_number : int
            The number of the colored dice.

        Returns
        -------
        list
            The list of closed rows (if there are any).
        """

        # Option 1: Mark the score sheet using the white dice
        if choice == 1:
            if white_number is None or white_color is None:
                raise ValueError("No white dice combination was provided.")
            self.players[player_number].mark_row(white_color, white_number)
            print(
                f"{self.players[player_number].name} marked the score sheet "
                f"using the white dice {white_color} {white_number}."
            )

            # Print if the row is closed
            if self.players[player_number].rows[white_color].closed:
                print(f"The {white_color.lower()} row is now closed!")
                return [white_color]

        # Option 2: Mark the score sheet using the colored dice
        elif choice == 2:
            if colored_color is None or colored_number is None:
                raise ValueError("Color and number must be provided.")

            self.players[player_number].mark_row(colored_color, colored_number)
            print(
                f"{self.players[player_number].name} marked the score sheet "
                "using the colored dice {colored_color} {colored_number}."
            )

            # Print if the row is closed
            if self.players[player_number].rows[colored_color].closed:
                print(f"The {colored_color.lower()} row is now closed!")
                return [colored_color]

        # Option 3: Mark the score sheet with the white dice followed by the
        # colored dice
        elif choice == 3:
            if colored_color is None or colored_number is None:
                raise ValueError("Color and number must be provided.")
            if white_number is None or white_color is None:
                raise ValueError("No white dice combination was provided.")

            self.players[player_number].mark_row(white_color, white_number)
            self.players[player_number].mark_row(colored_color, colored_number)
            print(
                f"{self.players[player_number].name} marked the score sheet "
                f"using the white dice {white_color} {white_number} and the "
                f"colored dice {colored_color} {colored_number}."
            )

            closed_colors = []
            # Print if the row is closed
            if self.players[player_number].rows[white_color].closed:
                print(f"The {white_color.lower()} row is now closed!")
                closed_colors.append(white_color)
            if self.players[player_number].rows[colored_color].closed:
                print(f"The {colored_color.lower()} row is now closed!")
                closed_colors.append(colored_color)

            return closed_colors

        # Option 4: Adding a failed attempt
        elif choice == 4:
            self.players[player_number].add_failed_attempt()
            print(
                f"{self.players[player_number].name} added a failed attempt.")

    def roll_dice(self):
        """
        Roll the dice.

        Returns
        -------
        list
            The list of the rolled dice.
        """

        # Roll the dice of the enabled colors
        roll = {
            color: self.dice[color].roll()
            for color in self.enabled_colors
            if self.enabled_colors[color]
        }

        # Roll the white dice
        white1 = self.dice["White1"].roll()
        white2 = self.dice["White2"].roll()

        # Save all possible dice combinations
        combinations = {"White": [white1 + white2]}

        for color in roll:
            combinations[f"{color}"] = sorted(
                (roll[color] + white1, roll[color] + white2)
            )

        return combinations

    def allowed_combinations(self, roll: dict, player_number: int):
        """
        Filter the possible combinations of the dice to only the ones that are
        allowed.

        Parameters
        ----------
        roll : dict
            The dictionary of the rolled dice.
        player_number : int
            The player number.

        Returns
        -------
        list, list
            The list of the allowed combinations for the white dice and the
            list of the allowed combinations for the colored dice.
        """

        # Filter out the combinations that are not allowed for player_number
        allowed_colored_combinations = {}
        allowed_white_combinations = {}

        for key, value in roll.items():
            if key == "White":
                for row in self.players[player_number].rows.values():
                    if row.is_allowed(value[0]):
                        allowed_white_combinations[row.color] = [value[0]]

            else:
                for i in range(len(value)):
                    if self.players[player_number]\
                            .rows[key].is_allowed(value[i]):
                        allowed_colored_combinations[key] = (
                            [value[i]]
                            if key not in allowed_colored_combinations
                            else (
                                allowed_colored_combinations[key] + [value[i]]
                                if not value[i] in
                                allowed_colored_combinations[key]
                                else allowed_colored_combinations[key]
                            )
                        )

        return allowed_white_combinations, allowed_colored_combinations

    def print_roll(self, roll: dict):
        """
        Print the roll in a nice way.

        Parameters
        ----------
        roll : dict
            The dictionary of the rolled dice.

        Returns
        -------
        None
        """

        print("Color     | Roll(s)")
        print("----------+----------")
        for key, value in roll.items():
            r = key
            r += " " * (10 - len(key)) + "| "
            for v in value:
                r += str(v) + " "

            print(r)
        print()
