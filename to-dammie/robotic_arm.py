import pygame
import math

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
screen_width, screen_height = 1000, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Box Swapping Animation')

# Box properties
box_width = 80
box_height = 100
box_gap = 20

# Colors
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

# Box labels
labels = ['A', 'B', 'C', 'D']

# Calculate stack position
stack_x = 50
stack_y = screen_height // 2 - ((len(colors) * (box_height + box_gap)) // 2)

# Box positions
boxes = []
for i, color in enumerate(colors):
    box_x = stack_x
    box_y = stack_y + i * (box_height + box_gap)
    boxes.append({'label': labels[i], 'color': color, 'position': (box_x, box_y)})

# Animation properties
animation_speed = 2  # Lower value for slower animation
frame_delay = 60 // animation_speed

# Robotic arm properties
arm_base_x = 850
arm_base_y = 200
arm_height = (len(colors) - 1) * (box_height + box_gap)
arm_thickness = 20
arm_color = (60, 60, 60)
gripper_size = 30
gripper_color = (200, 200, 200)

# Arm joint angles
base_angle = 0
segment_angle = 0

# Perform the box swap animation
def swap_boxes(box_a_index, box_b_index):
    global base_angle, segment_angle
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 2000:  # 2 seconds for the animation
        for i in range(frame_delay):
            screen.fill((255, 255, 255))

            # Update box positions
            if i < frame_delay // 2:
                boxes[box_a_index]['position'] = (
                    boxes[box_a_index]['position'][0],
                    boxes[box_a_index]['position'][1] + 1
                )
                boxes[box_b_index]['position'] = (
                    boxes[box_b_index]['position'][0],
                    boxes[box_b_index]['position'][1] - 1
                )
            else:
                boxes[box_a_index]['position'] = (
                    boxes[box_a_index]['position'][0],
                    boxes[box_a_index]['position'][1] - 1
                )
                boxes[box_b_index]['position'] = (
                    boxes[box_b_index]['position'][0],
                    boxes[box_b_index]['position'][1] + 1
                )

            # Calculate arm angles
            target_angle = math.degrees(math.atan2(boxes[box_a_index]['position'][1] - arm_base_y, arm_base_x - boxes[box_a_index]['position'][0]))
            base_angle = (base_angle + target_angle) / 2
            segment_angle = target_angle - base_angle

            # Draw boxes and labels
            for box in boxes:
                pygame.draw.rect(screen, box['color'], (box['position'][0], box['position'][1], box_width, box_height))
                font = pygame.font.SysFont(None, 24)
                label_text = font.render(box['label'], True, (0, 0, 0))
                label_position = (
                    box['position'][0] + box_width // 2 - label_text.get_width() // 2,
                    box['position'][1] + box_height // 2 - label_text.get_height() // 2
                )
                screen.blit(label_text, label_position)

            # Draw robotic arm
            pygame.draw.rect(screen, arm_color, (arm_base_x, arm_base_y, arm_thickness, arm_height))
            pygame.draw.line(screen, arm_color, (arm_base_x + arm_thickness // 2, arm_base_y),
                             (arm_base_x + arm_thickness // 2, arm_base_y + arm_height), arm_thickness)
            pygame.draw.line(screen, arm_color, (arm_base_x + arm_thickness // 2, arm_base_y + arm_height),
                             (boxes[box_a_index]['position'][0] + box_width // 2, boxes[box_a_index]['position'][1]), arm_thickness)
            pygame.draw.line(screen, arm_color, (arm_base_x + arm_thickness // 2, arm_base_y + arm_height),
                             (boxes[box_b_index]['position'][0] + box_width // 2, boxes[box_b_index]['position'][1]), arm_thickness)
            pygame.draw.rect(screen, gripper_color, (boxes[box_a_index]['position'][0] + box_width // 2 - gripper_size // 2,
                                                     boxes[box_a_index]['position'][1], gripper_size, gripper_size))
            pygame.draw.rect(screen, gripper_color, (boxes[box_b_index]['position'][0] + box_width // 2 - gripper_size // 2,
                                                     boxes[box_b_index]['position'][1], gripper_size, gripper_size))

            pygame.display.flip()
            clock.tick(60)  # Set the frame rate

    # Swap box colors
    boxes[box_a_index]['color'], boxes[box_b_index]['color'] = boxes[box_b_index]['color'], boxes[box_a_index]['color']


# Get the index of a box based on its label
def get_box_index(label):
    return labels.index(label)

# Pygame main loop
running = True
selected_box = None
show_robotic_arm = True  # Flag to show/hide robotic arm
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, box in enumerate(boxes):
                box_x, box_y = box['position']
                if box_x <= mouse_x <= box_x + box_width and box_y <= mouse_y <= box_y + box_height:
                    if selected_box is None:
                        selected_box = i
                    else:
                        if selected_box != i:
                            show_robotic_arm = False  # Hide robotic arm during the swap
                            swap_boxes(selected_box, i)
                            boxes[selected_box]['label'], boxes[i]['label'] = boxes[i]['label'], boxes[selected_box]['label']
                            show_robotic_arm = True  # Show robotic arm after the swap
                        selected_box = None

    # Draw boxes and labels
    for box in boxes:
        pygame.draw.rect(screen, box['color'], (box['position'][0], box['position'][1], box_width, box_height))
        font = pygame.font.SysFont(None, 24)
        label_text = font.render(box['label'], True, (0, 0, 0))
        label_position = (
            box['position'][0] + box_width // 2 - label_text.get_width() // 2,
            box['position'][1] + box_height // 2 - label_text.get_height() // 2
        )
        screen.blit(label_text, label_position)

    # Draw robotic arm if the flag is set
    if show_robotic_arm:
        pygame.draw.rect(screen, arm_color, (arm_base_x, arm_base_y, arm_thickness, arm_height))
        pygame.draw.line(screen, arm_color, (arm_base_x + arm_thickness // 2, arm_base_y),
                         (arm_base_x + arm_thickness // 2, arm_base_y + arm_height), arm_thickness)

    pygame.display.flip()
    clock.tick(60)  # Set the frame rate

# Clean up and quit Pygame
pygame.quit()
