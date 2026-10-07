from pico2d import *

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1024
SPRITE_WIDTH = 100
SPRITE_HEIGHT = 100
MOVE_SPEED = 220
FRAME_TIME = 0.08


def main():
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    hide_cursor()
    background = load_image('TUK_GROUND.png')
    character = load_image('animation_sheet.png')

    running = True
    x = WINDOW_WIDTH // 2
    y = WINDOW_HEIGHT // 2

    while running:
        clear_canvas()
        background.draw(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        character.clip_draw(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT, x, y)
        update_canvas()
        delay(0.016)

    close_canvas()


if __name__ == '__main__':
    main()
