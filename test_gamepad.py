import pygame
import time

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Gamepad tidak ditemukan")
    exit()

joy = pygame.joystick.Joystick(0)
joy.init()

print("Nama :", joy.get_name())

while True:

    pygame.event.pump()

    print("\033[2J\033[H", end="")

    print("===== AXIS =====")

    for i in range(joy.get_numaxes()):
        print(f"Axis {i} : {joy.get_axis(i):.2f}")

    print("\n===== BUTTON =====")

    for i in range(joy.get_numbuttons()):
        if joy.get_button(i):
            print("Button", i)

    print("\n===== HAT =====")

    print(joy.get_hat(0))

    time.sleep(0.05)