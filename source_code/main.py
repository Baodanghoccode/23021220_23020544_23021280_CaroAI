"""
Main entry point for the Caro AI game
"""

import pygame
from game import Game


def main():
    """
    Khởi tạo Pygame và chạy game.
    """
    # Khởi tạo Pygame
    pygame.init()
    
    # Tạo và chạy trò chơi
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
