import pygame
import sys
import numpy as np
from math import comb
import mido
from mido import Message


class MIDIController:
    def __init__(self, port=1, channel=1):
        self.port = port
        self.channel = channel - 1
        self.port_name = mido.get_output_names()[self.port - 1]
        print(f"Available MIDI output ports: {mido.get_output_names()}")  # 追加
        self.out_port = mido.open_output(self.port_name)

    def send_mackie_control_message(self, value, msg_type="pitchwheel", cc_number=91):
        print("send_mackie_control_message called")  # 追加
        try:
            if msg_type in ['control_change', 'note_on', 'note_off', 'aftertouch', 'polytouch']:
                msg = mido.Message(msg_type, control=cc_number, value=value, channel=self.channel)
            elif msg_type == 'pitchwheel':
                # Convert the value to a valid pitchwheel value (-8192 to 8191)
                value = value - 8192
                msg = mido.Message(msg_type, pitch=value, channel=self.channel)
            else:
                raise ValueError("Invalid message type")

            print(f"Sending MIDI message to port: {self.port_name}, channel: {self.channel}, cc_number: {cc_number}, value: {value}")
            self.out_port.send(msg)
            print(f"Sent MIDI CC Value {value}")

        except ValueError:
            # Ignore if the input is not a valid integer
            pass
        except IndexError:  # Handle the case when the selected port number is not available
            print(f"Invalid port number: {self.port}")
            pass


    def __del__(self):
        self.out_port.close()

midi_controller = MIDIController()

def bezier_point(t, control_points):
    n = len(control_points) - 1
    x = sum((1 - t) ** (n - i) * t ** i * p[0] * comb(n, i) for i, p in enumerate(control_points))
    y = sum((1 - t) ** (n - i) * t ** i * p[1] * comb(n, i) for i, p in enumerate(control_points))
    return x, y


pygame.init()

screen = pygame.display.set_mode((800, 1024))  # 縦 1024 ドットに変更
pygame.display.set_caption("Bezier Curve")

start_point = (0, 512)
end_point = (800, 512)
control_points = [start_point, end_point]

running = True
dragging = False
dragged_point_idx = None

go_button = pygame.Rect(10, 360, 50, 30)
go_button_color = (102, 204, 102)
go_button_pressed = False
moving_dot = False
dot_position = 0

clock = pygame.time.Clock()

while running:
    time_delta = clock.tick(60) / 1000.0
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for idx, point in enumerate(control_points):
                    if abs(event.pos[0] - point[0]) < 10 and abs(event.pos[1] - point[1]) < 10:
                        dragging = True
                        dragged_point_idx = idx

                if go_button.collidepoint(event.pos):
                    go_button_pressed = True

            elif event.button == 3:  # Right-click
                modifiers = pygame.key.get_mods()
                if modifiers & pygame.KMOD_SHIFT:
                    # Add a control point
                    control_points.insert(-1, event.pos)
                elif modifiers & pygame.KMOD_ALT:
                    # Remove a control point
                    for idx, point in enumerate(control_points):
                        if abs(event.pos[0] - point[0]) < 10 and abs(event.pos[1] - point[1]) < 10:
                            control_points.pop(idx)
                            break

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
                dragged_point_idx = None

                if go_button_pressed and go_button.collidepoint(event.pos):
                    moving_dot = True
                    dot_position = 0
                    go_button_pressed = False
                    moving_time = 4

        if event.type == pygame.MOUSEMOTION:
            if dragging:
                new_pos = event.pos
                if dragged_point_idx == 0 or dragged_point_idx == len(control_points) - 1:
                    new_pos = (control_points[dragged_point_idx][0], event.pos[1])
                control_points[dragged_point_idx] = new_pos

    for point in control_points:
        pygame.draw.circle(screen, (255, 0, 0), point, 5)

    for t in np.linspace(0, 1, 1000):
        x, y = bezier_point(t, control_points)
        pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 1)

    pygame.draw.rect(screen, go_button_color, go_button)
    font = pygame.font.SysFont('Arial', 14)
    go_text = font.render("Go", True, (0, 0, 0))
    go_text_rect = go_text.get_rect(center=go_button.center)
    screen.blit(go_text, go_text_rect)

    if moving_dot:
        t = dot_position / (moving_time * 60)
        if t > 1:
            moving_dot = False
        else:
            x, y = bezier_point(t, control_points)
            pygame.draw.circle(screen, (128, 128, 128), (int(x), int(y)), 5)
            dot_position += 1

            output_count = 32000
            if dot_position % (moving_time * 60 / output_count) < 1:
                value = int((1 - (y / 1024)) * 16383)  # 縦 1024 ドットの範囲を使用
                value = (value // 16) * 16  # 数値を 0 または 16 の倍数にする
                print("Calling send_mackie_control_message")
                midi_controller.send_mackie_control_message(value)
                print(f"dot_position: {dot_position}, value: {value}")

    pygame.display.flip()

pygame.quit()
