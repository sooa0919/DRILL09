from pico2d import *

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1024
SPRITE_WIDTH = 100
SPRITE_HEIGHT = 100
START_X = WINDOW_WIDTH // 2
START_Y = WINDOW_HEIGHT // 2
MOVE_SPEED = 220.0
FRAME_INTERVAL = 0.08
FRAME_COUNT = 8
BACKGROUND_IMAGE = 'TUK_GROUND.png'
SPRITE_IMAGE = 'animation_sheet.png'

IDLE_ROWS = {'left': 0, 'right': 0, 'up': 0, 'down': 0}
MOVE_ROWS = {'left': 300, 'right': 200, 'up': 100, 'down': 0}
IDLE_FRAME_START = 0
MOVE_FRAME_START = 0


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
        self.is_moving = False

    def update(self, dt, pressed):
        dx, dy = direction_from_input(pressed)
        self.set_motion(dx, dy)

    def is_idle(self):
        return not self.is_moving

    def set_motion(self, dx, dy):
        self.move_x = dx
        self.move_y = dy
        self.is_moving = dx != 0 or dy != 0

        if self.is_moving:
            self.state = 'move'
            if dx != 0:
                self.facing = 'right' if dx > 0 else 'left'
            # 위아래 입력일 때는 마지막 좌우 방향을 유지한다.
        else:
            self.state = 'idle'

        self.x += dx * MOVE_SPEED * dt
        self.y += dy * MOVE_SPEED * dt
        self.x = clamp(self.x, SPRITE_WIDTH // 2, WINDOW_WIDTH - SPRITE_WIDTH // 2)
        self.y = clamp(self.y, SPRITE_HEIGHT // 2, WINDOW_HEIGHT - SPRITE_HEIGHT // 2)

        self.frame_time += dt
        if self.frame_time >= FRAME_INTERVAL:
            self.frame = (self.frame + 1) % FRAME_COUNT
            self.frame_time = 0.0
        # 이동 상태와 정지 상태가 모두 애니메이션 타이머와 연결된다.

    def animation_row(self):
        if self.is_idle():
            return IDLE_ROWS[self.facing]
        return MOVE_ROWS[self.facing]

    def draw(self, sprite_sheet):
        # 화면 경계 안에서만 이동하는 캐릭터를 그린다.
        row = self.animation_row()
        sprite_x = self.frame * SPRITE_WIDTH
        sprite_sheet.clip_draw(sprite_x, row, SPRITE_WIDTH, SPRITE_HEIGHT, self.x, self.y)


def clamp(value, lower, upper):
    return max(lower, min(value, upper))


def direction_from_input(pressed):
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

    return dx, dy


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
    player = Player(START_X, START_Y)
    pressed = {key: False for key in (SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN)}

    last_time = get_time()
    while running:
        now = get_time()
        dt = now - last_time
        last_time = now

        running = handle_events(pressed)
        if not running:
            break

        player.update(dt, pressed)

        clear_canvas()
        background.draw(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        player.draw(sprite_sheet)
        update_canvas()
        delay(0.01)

    close_canvas()


if __name__ == '__main__':
    main()
