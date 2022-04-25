#!/usr/bin/env python3

from Qwixx import *

if __name__ == "__main__":
    Q = Qwixx(1, "Tim")
    Q.players[0].mark_row("Red", 8)
    Q.players[0].mark_row("Yellow", 8)
    Q.players[0].mark_row("Green", 8)
    Q.players[0].mark_row("Blue", 8)
    Q.play()
