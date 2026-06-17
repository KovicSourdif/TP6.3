# Kovic Sourdif
# TP6
# Jeux de roche papier ciseaux avec arcade


import arcade
from enum import Enum
from game_state import GameState
import random
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Starting Template"


# type d'attaque

class AttackType(Enum):
    ROCK = 0,
    PAPER = 1,
    SCISSORS = 2


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.AMAZON
        # assets
        self.computer = arcade.Sprite("Assets/compy.png", 1)
        self.joueur = arcade.Sprite("Assets/faceBeard.png", 0.2)

        self.rock = arcade.Sprite("Assets/srock.png", 0.4)
        self.paper = arcade.Sprite("Assets/spaper.png", 0.4)
        self.scissors = arcade.Sprite("Assets/scissors.png", 0.4)

        self.scissors_computer = arcade.Sprite("Assets/scissors.png", 0.4)
        self.paper_computer = arcade.Sprite("Assets/spaper.png", 0.4)
        self.rock_computer = arcade.Sprite("Assets/srock.png", 0.4)
        self.face_list = arcade.SpriteList()
        self.attack_list = arcade.SpriteList()
        self.computer_list = arcade.SpriteList()
        self.face_list.append(self.computer)
        self.face_list.append(self.joueur)

        # flage,score et autre variable
        self.scorejoueur = 0
        self.scorecomputer = 0
        self.currentstate = GameState.NOT_STARTED
        self.player_attack_type = None
        self.computer_attack_type = None
        self.flag_attack = False
        self.round_winner = None
        self.game_winner = None
        # If you have sprite lists, you should create them here,
        # and set them to None

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """
        Render the screen.
        """
        # coordonnée sprites
        self.computer.center_x = 800
        self.computer.center_y = 280

        self.joueur.center_x = 280
        self.joueur.center_y = 280

        self.scissors.center_x = 410
        self.scissors.center_y = 190

        self.paper.center_x = 280
        self.paper.center_y = 190

        self.rock.center_x = 150
        self.rock.center_y = 190

        self.paper_computer.center_x = 800
        self.paper_computer.center_y = 190

        self.rock_computer.center_x = 800
        self.rock_computer.center_y = 190

        self.scissors_computer.center_x = 800
        self.scissors_computer.center_y = 190

        self.clear()
        self.face_list.draw()

        self.attack_list.draw()
        if self.currentstate == GameState.ROUND_DONE or self.currentstate == GameState.GAME_OVER:
            self.computer_list.draw()

        # affichage
        arcade.draw.draw_lbwh_rectangle_outline(760, 160, 80, 60, (255, 0, 0), 3)

        arcade.draw.draw_lbwh_rectangle_outline(240, 160, 80, 60, (255, 0, 0), 3)
        arcade.draw.draw_lbwh_rectangle_outline(110, 160, 80, 60, (255, 0, 0), 3)
        arcade.draw.draw_lbwh_rectangle_outline(370, 160, 80, 60, (255, 0, 0), 3)
        # score et texte
        arcade.draw_text("Roche, Papier, Ciseaux", 140, 600, (255, 255, 255), 70)

        arcade.draw_text("Le pointage de joueur est de " + str(self.scorejoueur), 115, 120, (255, 255, 255), 20)
        arcade.draw_text("Le pointage de l'ordinateur est de " + str(self.scorecomputer), 625, 120, (255, 255, 255), 20)
        # Afficher les instructions au joueur
        if self.currentstate == GameState.NOT_STARTED:
            arcade.draw_text("Appuyer sur 'ESPACE' pour débuter une ronde!", 175, 500, (0, 255, 255), 30)

        if self.currentstate == GameState.ROUND_ACTIVE:
            arcade.draw_text("Appuyer sur une image pour faire une attaque!", 175, 500, (0, 255, 255), 30)

        if self.currentstate == GameState.ROUND_DONE:
            arcade.draw_text("Appuyer sur 'ESPACE' pour commencer", 245, 520, (0, 255, 255), 30)
            arcade.draw_text("une nouvelle ronde!", 370, 490, (0, 255, 255), 30)
            if self.round_winner == 0:
                arcade.draw_text("Égalité!", 460, 440, (0, 255, 255), 30)
            if self.round_winner == 1:
                arcade.draw_text("Vous avez gagné la ronde!", 315, 440, (0, 255, 255), 30)
            if self.round_winner == 2:
                arcade.draw_text("L'ordinateur a gagné la ronde!", 315, 440, (0, 255, 255), 30)

        if self.currentstate == GameState.GAME_OVER:
            if self.game_winner == 1:
                arcade.draw_text("Vous avez gagné la partie!", 325, 520, (0, 255, 0), 30)
            if self.game_winner == 2:
                arcade.draw_text("L'ordinateur a gagné la partie!", 325, 520, (0, 255, 0), 30)

            arcade.draw_text("La partie est terminée.", 345, 480, (0, 255, 255), 30)
            arcade.draw_text("Appuyer sur 'Espace' pour débuter une", 255, 430, (0, 255, 255), 30)
            arcade.draw_text("nouvelle partie", 390, 400, (0, 255, 255), 30)

    def on_update(self, delta_time):

        # déterminer qui a gagner la ronde
        if self.currentstate == GameState.ROUND_ACTIVE and self.flag_attack:

            self.computer_attack_type = random.choice(list(AttackType.__iter__()))

            if self.computer_attack_type == AttackType.ROCK:
                self.computer_list.clear()

                self.computer_list.append(self.rock_computer)

                if self.player_attack_type == AttackType.ROCK:
                    self.currentstate = GameState.ROUND_DONE
                    self.round_winner = 0

                if self.player_attack_type == AttackType.PAPER:
                    self.currentstate = GameState.ROUND_DONE
                    self.scorejoueur += 1
                    self.round_winner = 1

                if self.player_attack_type == AttackType.SCISSORS:
                    self.currentstate = GameState.ROUND_DONE
                    self.scorecomputer += 1
                    self.round_winner = 2

            if self.computer_attack_type == AttackType.PAPER:
                self.computer_list.clear()
                self.computer_list.append(self.paper_computer)

                if self.player_attack_type == AttackType.PAPER:
                    self.currentstate = GameState.ROUND_DONE
                    self.round_winner = 0

                if self.player_attack_type == AttackType.SCISSORS:
                    self.currentstate = GameState.ROUND_DONE
                    self.scorejoueur += 1
                    self.round_winner = 1

                if self.player_attack_type == AttackType.ROCK:
                    self.currentstate = GameState.ROUND_DONE
                    self.scorecomputer += 1
                    self.round_winner = 2

            if self.computer_attack_type == AttackType.SCISSORS:
                self.computer_list.clear()
                self.computer_list.append(self.scissors_computer)

                if self.player_attack_type == AttackType.SCISSORS:
                    self.currentstate = GameState.ROUND_DONE
                    self.round_winner = 0

                if self.player_attack_type == AttackType.ROCK:
                    self.currentstate = GameState.ROUND_DONE
                    self.scorejoueur += 1
                    self.round_winner = 1

                if self.player_attack_type == AttackType.PAPER:
                    self.currentstate = GameState.ROUND_DONE
                    self.scorecomputer += 1
                    self.round_winner = 2

            if self.scorejoueur == 3:
                self.currentstate = GameState.GAME_OVER
                self.game_winner = 1

            elif self.scorecomputer == 3:
                self.currentstate = GameState.GAME_OVER
                self.game_winner = 1

    def on_key_press(self, key, key_modifiers):
        # changer le statue du jeu
        if key == arcade.key.SPACE:
            if self.currentstate == GameState.NOT_STARTED:
                self.currentstate = GameState.ROUND_ACTIVE
                self.attack_list.append(self.rock)
                self.attack_list.append(self.paper)
                self.attack_list.append(self.scissors)
                self.computer_list.clear()

            elif self.currentstate == GameState.ROUND_DONE:
                self.player_attack_type = None
                self.computer_attack_type = None
                self.flag_attack = False

                self.attack_list.clear()
                self.computer_list.clear()

                self.attack_list.append(self.rock)
                self.attack_list.append(self.paper)
                self.attack_list.append(self.scissors)
                self.round_winner = None
                self.currentstate = GameState.ROUND_ACTIVE

            elif self.currentstate == GameState.GAME_OVER:

                self.player_attack_type = None
                self.computer_attack_type = None
                self.scorejoueur = 0
                self.scorecomputer = 0
                self.currentstate = GameState.ROUND_ACTIVE
                self.attack_list.clear()
                self.computer_list.clear()

                self.attack_list.append(self.rock)
                self.attack_list.append(self.paper)
                self.attack_list.append(self.scissors)
                self.game_winner = None

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        # detecter le choix d'attaque
        if self.rock.collides_with_point((x, y)) and self.currentstate == GameState.ROUND_ACTIVE:
            self.player_attack_type = AttackType.ROCK
            self.attack_list.clear()
            self.attack_list.append(self.rock)
            self.flag_attack = True

        if self.paper.collides_with_point((x, y)) and self.currentstate == GameState.ROUND_ACTIVE:
            self.player_attack_type = AttackType.PAPER
            self.attack_list.clear()
            self.attack_list.append(self.paper)
            self.flag_attack = True

        if self.scissors.collides_with_point((x, y)) and self.currentstate == GameState.ROUND_ACTIVE:
            self.player_attack_type = AttackType.SCISSORS
            self.attack_list.clear()
            self.attack_list.append(self.scissors)
            self.flag_attack = True

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()
