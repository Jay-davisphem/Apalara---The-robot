import unittest
import pygame
from apalara import Box, RoboticArm, BoxSwappingAnimation


class BoxSwappingAnimationTests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((800, 600))

    def tearDown(self):
        pygame.quit()

    def test_box_draw(self):
        box = Box("A", (255, 0, 0), (100, 100), 80, 100)
        screen = pygame.Surface((800, 600))
        box.draw(screen)

        # Assert that the box is drawn correctly
        self.assertEqual(screen.get_at((100, 100)), (255, 0, 0))

    def test_robotic_arm_draw(self):
        arm = RoboticArm(200, 200, 300, 20, (60, 60, 60))
        screen = pygame.Surface((800, 600))
        animation = BoxSwappingAnimation()
        animation.screen = screen
        animation.show_robotic_arm = True
        animation.draw_robotic_arm()

        # Assert that the robotic arm is drawn correctly
        self.assertEqual(screen.get_at((190, 200)), (0, 0, 0, 255))

    def test_get_selected_box(self):
        animation = BoxSwappingAnimation()
        animation.boxes = [
            Box("A", (255, 0, 0), (100, 100), 80, 100),
            Box("B", (0, 255, 0), (200, 200), 80, 100),
        ]

        # Simulate selecting the first box
        selected_box = animation.get_selected_box(110, 110)

        # Assert that the correct box is selected
        self.assertEqual(selected_box, 0)

    # Add more test methods to cover other functionality

if __name__ == '__main__':
    unittest.main()
