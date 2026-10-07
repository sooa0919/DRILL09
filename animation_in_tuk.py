from pico2d import *

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1024
SPRITE_WIDTH = 100
SPRITE_HEIGHT = 100
MOVE_SPEED = 220
FRAME_INTERVAL = 0.08


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 'idle'
        self.facing = 'right'
        self.frame = 0
        self.frame_time = 0.0

    def update(self, dt, pressed):
        pass

    def draw(self, sprite_sheet):
        pass


def main():
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    hide_cursor()
    background = load_image('TUK_GROUND.png')
    sprite_sheet = load_image('animation_sheet.png')

    running = True
    player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    pressed = {SDLK_LEFT: False, SDLK_RIGHT: False, SDLK_UP: False, SDLK_DOWN: False}

    while running:
        clear_canvas()
        background.draw(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        player.draw(sprite_sheet)
        update_canvas()
        delay(0.016)

    close_canvas()


if __name__ == '__main__':
    main()
