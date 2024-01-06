class Move:
    """
    Class Move

    Manages logic of mouse clicks

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
        Updates list of coordinates (row/col) of the click
        """
        self.click.append(coord)
        return self.click

    def empty_click(self):
        """
        Empties the click list
        """
        self.click.clear()
        return self.click

    def colid(self, board, board_sprite):
        """
        Checks if on the position there is not a tile
        """
        row = self.click[1][0]
        col = self.click[1][1]
        for letter in board_sprite:
            letter_row, letter_col = board.coord_to_row_col(letter.position)
            if letter_row == row and letter_col == col:
                return True
            else:
                continue
        return False

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
            or (count == 2 and (self.colid(board, board_sprite)))
        ):
            self.click.clear()
