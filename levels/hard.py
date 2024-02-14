import pygame
import random
import os
from pygame.locals import *

root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
move_tiles_sound = os.path.join(root_dir, "sounds", "move_tiles.wav")
congratulations = os.path.join(
    root_dir, "puzzle_simple_game/congratulations", "congratulations_window.py"
)
background_image_path = os.path.join(
    root_dir, "../puzzle_simple_game/images", "background_image.jpg")


class Tiles:
    # main method for initializing different variables
    def __init__(
        self, screen, start_position_x, start_position_y, num, mat_pos_x, mat_pos_y
    ):
        self.color = (75, 0, 130)  # Indigo color
        self.screen = screen
        self.start_pos_x = start_position_x
        self.start_pos_y = start_position_y
        self.num = num
        self.width = tile_width
        self.depth = tile_depth
        self.selected = False
        self.position_x = mat_pos_x
        self.position_y = mat_pos_y
        self.movable = False

    # Draw tiles
    def draw_tile(self):
        if self.selected:
            tile_color = (255, 0, 0)  # Red color when selected
        else:
            tile_color = (75, 0, 130)  # Indigo color when not selected

        pygame.draw.rect(
            self.screen,
            tile_color,
            pygame.Rect(self.start_pos_x, self.start_pos_y,
                        self.width, self.depth),
        )
        numb = font.render(str(self.num), True, (255, 255, 255))  # White color
        text_rect = numb.get_rect(
            center=(
                self.start_pos_x + self.width // 2,
                self.start_pos_y + self.depth // 2,
            )
        )
        screen.blit(numb, text_rect)

    # Mouse hover change the color of tiles
    def mouse_hover(self, x_m_motion, y_m_motion):
        if (
            x_m_motion > self.start_pos_x
            and x_m_motion < self.start_pos_x + self.width
            and y_m_motion > self.start_pos_y
            and y_m_motion < self.start_pos_y + self.depth
        ):
            self.color = (255, 255, 255)
        else:
            self.color = (255, 165, 0)

    # when mouse clicks check if a tile is selected or not
    def mouse_click(self, x_m_click, y_m_click):
        if (
            x_m_click > self.start_pos_x
            and x_m_click < self.start_pos_x + self.width
            and y_m_click > self.start_pos_y
            and y_m_click < self.start_pos_y + self.depth
        ):
            self.selected = True
        else:
            self.selected = False

    # when mouse click released unselect the tile by setting False
    def mouse_click_release(self, x_m_click_rel, y_m_click_rel):
        if x_m_click_rel > 0 and y_m_click_rel > 0:
            self.selected = False

    # Move the tile(i.e hover)
    def move_tile(self, x_m_motion, y_m_motion):
        self.start_pos_x = x_m_motion
        self.start_pos_y = y_m_motion


page_width, page_depth = 800, 600
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(
    background_image, (page_width, page_depth))

# Create tiles w.r.t to no of tiles available


def create_tiles():
    i = 1
    while i <= tile_count:
        r = random.randint(1, tile_count)
        if r not in tile_no:
            tile_no.append(r)
            i += 1
    tile_no.append("")
    k = 0
    for i in range(0, rows):
        for j in range(0, cols):
            if (i == rows - 1) and (j == cols - 1):
                pass
            else:
                t = Tiles(
                    screen,
                    tile_print_position[(i, j)][0],
                    tile_print_position[(i, j)][1],
                    tile_no[k],
                    i,
                    j,
                )
                tiles.append(t)
            matrix[i][j] = tile_no[k]
            k += 1
    check_mobility()


def check_mobility():
    for i in range(tile_count):
        tile = tiles[i]
        row_index = tile.position_x
        col_index = tile.position_y
        adjacent_cells = []
        adjacent_cells.append([row_index - 1, col_index, False])  # up
        adjacent_cells.append([row_index + 1, col_index, False])  # down
        adjacent_cells.append([row_index, col_index - 1, False])  # right
        adjacent_cells.append([row_index, col_index + 1, False])  # left
        for i in range(len(adjacent_cells)):
            if (adjacent_cells[i][0] >= 0 and adjacent_cells[i][0] < rows) and (
                adjacent_cells[i][1] >= 0 and adjacent_cells[i][1] < cols
            ):
                adjacent_cells[i][2] = True

        for j in range(len(adjacent_cells)):
            if adjacent_cells[j][2]:
                adj_cell_row = adjacent_cells[j][0]
                adj_cell_col = adjacent_cells[j][1]
                for k in range(tile_count):
                    if (
                        adj_cell_row == tiles[k].position_x
                        and adj_cell_col == tiles[k].position_y
                    ):
                        adjacent_cells[j][2] = False

                false_count = 0

                for m in range(len(adjacent_cells)):
                    if adjacent_cells[m][2]:
                        tile.movable = True
                        break
                    else:
                        false_count += 1

                if false_count == 4:
                    tile.movable = False


def is_game_over():
    global game_over, game_over_banner
    all_cell_data = ""
    for i in range(rows):
        for j in range(cols):
            all_cell_data = all_cell_data + str(matrix[i][j])

    if all_cell_data == "1234567891011 ":
        game_over = True
        game_over_banner = "Game Over"

        print("Game Over")

        for i in range(tile_count):
            tiles[i].movable = False
            tiles[i].selected = False


# Window dimension
page_width, page_depth = 800, 600

# tile dimensions
tiles = []
tile_width = 160
tile_depth = 160

# no of rows & column i.e puzzle size
rows, cols = (3, 4)  # 3 rows, 4 columns for 12 tiles
tile_count = rows * cols - 1  # how many tiles should be created
matrix = [["" for i in range(cols)] for j in range(rows)]
tile_no = []
# calculate position of red container
red_container_width = cols * tile_width
red_container_height = rows * tile_depth
red_container_x = (page_width - red_container_width) // 2
red_container_y = (page_depth - red_container_height) // 2
tile_print_position = {
    (0, 0): (red_container_x, red_container_y),
    (0, 1): (red_container_x + tile_width, red_container_y),
    (0, 2): (red_container_x + 2 * tile_width, red_container_y),
    (0, 3): (red_container_x + 3 * tile_width, red_container_y),
    (1, 0): (red_container_x, red_container_y + tile_depth),
    (1, 1): (red_container_x + tile_width, red_container_y + tile_depth),
    (1, 2): (red_container_x + 2 * tile_width, red_container_y + tile_depth),
    (1, 3): (red_container_x + 3 * tile_width, red_container_y + tile_depth),
    (2, 0): (red_container_x, red_container_y + 2 * tile_depth),
    (2, 1): (red_container_x + tile_width, red_container_y + 2 * tile_depth),
    (2, 2): (red_container_x + 2 * tile_width, red_container_y + 2 * tile_depth),
    (2, 3): (red_container_x + 3 * tile_width, red_container_y + 2 * tile_depth),
}

# initial values of variables
mouse_press = False
x_m_click, y_m_click = 0, 0
x_m_click_rel, y_m_click_rel = 0, 0
game_over = False
game_over_banner = ""

# initialize pygame and set the caption
pygame.init()
game_over_font = pygame.font.Font("freesansbold.ttf", 70)
screen = pygame.display.set_mode((page_width, page_depth))
pygame.display.set_caption("Puzzle Game 2024 [Hard Mode]")
font = pygame.font.Font("freesansbold.ttf", 100)

# Load the sound files
move_title_sound = pygame.mixer.Sound(move_tiles_sound)
# creation of tiles in the puzzle
create_tiles()

running = True
while running:
    screen.blit(background_image, (0, 0))  # Draw the background image

    # Get events from the queue.
    for event in pygame.event.get():
        # if its quite operation then exit the while loop
        if event.type == pygame.QUIT:
            running = False
        # if mouse click are detected then find (x,y)
        # and then pass them to mouse_hover method
        if event.type == pygame.MOUSEMOTION:
            x_m_motion, y_m_motion = pygame.mouse.get_pos()
            for i in range(tile_count):
                tiles[i].mouse_hover(x_m_motion, y_m_motion)
            # if the tile is selected & mouse is pressed
            # then pass the coords to move_tile method
            for i in range(tile_count):
                if tiles[i].selected and mouse_press:
                    tiles[i].move_tile(x_m_motion, y_m_motion)
        # Moving tile downwards
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_press = True
            x_m_click, y_m_click = pygame.mouse.get_pos()
            move_title_sound.play()  # Play sound when a tile is clicked
            for i in range(tile_count):
                tiles[i].mouse_click(x_m_click, y_m_click)
        # Moving tile upwards
        if event.type == pygame.MOUSEBUTTONUP:

            mouse_press = False
            x_m_click_rel, y_m_click_rel = pygame.mouse.get_pos()
            x_m_click, y_m_click = 0, 0
            cell_found = False
            for i in range(0, rows):
                for j in range(0, cols):
                    tile_start_pos_x = tile_print_position[(i, j)][0]
                    tile_start_pos_y = tile_print_position[(i, j)][1]

                    if (
                        x_m_click_rel > tile_start_pos_x
                        and x_m_click_rel < tile_start_pos_x + tile_width
                    ) and (
                        y_m_click_rel > tile_start_pos_y
                        and y_m_click_rel < tile_start_pos_y + tile_depth
                    ):
                        if matrix[i][j] == "":
                            for k in range(tile_count):
                                if game_over == False:
                                    if tiles[k].selected:
                                        if tiles[k].movable:
                                            cell_found = True
                                            dummy = matrix[tiles[k].position_x][
                                                tiles[k].position_y
                                            ]
                                            matrix[tiles[k].position_x][
                                                tiles[k].position_y
                                            ] = matrix[i][j]
                                            matrix[i][j] = dummy
                                            tiles[k].position_x = i
                                            tiles[k].position_y = j
                                            tiles[k].start_pos_x = tile_print_position[
                                                (i, j)
                                            ][0]
                                            tiles[k].start_pos_y = tile_print_position[
                                                (i, j)
                                            ][1]
                                            is_game_over()
                                            check_mobility()

                    if cell_found == False:
                        for k in range(tile_count):
                            if tiles[k].selected:
                                mat_pos_x = tiles[k].position_x
                                mat_pos_y = tiles[k].position_y
                                tiles[k].start_pos_x = tile_print_position[
                                    (mat_pos_x, mat_pos_y)
                                ][0]
                                tiles[k].start_pos_y = tile_print_position[
                                    (mat_pos_x, mat_pos_y)
                                ][1]
                                break

    # Draw tiles inside the container
    for i in range(tile_count):
        tiles[i].draw_tile()

    # Update the whole screen
    pygame.display.flip()

# Quit pygame
pygame.quit()
