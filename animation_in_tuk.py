from pico2d import *

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1024
SPRITE_WIDTH = 100
SPRITE_HEIGHT = 100
MOVE_SPEED = 220.0
FRAME_INTERVAL = 0.08
FRAME_COUNT = 8
BACKGROUND_IMAGE = 'TUK_GROUND.png'
SPRITE_IMAGE = 'animation_sheet.png'

IDLE_ROWS = {'left': 0, 'right': 0, 'up': 0, 'down': 0}
MOVE_ROWS = {'left': 300, 'right': 200, 'up': 100, 'down': 0}


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 'idle'
        self.facing = 'right'
        self.frame = 0
        self.frame_time = 0.0
        self.move_x = 0
        self.move_y = 0

    def update(self, dt, pressed):
        dx = 0
        dy = 0

        if pressed.get(SDLK_RIGHT, False):
            dx += 1
        if pressed.get(SDLK_LEFT, False):
            dx -= 1
        if pressed.get(SDLK_UP, False):
            dy += 1
        if pressed.get(SDLK_DOWN, False):
            dy -= 1

        self.move_x = dx
        self.move_y = dy

        if dx != 0 or dy != 0:
            self.state = 'move'
            if dx != 0:
                self.facing = 'right' if dx > 0 else 'left'
        else:
            self.state = 'idle'

        self.x += dx * MOVE_SPEED * dt
        self.y += dy * MOVE_SPEED * dt

        self.x = max(SPRITE_WIDTH // 2, min(self.x, WINDOW_WIDTH - SPRITE_WIDTH // 2))
        self.y = max(SPRITE_HEIGHT // 2, min(self.y, WINDOW_HEIGHT - SPRITE_HEIGHT // 2))

        self.frame_time += dt
        if self.frame_time >= FRAME_INTERVAL:
            self.frame = (self.frame + 1) % FRAME_COUNT
            self.frame_time = 0.0

    def draw(self, sprite_sheet):
        row = IDLE_ROWS[self.facing] if self.state == 'idle' else MOVE_ROWS[self.facing]
        sprite_x = self.frame * SPRITE_WIDTH
        sprite_sheet.clip_draw(sprite_x, row, SPRITE_WIDTH, SPRITE_HEIGHT, self.x, self.y)


def handle_events(pressed):
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                return False
            pressed[event.key] = True
        elif event.type == SDL_KEYUP:
            pressed[event.key] = False
    return True


def main():
    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    hide_cursor()
    background = load_image(BACKGROUND_IMAGE)
    sprite_sheet = load_image(SPRITE_IMAGE)

    running = True
    player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    pressed = {SDLK_LEFT: False, SDLK_RIGHT: False, SDLK_UP: False, SDLK_DOWN: False}

    last_time = get_time()
    while running:
        now = get_time()
        dt = now - last_time
        last_time = now

        running = handle_events(pressed)
        player.update(dt, pressed)

        clear_canvas()
        background.draw(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        player.draw(sprite_sheet)
        update_canvas()
        delay(0.01)

    close_canvas()


if __name__ == '__main__':
    main()
