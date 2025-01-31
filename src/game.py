from board import *
from AI import AI
from button import Button
import webbrowser
import sys


class Game:
    def __init__(self):
        # Window settings
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_icon(WINDOW_ICON)
        pygame.display.set_caption("Connect 4")

        # Variables
        self.mouse_pos = (-1, -1)
        self.board = Board()
        self.computer = AI()
        self.is_player_red = True

        # Main Menu Buttons
        self._play_button = Button(WIDTH // 2 - 200, 175, PLAY_BUTTON, HOVERED_PLAY)
        self._options_button = Button(WIDTH // 2 - 200, 400, OPTIONS_BUTTON, HOVERED_OPTIONS)
        self._exit_button = Button(WIDTH // 2 - 200, 625, EXIT_BUTTON, HOVERED_EXIT)

        # Git/LinkedIn Buttons
        self._git_button = Button(30, 700, GIT_ICON, HOVERED_GIT)
        self._linkedin_button = Button(720, 700, LINKEDIN_ICON, HOVERED_LINKEDIN)

        # Options Menu Buttons
        self._player_red = Button(WIDTH // 2 - 200, 175, PLAYER_COLOR_RED, HOVERED_COLOR_RED)
        self._player_yellow = Button(WIDTH // 2 - 200, 175, PLAYER_COLOR_YELLOW, HOVERED_COLOR_YELLOW)
        self._pvp_disabled = Button(WIDTH // 2 - 200, 400, PVP_DISABLED, HOVERED_PVP_DISABLED)
        self._pvp_enabled = Button(WIDTH // 2 - 200, 400, PVP_ENABLED, HOVERED_PVP_ENABLED)

        self._easy_difficulty = Button(WIDTH // 2 - 200, 625, EASY_DIFFICULTY, HOVERED_EASY_DIFFICULTY)
        self._medium_difficulty = Button(WIDTH // 2 - 200, 625, MEDIUM_DIFFICULTY, HOVERED_MEDIUM_DIFFICULTY)
        self._hard_difficulty = Button(WIDTH // 2 - 200, 625, HARD_DIFFICULTY, HOVERED_HARD_DIFFICULTY)

        self._back_arrow = Button(720, 700, BACK_ARROW, HOVERED_BACK_ARROW)

    # Menu Functions
    def main_menu(self):
        # Function that sets up the main menu and runs its game-loop.
        self.window.fill(LIGHT_BLUE)
        self.window.blit(BG_IMAGE, (120, 0))

        while True:
            self.mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Transition into the game screen if the player clicks play.
                        if self._play_button.is_mouse_over(self.mouse_pos):
                            if self.is_player_red or self.board.pvp:
                                self.board.player_turn = True
                                self.board.player_color = 'Red'
                            else:
                                self.board.player_turn = False
                                self.board.player_color = 'Yellow'
                            self.run()
                        # Transition to the options' menu if player clicks the options button.
                        elif self._options_button.is_mouse_over(self.mouse_pos):
                            self.options_menu()
                        # Open the git url if the icon is selected.
                        elif self._git_button.is_mouse_over(self.mouse_pos):
                            webbrowser.open(GIT_URL, new=0, autoraise=True)
                        # Open the LinkedIn url if the icon is selected.
                        elif self._linkedin_button.is_mouse_over(self.mouse_pos):
                            webbrowser.open(LINKEDIN_URL, new=0, autoraise=True)
                        elif self._exit_button.is_mouse_over(self.mouse_pos):
                            pygame.quit()
                            sys.exit()

            self._play_button.draw(self.window, self.mouse_pos)
            self._options_button.draw(self.window, self.mouse_pos)
            self._exit_button.draw(self.window, self.mouse_pos)

            self._git_button.draw(self.window, self.mouse_pos)
            self._linkedin_button.draw(self.window, self.mouse_pos)

            pygame.display.update()

    def options_menu(self):
        # Setting up the options menu and its game-loop.
        self.window.fill(LIGHT_BLUE)
        self.window.blit(BG_IMAGE, (120, 0))
        while True:
            self.mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Transitioning from the options' menu to the main menu using ESC.
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self._player_red.is_mouse_over(self.mouse_pos):
                            # is_player_red controls which button appears,
                            # we also change the computers symbol.
                            self.is_player_red = not self.is_player_red
                            self.computer.change_computer_symbol()
                            break
                        elif self._pvp_enabled.is_mouse_over(self.mouse_pos):
                            self.board.pvp = not self.board.pvp
                            break
                        elif self._easy_difficulty.is_mouse_over(self.mouse_pos):
                            self.computer.set_search_depth()
                        elif self._git_button.is_mouse_over(self.mouse_pos):
                            webbrowser.open(GIT_URL, new=0, autoraise=True)
                        # Transitioning to the main menu with clicking on the arrow.
                        elif self._back_arrow.is_mouse_over(self.mouse_pos):
                            self.main_menu()

            self._back_arrow.draw(self.window, self.mouse_pos)

            self._player_yellow.draw_changing_button(self.window, self.mouse_pos,
                                                     self._player_red, self.is_player_red)

            self._pvp_disabled.draw_changing_button(self.window, self.mouse_pos,
                                                    self._pvp_enabled, self.board.pvp)

            if self.computer.search_depth == 1:
                self._easy_difficulty.draw(self.window, self.mouse_pos)
            elif self.computer.search_depth == 2:
                self._medium_difficulty.draw(self.window, self.mouse_pos)
            else:
                self._hard_difficulty.draw(self.window, self.mouse_pos)

            pygame.display.update()

    # Game Functions
    def update_events(self):
        self.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Transition back to the main menu and reset the board.
                if event.key == pygame.K_ESCAPE:
                    self.board.reset()
                    self.main_menu()
                    return
                # Resetting the board when pressing 'r'.
                elif event.key == pygame.K_r:
                    self.board.reset()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.board.game_over:
                        self.board.reset()

                    if self.board.player_turn:
                        self.board.play_move(self.mouse_pos)

    def update(self):
        if not self.board.game_over:
            self.board.check_winner()

        if not self.board.game_over and not self.board.player_turn\
           and not self.board.pvp:
            self.computer.generate_best(self.board)

    def render(self):
        self.board.draw_grid(self.window, self.mouse_pos[0])
        pygame.display.update()

    def run(self):
        self.window.fill(LIGHT_BLUE)
        while True:
            self.update_events()
            self.update()
            self.render()
