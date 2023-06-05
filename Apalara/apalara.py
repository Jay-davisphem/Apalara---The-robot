import pygame
import math


class Box:
    def __init__(self, label, color, position, width, height):
        self.label = label
        self.color = color
        self.position = position
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.position[0], self.position[1], self.width, self.height))
        font = pygame.font.SysFont(None, 24)
        label_text = font.render(self.label, True, (0, 0, 0))
        label_position = (
            self.position[0] + self.width // 2 - label_text.get_width() // 2,
            self.position[1] + self.height // 2 - label_text.get_height() // 2
        )
        screen.blit(label_text, label_position)


class RoboticArm:
    def __init__(self, base_x, base_y, height, thickness, color):
        self.base_x = base_x
        self.base_y = base_y
        self.height = height
        self.thickness = thickness
        self.color = color


class BoxSwappingAnimation:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen_width, self.screen_height = 1000, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Box Swapping Animation')

        # Box properties
        self.box_width = 80
        self.box_height = 100
        self.box_gap = 20

        # Colors
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

        # Box labels
        self.labels = ['A', 'B', 'C', 'D']

        # Calculate stack position
        self.stack_x = 50
        self.stack_y = self.screen_height // 2 - ((len(self.colors) * (self.box_height + self.box_gap)) // 2)

        # Create boxes
        self.boxes = []
        for i, color in enumerate(self.colors):
            box_x = self.stack_x
            box_y = self.stack_y + i * (self.box_height + self.box_gap)
            box = Box(self.labels[i], color, (box_x, box_y), self.box_width, self.box_height)
            self.boxes.append(box)

        # Animation properties
        self.animation_speed = 2  # Lower value for slower animation
        self.frame_delay = 60 // self.animation_speed

        # Robotic arm properties
        self.arm_base_x = 850
        self.arm_base_y = 200
        self.arm_height = (len(self.colors) - 1) * (self.box_height + self.box_gap)
        self.arm_thickness = 20
        self.arm_color = (60, 60, 60)
        self.gripper_size = 30
        self.gripper_color = (200, 200, 200)

        # Arm joint angles
        self.base_angle = 0
        self.segment_angle = 0

        # Drag and drop variables
        self.selected_box = None
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

        # Flag to show/hide robotic arm
        self.show_robotic_arm = True

    def reset_boxes(self):
        for i, box in enumerate(self.boxes):
            box_x = self.stack_x
            box_y = self.stack_y + i * (self.box_height + self.box_gap)
            box.position = (box_x, box_y)
    def reorder_boxes(self, descending=True):
        self.boxes.sort(key=lambda box: box.label, reverse=descending)
        self.reset_boxes()

    def run(self):
        # Pygame main loop
        running = True
        while running:
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_boxes()
                    elif event.key == pygame.K_d:
                        self.reorder_boxes()
                    elif event.key == pygame.K_a:
                        self.reorder_boxes(False)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.selected_box = self.get_selected_box(mouse_x, mouse_y)
                    if self.selected_box is not None:
                        self.dragging = True
                        self.offset_x = mouse_x - self.boxes[self.selected_box].position[0]
                        self.offset_y = mouse_y - self.boxes[self.selected_box].position[1]
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.selected_box is not None:
                        self.dragging = False
                        self.selected_box = None

            if self.dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.boxes[self.selected_box].position = (mouse_x - self.offset_x, mouse_y - self.offset_y)

            # Draw boxes and labels
            for box in self.boxes:
                box.draw(self.screen)

            # Draw robotic arm if the flag is set
            if self.show_robotic_arm:
                self.draw_robotic_arm()

            pygame.display.flip()
            try:
                    self.clock.tick(60)  # Set the frame rate
            except:
                    print("\nExisting Forcefully ...")
                    return

        # Clean up and quit Pygame
        pygame.quit()

    def get_selected_box(self, mouse_x, mouse_y):
        for i, box in enumerate(self.boxes):
            box_x, box_y = box.position
            if box_x <= mouse_x <= box_x + self.box_width and box_y <= mouse_y <= box_y + self.box_height:
                return i
        return None

    def draw_robotic_arm(self):
        arm_base_x = self.arm_base_x - self.arm_thickness // 2  # Adjust base position
        pygame.draw.rect(self.screen, self.arm_color,
                         (arm_base_x, self.arm_base_y, self.arm_thickness, self.arm_height))

        # Calculate segment position and angle
        segment_length = self.box_height * 5 + self.box_gap
        segment_start = (arm_base_x + self.arm_thickness // 2, self.arm_base_y)
        segment_end = (segment_start[0] - segment_length * math.cos(math.radians(self.segment_angle)),
                       segment_start[1] - segment_length * math.sin(math.radians(self.segment_angle)))  # Adjust y-coordinate

        pygame.draw.line(self.screen, self.arm_color, segment_start, segment_end, self.arm_thickness)



    def swap_boxes(self, box_a_index, box_b_index):
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 2000:  # 2 seconds for the animation
            for i in range(self.frame_delay):
                self.screen.fill((255, 255, 255))

                # Update box positions
                if i < self.frame_delay // 2:
                    self.boxes[box_a_index].position = (
                        self.boxes[box_a_index].position[0],
                        self.boxes[box_a_index].position[1] + 1
                    )
                    self.boxes[box_b_index].position = (
                        self.boxes[box_b_index].position[0],
                        self.boxes[box_b_index].position[1] - 1
                    )
                else:
                    self.boxes[box_a_index].position = (
                        self.boxes[box_a_index].position[0],
                        self.boxes[box_a_index].position[1] - 1
                    )
                    self.boxes[box_b_index].position = (
                        self.boxes[box_b_index].position[0],
                        self.boxes[box_b_index].position[1] + 1
                    )

                # Calculate arm angles
                target_angle = math.degrees(math.atan2(
                    self.boxes[box_b_index].position[1] - self.boxes[box_a_index].position[1],
                    self.boxes[box_b_index].position[0] - self.boxes[box_a_index].position[0]
                ))
                self.base_angle = self.base_angle + (target_angle - self.base_angle) / 10
                self.segment_angle = math.degrees(math.atan2(
                    self.boxes[box_b_index].position[1] - self.boxes[box_a_index].position[1],
                    self.boxes[box_b_index].position[0] - self.boxes[box_a_index].position[0]
                ))

                # Draw boxes and labels
                for box in self.boxes:
                    box.draw(self.screen)

                # Draw robotic arm
                self.draw_robotic_arm()

                pygame.display.flip()
                try:
                    self.clock.tick(60)  # Set the frame rate
                except:
                    print("\nExisting Forcefully ...")
                    return