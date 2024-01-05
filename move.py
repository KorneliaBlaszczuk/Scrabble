class Move:
    """
    Class Move

    Manages logic - valid positions

    :param click: list of coordinates where player clicked
    :type click: list of tuples representing rows
    """

    def __init__(self):
        self._click = []

    @property
    def click(self):
        return self._click

    def update_click(self, coord):
        """
        Updates list of coordinates of the click
        """
        self.click.append(coord)
        return self.click

    def empty_click(self):
        """
        Empties the click list
        """
        self.click.clear()
        return self.click

    def click_handling(self, player, board, board_sprite):
        """
        Function that handles invalid mouse clicks
        """
        count = len(self.click)
        if (
            (count == 1 and ((self.click[0][0] != 16)))
            or (count == 1 and (self.click[0][1] > 10))
            or (count == 1 and (self.click[0][1] < 4))
            or (count == 1 and (player.rack[self.click[0][1] - 4] == ""))
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

    def valid_placement(self, board, board_sprite, player):
        """
        Manages validation of the placement. If it's correct nothing happens
        in this function. The game goes on. In case of the opposite, we
        execute not_valid_action.
        """
        if len(board.word_list) == 0 and not any(
            key == (7, 7) for key in board.current_word.keys()
        ):
            board.not_valid_action(board_sprite, player)
        elif (
            len(board.word_list) != 0
            and len(board.current_word.values()) == 1
            and all(
                board.not_touching(
                    list(board.current_word.keys())[0][0],
                    list(board.current_word.keys())[0][1],
                )
            )
        ):
            board.not_valid_action(board_sprite, player)
        elif not board.sort_current_word():
            board.not_valid_action(
                board_sprite,
                player,
            )
        else:
            if not board.current_word and not board.valid_added_word():
                board.not_valid_action(
                    board_sprite,
                    player,
                )
