class Move:
    """
    Class Move
    Manages logic - valid positions
    """

    # najpierw patrzymy na położenie, a potem na valid_words
    def __init__(self):
        self.click = []

    def click_handling(self, player, board, board_sprite):
        """
        Function that handles invalid mouse clicks
        """
        count = len(self.click)
        if (
            (count == 1 and ((self.click[0][0] != 16)))
            or (count == 1 and (self.click[0][1] > 10))
            or (count == 1 and (self.click[0][1] < 4))
            or (count == 1 and (player.rack()[self.click[0][1] - 4] == ""))
            or (count == 2 and (self.click[1][0] > 14))
            or (
                count == 2
                and (
                    board.colid(
                        board_sprite,
                        self.click,
                    )
                )
            )
        ):
            self.click.clear()
