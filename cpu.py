import random


class ComputerBrain:
    def __init__(self, used_positions, circle_shape=None, x_shape=None, circle_group=None, own_movements=None,
                 user_movements=None):
        self.game_total_mov = used_positions
        self.x = x_shape
        self.circle = circle_shape
        self.circle_group = circle_group
        self.game_grid = [
            [120, 120], [300, 120], [480, 120],
            [120, 300], [300, 300], [480, 300],
            [120, 480], [300, 480], [480, 480]
        ]
        self.winning_positions = [
            # Horizontal combinations
            [[120, 120], [300, 120], [480, 120]],  # Top row
            [[120, 300], [300, 300], [480, 300]],  # Middle row
            [[120, 480], [300, 480], [480, 480]],  # Bottom row

            # Vertical combinations
            [[120, 120], [120, 300], [120, 480]],  # Left column
            [[300, 120], [300, 300], [300, 480]],  # Middle column
            [[480, 120], [480, 300], [480, 480]],  # Right column

            # Diagonal combinations
            [[120, 120], [300, 300], [480, 480]],  # Top-left to bottom-right diagonal
            [[480, 120], [300, 300], [120, 480]]  # Top-right to bottom-left diagonal
        ]

        self.corner_pos = [[120, 120], [480, 120], [120, 480], [480, 480]]
        self.cross_pos = [[300, 120], [120, 300], [480, 300], [300, 480]]
        self.center_pos = [[300, 300]]

        self.available_positions = [pos for pos in self.game_grid if pos not in self.game_total_mov]
        self.available_corners = [pos for pos in self.corner_pos if pos in self.available_positions]
        self.available_cross = [pos for pos in self.cross_pos if pos in self.available_positions]

        self.own_mov = own_movements
        self.user_mov = user_movements

    def figure_maker(self, pos_list):
        """Receives a list with coordinates."""
        pos = None
        if len(pos_list) > 1:
            pos = random.choice(pos_list)
        elif len(pos_list) == 1:
            pos = pos_list[0]
        self.circle.create_rect(x_pos=pos[0], y_pos=pos[1])
        self.circle_group.add(self.circle)
        self.game_total_mov.append(pos)
        self.own_mov.append(pos)

    def anti_traps_start(self):
        if self.center_pos[0] in self.available_positions:
            self.figure_maker(self.center_pos)
        else:
            self.figure_maker(self.available_corners)

    def easy(self):
        if self.available_positions:
            self.figure_maker(self.available_positions)

    def medium(self):
        if self.available_positions:
            random_choice = random.randint(0, 8)
            # First moves
            if len(self.game_total_mov) < 2:
                if random_choice <= 5:
                    self.anti_traps_start()
                else:
                    self.easy()
            # Next moves
            else:
                if random_choice <= 6:
                    self.hard()
                else:
                    self.easy()

    def hard(self):
        if self.available_positions:
            # First move
            if len(self.game_total_mov) < 2:
                self.anti_traps_start()
            else:
                found_pos_to_block = False
                found_pos_to_win = False
                for row in self.winning_positions:
                    pos_to_win = [pos for pos in row if pos not in self.game_total_mov]
                    if len(pos_to_win) == 1 and pos_to_win[0] not in self.game_total_mov:
                        # Skip this row if the user has played a position in it
                        if any(pos in self.user_mov for pos in row):
                            continue
                        print('found position to win')
                        self.figure_maker(pos_to_win)
                        found_pos_to_win = True
                        break

                if not found_pos_to_win:
                    for row in self.winning_positions:
                        pos_to_block = [pos for pos in row if pos not in self.user_mov]
                        if len(pos_to_block) == 1 and pos_to_block[0] not in self.game_total_mov:
                            print('Found position to block')
                            self.figure_maker(pos_to_block)
                            found_pos_to_block = True
                            break

                    if not found_pos_to_block:
                        if len(self.own_mov) == 1 and [300, 300] in self.own_mov \
                                and self.user_mov[1] in self.corner_pos:
                            print('Covering traps by playing on the cross')
                            self.figure_maker(self.available_cross)

                        elif len(self.own_mov) == 1 and [300, 300] in self.own_mov \
                                and self.user_mov[1] in self.cross_pos:
                            print('Covering traps by playing on the corners')
                            self.figure_maker(self.available_corners)

                        else:
                            for row in self.winning_positions:
                                positions_to_fill = [pos for pos in row if pos not in self.game_total_mov]
                                if len(positions_to_fill) == 2 \
                                        and all(pos not in self.game_total_mov for pos in positions_to_fill):
                                    print('Found position to fill')
                                    self.figure_maker(positions_to_fill)
                                    break
