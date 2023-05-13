import pygame
import pygame_gui
import sys
import random
from pygame.locals import USEREVENT
from typing import List
import mido
import numpy as np
import time

screen_width = 800
screen_height = 600
outport = mido.open_output()

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
ui_manager = pygame_gui.UIManager((screen_width, screen_height))

screen = pygame.display.set_mode((screen_width, screen_height))

ui_manager = pygame_gui.UIManager((screen_width, screen_height))

slider_x = 30
label_x = 10

friction_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((slider_x, 20), (150, 20)),
    start_value=0.5,
    value_range=(0.0, 1.0),
    manager=ui_manager,
)
fall_speed_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((slider_x, 50), (150, 20)),
    start_value=5,
    value_range=(1, 10),
    manager=ui_manager,
)
ball_lifetime_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((slider_x, 80), (150, 20)),
    start_value=300,
    value_range=(100, 500),
    manager=ui_manager,
)
gravity_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((slider_x, 110), (150, 20)),
    start_value=0.2,
    value_range=(0.0, 1.0),
    manager=ui_manager,
)

bounce_threshold_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((slider_x, 140), (150, 20)),
    start_value=1,
    value_range=(0, 10),
    manager=ui_manager,
)

ball_spawn_rate_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((slider_x, 170), (150, 20)),
    start_value=1,
    value_range=(1, 10),
    manager=ui_manager,
)

wind_strength_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((slider_x, 200), (150, 20)),
    start_value=0,
    value_range=(0, 10),
    manager=ui_manager,
)

wind_direction_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((slider_x, 230), (150, 20)),
    start_value=0,
    value_range=(-1, 1),
    manager=ui_manager,
)



start_stop_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((640, 170), (150, 20)),
    text="START/STOP",
    manager=ui_manager,
)




reset_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((690, 80), (100, 30)),
    text="Reset",
    manager=ui_manager,
)

velocity_min_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(
        (662, 110), (128, 20) 
    ),
    start_value=30,
    value_range=(0, 127),
    manager=ui_manager,
)

velocity_max_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(
        (662, 130), (128, 20),
    ),
    start_value=100,
    value_range=(0, 127),
    manager=ui_manager,
)

exponent_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(
        (662,150), (128, 20)
    ),
    start_value=2,
    value_range=(2, 16),
    manager=ui_manager,
)

note_length_min_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((662, 190), (128, 20)),
    start_value=20,
    value_range=(1, 1000),
    manager=ui_manager,
)

note_length_max_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((662, 210), (128, 20)),
    start_value=200,
    value_range=(1, 1000),
    manager=ui_manager,
)




friction_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((40, 20), (120, 20)),
    text=" Friction",
    manager=ui_manager,
)
fall_speed_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((40, 50), (120, 20)),
    text=" Fall Speed",
    manager=ui_manager,
)
ball_lifetime_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((40, 80), (120, 20)),
    text=" Ball Lifetime",
    manager=ui_manager,
)
gravity_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((40, 110), (120, 20)),
    text=" Gravity",
    manager=ui_manager,
)

bounce_threshold_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((40, 140), (120, 20)),
    text=" Threshold",
    manager=ui_manager,
)

ball_spawn_rate_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((40, 170), (120, 20)),
    text=" Spawn Rate",
    manager=ui_manager,
)

wind_strength_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((40, 200), (120, 20)),
    text=" Wind Strength",
    manager=ui_manager,
)

wind_direction_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((40, 230), (120, 20)),
    text=" Wind Direction",
    manager=ui_manager,
)


velocity_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(
        (662, 110), (128, 20) 
    ),
    text=" Min VELOCITY",
    manager=ui_manager,
)
velocity_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(
        (662, 130), (128, 20),
    ),
    text=" Max VELOCITY",
    manager=ui_manager,
)

exponent_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(
        (662,150), (128, 20)
    ),
    text=" DynamicRange",
    manager=ui_manager,
)

note_length_min_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(
        (662, 190), (128, 20) 
    ),
    text=" Min LENGTH",
    manager=ui_manager,
)
note_length_max_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(
        (662, 210), (128, 20),
    ),
    text=" Max LENGTH",
    manager=ui_manager,
)


note_name_to_number = {
    "C": 0,
    "C#": 1,
    "D": 2,
    "D#": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "G": 7,
    "G#": 8,
    "A": 9,
    "A#": 10,
    "B": 11,
}


scale_options = ['Chromatic', 'Major', 'Minor', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian', 'Pentatonic', 'Blues', 'Minor Pentatonic', 'Japanese In', 'All C', 'Hungarian Minor', 'Greek']
scale_dropdown = pygame_gui.elements.UIDropDownMenu(scale_options, starting_option='Chromatic', relative_rect=pygame.Rect((screen_width - 110, 50), (100, 30)),manager=ui_manager)

min_octave = 3
max_octave = 5
min_midi_note = min_octave * 12
max_midi_note = max_octave * 12

keyboard_width = screen_width
keyboard_height = 100

keyboard_y = screen_height - keyboard_height

num_notes = (max_octave - min_octave + 1) * 12

key_width = keyboard_width / num_notes

def init_midi_port():
    available_ports = mido.get_output_names()

    if available_ports:
        return available_ports
    else:
        print("No MIDI output ports available.")
        sys.exit()


def create_midi_port_dropdown(available_ports):
    return pygame_gui.elements.UISelectionList(
        relative_rect=pygame.Rect((screen_width - 150, 10), (140, 200)),
        manager=ui_manager,
        item_list=available_ports,
        object_id="midi_port_dropdown",
    )

midi_port_names = init_midi_port()

midi_port_selector = pygame_gui.elements.UIDropDownMenu(
    options_list=midi_port_names,
    starting_option=midi_port_names[0],
    relative_rect=pygame.Rect((screen_width - 210, 10), (200, 40)),
    manager=ui_manager
)



def get_note_number(x_pos):
    scale_indices = {
        'Chromatic': list(range(12)),
        'Major': [0, 2, 4, 5, 7, 9, 11],
        'Minor': [0, 2, 3, 5, 7, 8, 10],
        'Dorian': [0, 2, 3, 5, 7, 9, 10],
        'Phrygian': [0, 1, 3, 5, 7, 8, 10],
        'Lydian': [0, 2, 4, 6, 7, 9, 11],
        'Mixolydian': [0, 2, 4, 5, 7, 9, 10],
        'Aeolian': [0, 2, 3, 5, 7, 8, 10],
        'Locrian': [0, 1, 3, 5, 6, 8, 10],
        'Pentatonic': [0, 2, 4, 7, 9],
        'Blues': [0, 3, 5, 6, 7, 10],
        'Minor Pentatonic': [0, 3, 5, 7, 10],
        'Japanese In': [0, 1, 5, 6, 10],
        'All C': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'Hungarian Minor': [0, 2, 3, 6, 7, 8, 11],
        'Greek': [0, 1, 4, 5, 7, 8, 10]
    }


    selected_scale = scale_dropdown.selected_option
    scale = scale_indices[selected_scale]
    num_notes = len(scale)
    index = int(x_pos / screen_width * num_notes)
    return 60 + scale[index % num_notes] 

def get_note_name_for_x_pos(x_pos):
    note_name_list = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    scale_indices = {
        'Chromatic': list(range(12)),
        'Major': [0, 2, 4, 5, 7, 9, 11],
        'Minor': [0, 2, 3, 5, 7, 8, 10],
        'Dorian': [0, 2, 3, 5, 7, 9, 10],
        'Phrygian': [0, 1, 3, 5, 7, 8, 10],
        'Lydian': [0, 2, 4, 6, 7, 9, 11],
        'Mixolydian': [0, 2, 4, 5, 7, 9, 10],
        'Aeolian': [0, 2, 3, 5, 7, 8, 10],
        'Locrian': [0, 1, 3, 5, 6, 8, 10],
        'Pentatonic': [0, 2, 4, 7, 9],
        'Blues': [0, 3, 5, 6, 7, 10],
        'Minor Pentatonic': [0, 3, 5, 7, 10],
        'Japanese In': [0, 1, 5, 6, 10],
        'All C': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'Hungarian Minor': [0, 2, 3, 6, 7, 8, 11],
        'Greek': [0, 1, 4, 5, 7, 8, 10]
    }
    note_number = get_note_number(x_pos)
    note_name = note_name_list[note_number % 12]
    return note_name

def play_note_async(ball, note_number, velocity, note_length):
    outport.send(
        mido.Message(
            "note_on", channel=0, note=note_number, velocity=velocity, time=0
        )
    )
    ball.note_off_time = time.time() + note_length / 1000






ball_radius = 10
ball_color = (255, 255, 255)

def check_collision(ball, obstacle):
    circle_distance_x = abs(ball.pos[0] - (obstacle.start_pos[0] + obstacle.end_pos[0]) / 2)
    circle_distance_y = abs(ball.pos[1] - (obstacle.start_pos[1] + obstacle.end_pos[1]) / 2)

    if circle_distance_x > (ball_radius + (obstacle.end_pos[0] - obstacle.start_pos[0]) / 2):
        return False
    if circle_distance_y > (ball_radius + (obstacle.end_pos[1] - obstacle.start_pos[1]) / 2):
        return False

    if circle_distance_x <= (obstacle.end_pos[0] - obstacle.start_pos[0]) / 2:
        return True
    if circle_distance_y <= (obstacle.end_pos[1] - obstacle.start_pos[1]) / 2:
        return True

    corner_distance_sq = (circle_distance_x - (obstacle.end_pos[0] - obstacle.start_pos[0]) / 2) ** 2 + (circle_distance_y - (obstacle.end_pos[1] - obstacle.start_pos[1]) / 2) ** 2

    return corner_distance_sq <= (ball_radius ** 2)

    def update_speed_on_collision(ball, obstacle):
        dx = obstacle.end_pos[0] - obstacle.start_pos[0]
        dy = obstacle.end_pos[1] - obstacle.start_pos[1]

        normal_x = dy
        normal_y = -dx

        normal_length = (normal_x ** 2 + normal_y ** 2) ** 0.5
        normal_x /= normal_length
        normal_y /= normal_length

        dot_product = ball.speed[0] * normal_x + ball.speed[1] * normal_y

        new_speed_x = ball.speed[0] - 2 * dot_product * normal_x
        new_speed_y = ball.speed[1] - 2 * dot_product * normal_y

        return [new_speed_x, new_speed_y]

def collide_balls(ball1, ball2):
    distance = np.linalg.norm(np.array(ball1.pos) - np.array(ball2.pos))
    if distance <= ball1.radius + ball2.radius:
        normal_vec = np.array(ball1.pos) - np.array(ball2.pos)
        normal_vec = normal_vec / np.linalg.norm(normal_vec)

        reflection1 = np.array(ball1.speed) - 2 * np.dot(np.array(ball1.speed), normal_vec) * normal_vec
        reflection2 = np.array(ball2.speed) + 2 * np.dot(np.array(ball2.speed), normal_vec) * normal_vec

        ball1.speed = list(reflection1)
        ball2.speed = list(reflection2)



class Ball:
    def __init__(self, pos, speed, radius, lifetime):
        self.pos = np.array(pos)
        self.speed = [speed_x, speed_y]
        self.lifetime = lifetime
        self.bounce_count = 0 
        self.radius = ball_radius
        self.note_off_time = None

    def collides_with_line(self, line_start, line_end):
        line_vec = np.array(line_end) - np.array(line_start)
        ball_vec = np.array(self.pos) - np.array(line_start)
        line_length = np.linalg.norm(line_vec)

        if line_length == 0:
            return False, None

        projection_length = np.dot(ball_vec, line_vec) / line_length
        projection_vec = (projection_length / line_length) * line_vec
        closest_point = line_start + projection_vec

        # 線分の端点の外側に最も近い点がある場合は、端点への距離を考慮
        if projection_length < 0:
            closest_point = line_start
        elif projection_length > line_length:
            closest_point = line_end

        distance_to_line = np.linalg.norm(np.array(self.pos) - closest_point)

        if distance_to_line <= self.radius:
            normal_vec = np.array(self.pos) - closest_point
            normal_vec = normal_vec / np.linalg.norm(normal_vec)
            return True, normal_vec
        return False, None





    def apply_wind_force(self, wind_strength, wind_direction):
        scaling_factor = 50
        if wind_direction == 0:
            wind_force = np.random.uniform(-wind_strength, wind_strength) / scaling_factor
        elif wind_direction == 1:
            wind_force = -wind_strength / scaling_factor
        else:
            wind_force = wind_strength / scaling_factor

        self.speed[0] += wind_force



    def update(self, gravity):
        self.apply_wind_force(wind_strength_slider.get(), wind_direction_slider.get())
        self.speed[1] += gravity 
        self.pos[0] += self.speed[0] 
        self.pos[1] += self.speed[1] 



balls: List[Ball] = []

min_radius = 10
max_radius = 30



def spawn_ball(position, note_choices, color_choices, gravity, friction, fall_speed, ball_lifetime, outport, selected_scale):
    global balls
    ball = Ball(
        position[0],
        position[1],
        random.choice(note_choices),
        random.uniform(min_radius, max_radius),
        random.choice(color_choices),
        gravity,
        friction,
        fall_speed,
        ball_lifetime,
    )
    balls.append(ball)
    ball.play_sound(outport, selected_scale)

class Obstacle:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos

    def draw(self, screen):
        pygame.draw.line(screen, (255, 255, 255), self.start_pos, self.end_pos, 5)

    def draw_point(self, screen, pos):
        pygame.draw.circle(screen, (255, 255, 255), pos, 5)

obstacles = []
drawing_point = False
current_obstacle_start = None
current_obstacle_end = None
ball_spawn_enabled = True
clock = pygame.time.Clock()

while True:
    time_delta = clock.tick(60) / 1000.0


    bounce_threshold = bounce_threshold_slider.get_current_value()
    ball_spawn_rate = ball_spawn_rate_slider.get_current_value()
    note_length_min = note_length_min_slider.get_current_value()
    note_length_max = note_length_max_slider.get_current_value()

    if note_length_min > note_length_max:
        note_length_min, note_length_max = note_length_max, note_length_min

    random_note_length = random.randint(note_length_min, note_length_max)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                if not drawing_point:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    current_obstacle_start = (mouse_x, mouse_y)
                    drawing_point = True
                else:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    obstacles.append(Obstacle(current_obstacle_start, (mouse_x, mouse_y)))
                    current_obstacle_start = None
                    drawing_point = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            for i, obstacle in enumerate(obstacles):
                if (abs(obstacle.start_pos[0] - event.pos[0]) <= 5 and
                        abs(obstacle.start_pos[1] - event.pos[1]) <= 5):
                    obstacles.pop(i)
                    break        

        if event.type == USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == reset_button:
                    balls = []
                    obstacles = []  

                if event.ui_element == start_stop_button:
                    ball_spawn_enabled = not ball_spawn_enabled

            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == scale_dropdown:
                    selected_scale = event.text
                if event.ui_element == midi_port_selector:
                    selected_port_name = midi_port_selector.selected_option
                    outport = mido.open_output(selected_port_name)

            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == friction_slider:
                    friction = friction_slider.get_current_value()
                elif event.ui_element == fall_speed_slider:
                    fall_speed = fall_speed_slider.get_current_value()
                elif event.ui_element == ball_lifetime_slider:
                    ball_lifetime = ball_lifetime_slider.get_current_value()
                elif event.ui_element == gravity_slider:
                    gravity = gravity_slider.get_current_value()
                elif event.ui_element == bounce_threshold_slider:
                    bounce_threshold = bounce_threshold_slider.get_current_value()
                elif event.ui_element == ball_spawn_rate_slider:
                    ball_spawn_rate = ball_spawn_rate_slider.get_current_value()
                elif event.ui_element == exponent_slider:
                    exponent = exponent_slider.get_current_value()

               

        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    for ball in balls:
        ball.apply_wind_force(wind_strength_slider.get_current_value(), wind_direction_slider.get_current_value())
        ball.speed[1] += gravity_slider.get_current_value()
        ball.pos[0] += ball.speed[0]
        ball.pos[1] += ball.speed[1]
        ball.lifetime -= 1

        if ball.note_off_time is not None and time.time() >= ball.note_off_time:
            outport.send(
                mido.Message(
                    "note_off", channel=0, note=note_number, velocity=velocity, time=0
                )
            )
            ball.note_off_time = None


    collision_checks = 5

    # メインループ内でボールの更新処理を行う部分
    for ball in balls:
        ball.apply_wind_force(wind_strength_slider.get_current_value(), wind_direction_slider.get_current_value())
        ball.speed[1] += gravity_slider.get_current_value()

        for _ in range(collision_checks):
            # ボールの移動距離を分割して更新
            new_pos = ball.pos + np.array(ball.speed) / collision_checks

            for obstacle in obstacles:
                collision, normal_vec = ball.collides_with_line(obstacle.start_pos, obstacle.end_pos)
                if collision:
                    reflection = np.array(ball.speed) - 2 * np.dot(np.array(ball.speed), normal_vec) * normal_vec
                    ball.speed = list(reflection)
                    new_pos = ball.pos + np.array(ball.speed) / collision_checks
                    break

            ball.pos = new_pos

        ball.lifetime -= 1



        if ball.pos[1] + ball_radius >= screen_height:
            ball.speed[1] = -ball.speed[1] * (1 - friction_slider.get_current_value()) * 2.0
            ball.pos[1] = screen_height - ball_radius
            bounce_height = abs(ball.speed[1])

            if bounce_height > bounce_threshold:
                if not hasattr(ball, "note_played") or ball.bounce_count > 1:  
                    note_number = get_note_number(ball.pos[0])
                    ball_speed_magnitude = np.sqrt(ball.speed[0] ** 2 + ball.speed[1] ** 2)
                    exponent = exponent_slider.get_current_value()
                    velocity = int(
                        np.interp(
                            ball_speed_magnitude ** exponent,
                            [0, 10 ** exponent],
                            [
                                velocity_min_slider.get_current_value(),
                                velocity_max_slider.get_current_value(),
                            ],
                        )
                    )
                    play_note_async(ball, note_number, velocity, random_note_length)
                    ball.note_played = True
                    note_name = get_note_name_for_x_pos(ball.pos[0])
                    print(f"AXIS: x={ball.pos[0]}, VELOCITY: {velocity}, NOTE: {note_name}, NOTE LENGTH: {random_note_length}")



            elif ball.pos[1] + ball_radius < screen_height:
                ball.note_played = False
                

            ball.bounce_count += 1 

            bounce_height = abs(ball.speed[1])


            if bounce_height > bounce_threshold:
                if not hasattr(ball, "note_played") or ball.bounce_count > 1:  
                    note_number = get_note_number(ball.pos[0])
                    play_note_async(ball, note_number, velocity, random_note_length)
                    ball.note_played = True
            elif ball.pos[1] + ball_radius < screen_height:
                ball.note_played = False

            for i, ball1 in enumerate(balls):
                for ball2 in balls[i + 1:]:
                    collide_balls(ball1, ball2)


    if random.random() < ball_spawn_rate * 0.01:
        angle = random.uniform(0, 2 * 3.14159265) 
        speed = fall_speed_slider.get_current_value()
        speed_x = speed * random.uniform(0.5, 1.5) * random.choice([-1, 1]) * 0.2
        speed_y = -speed * random.uniform(0.5, 1.5) * 0.2
        lifetime = ball_lifetime_slider.get_current_value()
        new_ball = Ball((screen_width // 2, screen_height // 3.5), (speed_x, speed_y), ball_radius, lifetime)
        balls.append(new_ball)

    screen.fill((50, 50, 50))  

    balls[:] = [ball for ball in balls if ball.lifetime > 0]
    for ball in balls:
        pygame.draw.circle(
            screen, ball_color, (int(ball.pos[0]), int(ball.pos[1])), ball_radius
        )


    for obstacle in obstacles:
        obstacle.draw(screen)
        pygame.draw.circle(screen, (255, 128, 128), obstacle.start_pos, 3)

    if drawing_point:
        pygame.draw.circle(screen, (255, 128, 128), current_obstacle_start, 3)

    note_display_font = pygame.font.Font(None, 20)

    for x_pos in range(0, screen_width, 50):
        note_name = get_note_name_for_x_pos(x_pos)
        note_display_text = note_display_font.render(note_name, True, (200, 200, 200))
        screen.blit(note_display_text, (x_pos, screen_height - 30))

    ui_manager.draw_ui(screen)

    pygame.display.flip()
