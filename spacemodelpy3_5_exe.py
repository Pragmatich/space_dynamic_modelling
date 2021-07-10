# Modelling space movement and start situation.
# Using pygame as a 3D tool and numpy.

import pygame as pg
import numpy as np
import time
import sys

print(sys.maxsize)

pg.init()

fps = 300
fpsClock = pg.time.Clock()
resolution = 2

name = 0
mass = 1
mean_radius = 2
position = 3
speed = 4
color = 5
line_drow = 6
center = 7
visible = 8
editing = 9
trace = 10
control_list_position = 11
trace_pos = 12
rect_pos = 13

space_objects_pre = []
space_objects=[]

running_time2 = 0


def read_file():
    space_objects_txt = open("space_objects.txt", "r")
    for row_space_object_txt in space_objects_txt:
        space_objects_pre.append(row_space_object_txt.strip().split(','))
    space_objects_txt.close()

    space_objects_arranged_row = []

    for space_object in space_objects_pre:
        space_objects_arranged_row.append(space_object[0])  # name [0]
        space_objects_arranged_row.append(int(space_object[1])) # mass
        space_objects_arranged_row.append(int(space_object[2])) # main_radius
        space_objects_arranged_row.append(np.array([float(space_object[3]), float(space_object[4]), float(space_object[5])], dtype=float))  # position
        space_objects_arranged_row.append(np.array([float(space_object[6]), float(space_object[7]), float(space_object[8])], dtype=float))  # speed
        space_objects_arranged_row.append([int(space_object[9]), int(space_object[10]), int(space_object[11])]) # color
        if space_object[12] == 'True':                # line_drow [6]
            space_objects_arranged_row.append(True)
        else:
            space_objects_arranged_row.append(False)
        if space_object[13] == 'True':                # center [7]
            space_objects_arranged_row.append(True)
        else:
            space_objects_arranged_row.append(False)
        if space_object[14] == 'True':                # visible [8]
            space_objects_arranged_row.append(True)
        else:
            space_objects_arranged_row.append(False)
        if space_object[15] == 'True':                # editing [9]
            space_objects_arranged_row.append(True)
        else:
            space_objects_arranged_row.append(False)
        if space_object[16] == 'True':                # trace [10]
            space_objects_arranged_row.append(True)
        else:
            space_objects_arranged_row.append(False)
        space_objects_arranged_row.append(None)       # control_list_position [11]
        space_objects_arranged_row.append([np.array([])])       # trace_pos [12]
        space_objects_arranged_row.append(None)       # rect_pos [13]

        space_objects.append(space_objects_arranged_row)
        space_objects_arranged_row = []


read_file()

def save_file():
    try:
        new_space_objects = open("new_space_objects.txt", "x")
        for space_object in space_objects:
            row = str(space_object[0]) + ',' + str(space_object[1]) + ',' + str(space_object[2]) + ',' + \
            str(space_object[3][0]) + ',' + str(space_object[3][1]) + ',' + str(space_object[3][2]) + ',' + \
            str(space_object[4][0]) + ',' + str(space_object[4][1]) + ',' + str(space_object[4][2]) + ',' + \
            str(space_object[5][0]) + ',' + str(space_object[5][1]) + ',' + str(space_object[5][2]) + ',' + \
            str(space_object[6]) + ',' + str(space_object[7]) + ',' + str(space_object[8]) + ',' +\
            str(space_object[9]) + ',' + str(space_objects[i][10]) + '\n'
            new_space_objects.write(row)
        new_space_objects.close()
    except:
        new_file_exist.warning_on = True

pg.display.set_caption('Newtoni Mozgás Szimuláció')
pg.font.init()

white = (255, 255, 255)
dark = (10, 10, 10)
grey = (80, 80, 80)
grey_dark = (50, 50, 50)
green = (0, 255, 0)
blue = (100, 100, 255)
blue_light = (52, 152, 219)
red = (255, 0, 0)
red_light = (255, 30, 30)
yellow = (255, 255, 0)
purple = (155, 89, 182)
red_light =(231, 76, 60)
blue_green = (23, 165, 137)

COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')

font = pg.font.SysFont("Arial", 14)

display_x = 1000
display_x_half = display_x / 2
display_y = 800
display_y_half = display_y / 2

view_pos = np.array([0, 0, 0])
jump = 15

editing_on = False

# Space object properties
# class SpaceObject:

#     def __init__(self, name, mass, mean_radius, position, speed, color, line_drow, center, visible, control_list_position, editing, rect_pos):
#         self.name = name
#         self.mass = mass # [kg]
#         self.mean_radius = mean_radius # [m]
#         self.position = position # [m] x,y,z
#         self.speed = speed # [m] x,y,z
#         self.color = color
#         self.line_drow = line_drow
#         self.center = center
#         self.visible = visible
#         self.control_list_position = control_list_position
#         self.editing = editing
#         self.rect_pos = rect_pos
    
#     def add_element(self, name):
# 	    setattr(self, name, 0, 0, np.array([0, 0, 0], dtype=float), np.array([0, 0, 0], dtype=float), white_code.color_code, True, True, True, None, False, 0)

# space_objects = []



class ButtonProperties:

    def __init__(self, name, text, size_x, size_y, pos_x, pos_y, color, event):
        self.name = name
        self.text = text
        self.size_x = size_x
        self.size_y = size_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.event = event

class EditingControls:

    def __init__(self, name, text, size_x, size_y, pos_x, pos_y, color, active, space_object):
        self.name = name
        self.text = text
        self.size_x = size_x
        self.size_y = size_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.active = active
        self.space_object = space_object

class Axles:

    def __init__(self, name, position, color):
        self.name = name
        self.position = position
        self.color = color


class ColorList:

    def __init__(self, name, color_code):
        self.name = name
        self.color_code = color_code

white_code = ColorList('fehér', [255, 255, 255])
green_code = ColorList('zöld', [0, 255, 0])
blue_code = ColorList('kék', [100, 100, 255])
blue_light_code = ColorList('világoskék', [52, 152, 219])
red_code = ColorList('piros', [255, 0, 0])
yellow_code = ColorList('sárga', [255, 255, 0])
purple_code = ColorList('lila', [155, 89, 182])
red_light_code =ColorList('világospiros', [231, 76, 60])
blue_green_code = ColorList('kékeszöld', [23, 165, 137])

# color_codes = [white_code, green_code, blue_code, blue_light_code, red_code, yellow_code, purple_code, red_light_code, blue_green_code]


class InputBox:

    def __init__(self, space_object, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False
        self.space_object = space_object

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    if self == name_box:
                        self.space_object[name] = self.text
                        self.text = ''
                    elif self == mass_box:
                        self.space_object[mass] = int(self.text)
                        self.text = ''
                    elif self == radius_box:
                        self.space_object[mean_radius] = int(self.text)
                        self.text = ''

                    elif self == pos_x_box:
                        self.space_object[position][0] = int(self.text)
                        self.text = ''
                    elif self == pos_y_box:
                        self.space_object[position][1] = int(self.text)
                        self.text = ''
                    elif self == pos_z_box:
                        self.space_object[position][2] = int(self.text)
                        self.text = ''

                    elif self == speed_x_box:
                        self.space_object[speed][0] = int(self.text)
                        self.text = ''
                    elif self == speed_y_box:
                        self.space_object[speed][1] = int(self.text)
                        self.text = ''
                    elif self == speed_z_box:
                        self.space_object[speed][2] = int(self.text)
                        self.text = ''

                    # elif self == color_box:
                    #     for color in color_codes:
                    #         if color.name == self.text:
                    #             self.space_object[color = color.color_code
                    #     self.text = ''

                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = font.render(self.text, True, green)

    def update(self):
        # Resize the box if the text is too long.
        width = max(100, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

class WarningClass:

    def __init__(self, warning_text, warning_on, time):
        self.warning_text = warning_text
        self.warning_on = warning_on
        self.time = time

    def warning(self):
        if not self.time:
            self.time = time.time() + 3
        elif self.time < time.time():
            self.warning_on = False
            self.time = 0
        text = font.render(self.warning_text, True, red)
        pg.draw.rect(screen, red, [display_x // 2 - text.get_width() // 2 - 20, display_y // 2 - text.get_height() // 2 - 11, text.get_width() + 40, 40])
        pg.draw.rect(screen, white, [display_x // 2 - text.get_width() // 2 - 15, display_y // 2 - text.get_height() // 2 - 6, text.get_width() + 30, 30])
        screen.blit(text, (display_x // 2 - text.get_width() // 2, display_y // 2 - text.get_height() // 2))

# class TracingClass:
#     def __init__(self):
#         self.traced_space_objects = []

#     def tracing(space_objects):
#         traced_space_objects.append[red_light]
#         # for traced_space_object in traced_space_objects:
#             # if traced_space_object[0] = 
#             # pg.draw.lines(screen, space_objects[color], False, traced_space_object, 1)

def tracing(space_object, r11, r12, r13, r21, r22, r23, correction_x, correction_y):
    if space_object[trace] and run:
        # try:
        #     if space_object[trace_pos[-1]] == space_object[position]:
        pre_trace_pos = []
        pre_trace_pos.append(space_object[position][0])
        pre_trace_pos.append(space_object[position][1])
        pre_trace_pos.append(space_object[position][2])
        space_object[trace_pos].append(pre_trace_pos)
        # print(str(pre_trace_pos)[-1] + ' kakukk ' + str([space_object[position][0], space_object[position][1], space_object[position][2]]))
        # print([space_object[position][0], space_object[position][1], space_object[position][2]])
        if space_object[trace_pos][-1] == space_object[trace_pos][-2]:
            del space_object[trace_pos][-1]
            
            print(3)
        # except:
        #     None
        # for trace_point in space_object[trace_pos]:
        # try:
        #     pg.draw.lines(screen, space_object[color], False, [space_object[trace_pos]], 1)
        # except:
        #     None
# [(x_1, y_1), (x_2, y_2)]
scale_divider = 80000
# 7780 m/s 200 km-en
# earth = SpaceObject('Föld', 5972370000000000000000000, 6371000, np.array([0, 0, 0], dtype=float), np.array([0, 0, 0], dtype=float), white_code.color_code, True, True, True, None, False, 0)
# satellite = SpaceObject('Műhold', 500, 1, np.array([0, 6371000 + 200000,0], dtype=float), np.array([7780, 0, 0], dtype=float), blue_code.color_code, False, False, True, None, False, 0)
# moon = SpaceObject('Hold', 73476730000000000000000, 347200, np.array([380000000, 0, 0], dtype=float), np.array([0, 0, 1000], dtype=float), blue_green_code.color_code, False, False, True, None, False, 0)

start = ButtonProperties('start', font.render('INDÍTÁS', True, green), 110, 40, display_x - 130, 20, grey, None)
stop = ButtonProperties('stop', font.render('LEÁLLÍTÁS', True, green), 110, 40, display_x - 130, 80, grey, None)
alpha_plus = ButtonProperties('a+', font.render('A +', True, green), 30, 30, display_x - 130, 140, grey, None)
alpha_minus = ButtonProperties('a-', font.render('A -', True, green), 30, 30, display_x - 130, 180, grey, None)
beta_plus = ButtonProperties('b+', font.render('B +', True, green), 30, 30, display_x - 90, 140, grey, None)
beta_minus = ButtonProperties('b-', font.render('B -', True, green), 30, 30, display_x - 90, 180, grey, None)
gamma_plus = ButtonProperties('g+', font.render('G +', True, green), 30, 30, display_x - 50, 140, grey, None)
gamma_minus = ButtonProperties('g-', font.render('G -', True, green), 30, 30, display_x - 50, 180, grey, None)
zoom_in = ButtonProperties('közelítés', font.render('KÖZELÍTÉS', True, green), 110, 40, display_x - 130, 230, grey, None)
zoom_out = ButtonProperties('távolítás', font.render('TÁVOLÍTÁS', True, green), 110, 40, display_x - 130, 290, grey, None)
fps_up = ButtonProperties('fps+', font.render('FPS +', True, green), 110, 40, display_x - 130, 350, grey, None)
fps_down = ButtonProperties('fps-', font.render('FPS -', True, green), 110, 40, display_x - 130, 410, grey, None)
resulution_up = ButtonProperties('felbontás+', font.render('FELBONTÁS +', True, green), 110, 40, display_x - 130, 470, grey, None)
resulution_down = ButtonProperties('felbontás-', font.render('FELBONTÁS -', True, green), 110, 40, display_x - 130, 530, grey, None)
editing_button = ButtonProperties('editing', font.render('SZERKESZTÉS', True, green), 110, 40, display_x - 130, 590, grey, None)
reset = ButtonProperties('reset', font.render('VISSZÁLLÍTÁS', True, green), 110, 40, display_x - 130, 650, grey, None)
save = ButtonProperties('save', font.render('MENTÉS', True, green), 110, 40, display_x - 130, 710, grey, None)

left = EditingControls('left', '<', 20, 20, 30, display_y - 130, grey_dark, True, False)
right = EditingControls('right', '>', 20, 20, 690, display_y - 130, grey_dark, True, False)
visible_yes = EditingControls('visible_yes', 'IGEN', 40, 20, 385, display_y - 107, grey_dark, False, True)
visible_no = EditingControls('visible_no', 'NEM', 40, 20, 385, display_y - 107, grey_dark, False, True)
axles_yes = EditingControls('axles_yes', 'IGEN', 40, 20, 507, display_y - 107, grey_dark, False, True)
axles_no = EditingControls('axles_no', 'NEM', 40, 20, 507, display_y - 107, grey_dark, False, True)
add_object = EditingControls('add_object', 'HOZZÁADÁS', 80, 20, 570, display_y - 107, grey_dark, True, False)
save_object = EditingControls('save_object', 'MENTÉS', 80, 20, 680, display_y - 107, grey_dark, True, True)
delet_object = EditingControls('delet_object', 'TÖRLÉS', 80, 20, 680, display_y - 87, grey_dark, True, True)

x_axis = Axles('x_tengely', np.array([[1, 0, 0], [-1, 0, 0]], dtype=float), yellow)
y_axis = Axles('y_tengely', np.array([[0, -1, 0], [0, 1, 0]], dtype=float), purple)
z_axis = Axles('z_tengely', np.array([[0, 0, 1], [0, 0, -1]], dtype=float), red_light)

name_box = InputBox(None, 53, display_y - 85, 20, 20)
mass_box = InputBox(None, 500, display_y - 85, 20, 20)
radius_box = InputBox(None, 170, display_y - 65, 20, 20)
pos_x_box = InputBox(None, 340, display_y - 65, 20, 20)
pos_y_box = InputBox(None, 510, display_y - 65, 20, 20)
pos_z_box = InputBox(None, 680, display_y - 65, 20, 20)
speed_x_box = InputBox(None, 340, display_y - 45, 20, 20)
speed_y_box = InputBox(None, 510, display_y - 45, 20, 20)
speed_z_box = InputBox(None, 680, display_y - 45, 20, 20)
color_box = InputBox(None, 170, display_y - 45, 20, 20)

new_object_exist = WarningClass('Már létezik egy "UjTest"', False, 0)
data_fault = WarningClass('Több test, nem létezhet ugyanazon a helyen, ugyanabban az időben', False, 0)
new_file_exist = WarningClass('Már létezik egy "new_space_object.txt"', False, 0)

# space_objects = [earth, satellite, moon]

buttons = [start, stop, alpha_plus, alpha_minus, beta_plus, beta_minus, gamma_plus, gamma_minus, zoom_in, zoom_out, fps_up, fps_down, resulution_up, resulution_down, editing_button, reset, save]

editing_controls = [left, right, visible_yes, visible_no, axles_yes, axles_no, add_object, save_object]

axles = [x_axis, y_axis, z_axis]

input_boxes = [name_box, mass_box, radius_box, pos_x_box, pos_y_box, pos_z_box, speed_x_box, speed_y_box, speed_z_box, color_box]

warnings = [new_object_exist, data_fault, new_file_exist]


screen = pg.display.set_mode([display_x, display_y])

def editing_control_draw(space_object_editing, space_object_visible, line_drow):
    # for editing_control in editing_controls:
        
    for editing_control in editing_controls:
        if editing_control.name == 'visible_yes' and space_object_visible:
            editing_control.active = True
        elif editing_control.name == 'visible_yes' and not space_object_visible:
            editing_control.active = False
        if editing_control.name == 'visible_no' and space_object_visible:
            editing_control.active = False
        elif editing_control.name == 'visible_no' and not space_object_visible:
            editing_control.active = True

        if editing_control.name == 'axles_yes' and line_drow:
            editing_control.active = True
        elif editing_control.name == 'axles_yes' and not line_drow:
            editing_control.active = False
        if editing_control.name == 'axles_no' and line_drow:
            editing_control.active = False
        elif editing_control.name == 'axles_no' and not line_drow:
            editing_control.active = True

        if not editing_control.space_object or editing_control.space_object and space_object_editing and editing_control.active:
            if editing_control.name == 'left' and not roll_base:
                control_color = white
            elif editing_control.name == 'right' and not roll_base_adding:
                control_color = white
            else:
                control_color = green
            pg.draw.rect(screen,editing_control.color,[editing_control.pos_x, editing_control.pos_y, editing_control.size_x, editing_control.size_y])
            controll_text = font.render(editing_control.text, True, control_color)
            screen.blit(controll_text, (editing_control.pos_x + editing_control.size_x // 2 - controll_text.get_width() // 2, editing_control.pos_y + editing_control.size_y // 2 - controll_text.get_height() // 2))

def change_visible():
    for space_object in space_objects:
        if space_object[editing]: 
            if space_object[visible]:
                space_object[visible] = False
            else:
                space_object[visible] = True
            break

def change_axles():
    for space_object in space_objects:
        if space_object[editing]: 
            if space_object[line_drow]:
                space_object[line_drow] = False
            else:
                space_object[line_drow] = True
            break

# def rotator(r11, r12, r13, r21, r22, r23, x, y, z):
#     x_rotated = (r11 * x + r12 * y + r13 * z)
#     y_rotated = (r21 * x + r22 * y + r23 * z)
#     return[x_rotated, y_rotated]

def new_object(space_objects):
    new_object = False
    for space_object in space_objects:
        if space_object[name] == 'UjTest':
            new_object = True
            new_object_exist.warning_on = True

    if not new_object:
        space_objects.append(['UjTest', 1, 1, np.array([0, 0, 0], dtype=float), np.array([0, 0, 0], dtype=float), [155, 155, 155], True, False, True, False, False, None, None, None])

def save_object_func(space_objects):
    for i in range(len(space_objects)):
        if space_objects[i][editing]:
            with open('space_objects.txt', 'r') as space_objects_file:
                data = space_objects_file.readlines()
            try:
                data[i] = str(space_object[0]) + ',' + str(space_object[1]) + ',' + str(space_object[2]) + ',' + \
                str(space_object[3][0]) + ',' + str(space_object[3][1]) + ',' + str(space_object[3][2]) + ',' + \
                str(space_object[4][0]) + ',' + str(space_object[4][1]) + ',' + str(space_object[4][2]) + ',' + \
                str(space_object[5][0]) + ',' + str(space_object[5][1]) + ',' + str(space_object[5][2]) + ',' + \
                str(space_object[6]) + ',' + str(space_object[7]) + ',' + str(space_object[8]) + ',' +\
                str(space_object[9]) + ',' + str(space_objects[i][10]) + '\n'
                with open('space_objects.txt', 'w') as space_objects_file:
                    space_objects_file.writelines(data)
            except:
                with open("space_objects.txt", "a") as space_objects_file:
                    space_objects_file.write(str(space_objects[i][0]) + ',' + str(space_objects[i][1]) + ',' + str(space_objects[i][2]) + ',' + str(space_objects[i][3][0]) + ',' + str(space_objects[i][3][1]) + ',' + str(space_objects[i][3][2]) + ',' + str(space_objects[i][4][0]) + ',' + str(space_objects[i][4][1]) + ',' + str(space_objects[i][4][2]) + ',' + str(space_objects[i][5][0]) + ',' + str(space_objects[i][5][1]) + ',' + str(space_objects[i][5][2]) + ',' + str(space_objects[i][6]) + ',' + str(space_objects[i][7]) + ',' + str(space_objects[i][8]) + ',' + str(None) + ',' + str(space_objects[i][10]) + ',' + str(space_objects[i][12]) + '\n')
            space_objects_file.close()

# def delet_object_func():
#     None


running_time = 0
running_m = 0
running_h = 0
running_d = 0

correction_x = 0
correction_y = 0

space_object_pos_rectangle_color = grey
space_object_pos_rectangle_size = 14

roll_base = 0
roll_base_adding = True

run = False

running = True

while running:
    if run:
        running_time += 1 * resolution
        running_d = running_time // 86400
        running_h = running_time % 86400 // 3600
        running_m = running_time % 86400 % 3600 // 60

    screen.fill((dark))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.pos_x <= mouse[0] <= button.pos_x + button.size_x and button.pos_y <= mouse[1] <= button.pos_y + button.size_y:
                    if button.name == 'a+':
                        view_pos[0] += jump
                        if view_pos[0] == 360:
                            view_pos[0] = 0
                    elif button.name == 'a-':
                        if view_pos[0] == 0:
                            view_pos[0] = 360
                        view_pos[0] -= jump
                    elif button.name == 'b+':
                        view_pos[1] += jump
                        if view_pos[1] == 360:
                            view_pos[1] = 0
                    elif button.name == 'b-':
                        if view_pos[1] == 0:
                            view_pos[1] = 360
                        view_pos[1] -= jump
                    elif button.name == 'g+':
                        view_pos[2] += jump
                        if view_pos[2] == 360:
                            view_pos[2] = 0
                    elif button.name == 'g-':
                        if view_pos[2] == 0:
                            view_pos[2] = 360
                        view_pos[2] -= jump
                    elif button.name == 'közelítés':
                        scale_divider *= 0.5
                    elif button.name == 'távolítás':
                        scale_divider *= 2
                    elif button.name == 'fps+':
                        fps += 20
                    elif button.name == 'fps-':
                        fps -=  20
                    elif button.name == 'start':
                        run = True
                    elif button.name == 'stop':
                        run = False
                    elif button.name == 'felbontás+':
                        if resolution < 10:
                            resolution += 1
                        else:
                            resolution += 10
                    elif button.name == 'felbontás-':
                        if resolution > 10:
                            resolution -= 10
                        else:
                            resolution -= 1
                    elif button.name == 'editing':
                        if editing_on:
                            editing_on = False
                        else:
                            editing_on = True
                    elif button.name == 'reset':
                        space_objects_pre = []
                        space_objects=[]
                        running_time = 0
                        read_file()
                    elif button.name == 'save':
                        save_file()

            for space_object in space_objects:
                if 20 <= mouse[0] <= 20 + space_object_pos_rectangle_size and space_object[rect_pos] <= mouse[1] <= space_object[rect_pos] + space_object_pos_rectangle_size:
                    for space_object2 in space_objects:
                        if space_object2[center]:
                            space_object2[center] = False
                    space_object[center] = True
                if space_object[control_list_position] and space_object[control_list_position].left <= mouse[0] <= space_object[control_list_position].left + space_object[control_list_position].width and space_object[control_list_position].top <= mouse[1] <= space_object[control_list_position].top + space_object[control_list_position].height:
                    for space_object3 in space_objects:
                        space_object3[editing] = False
                    space_object[editing] = True

            for editing_control in editing_controls:
                if editing_control.pos_x <= mouse[0] <= editing_control.pos_x + editing_control.size_x and editing_control.pos_y <= mouse[1] <= editing_control.pos_y + editing_control.size_y and editing_control.active:
                    if editing_control.name == 'left' and roll_base > 0:
                        roll_base -= 1
                        roll_base_adding = True
                    elif editing_control.name == 'right' and roll_base_adding:
                        roll_base += 1
                    if editing_control.name == 'visible_yes':
                        change_visible()
                    elif editing_control.name == 'visible_no':
                        change_visible()
                    if editing_control.name == 'axles_yes':
                        change_axles()
                    elif editing_control.name == 'axles_no':
                        change_axles()
                    if editing_control.name == 'add_object':
                        new_object(space_objects)
                    if editing_control.name == 'save_object':
                        save_object_func(space_objects)
                    # if editing_control.name == 'delet_object':
                    #     delet_object_func(space_objects)


        for box in input_boxes:
            box.handle_event(event)
                        


    r11 = np.cos(view_pos[2] * np.pi/180) * np.cos(view_pos[1] * np.pi/180)
    r12 = np.cos(view_pos[2] * np.pi/180) * np.sin(view_pos[1] * np.pi/180) * np.sin(view_pos[0] * np.pi/180) - np.sin(view_pos[2] * np.pi/180) * np.cos(view_pos[0] * np.pi/180)
    r13 = np.cos(view_pos[2] * np.pi/180) * np.sin(view_pos[1] * np.pi/180) * np.cos(view_pos[0] * np.pi/180) +  np.sin(view_pos[2] * np.pi/180) * np.sin(view_pos[0] * np.pi/180)
    r21 = np.sin(view_pos[2] * np.pi/180) * np.cos(view_pos[1] * np.pi/180)
    r22 = np.sin(view_pos[2] * np.pi/180) * np.cos(view_pos[1] * np.pi/180) * np.sin(view_pos[0] * np.pi/180) + np.cos(view_pos[2] * np.pi/180) * np.cos(view_pos[0] * np.pi/180)
    r23 = np.sin(view_pos[2] * np.pi/180) * np.sin(view_pos[1] * np.pi/180) * np.cos(view_pos[0] * np.pi/180) -  np.cos(view_pos[2] * np.pi/180) * np.sin(view_pos[0] * np.pi/180)

    sor = 0

    for space_object in space_objects:
        if space_object[center]:
            # space_object_position_x = rotator(r11, r12, r13, r21, r22, r23, space_object.position[0], space_object.position[1], space_object.position[2])[0]
            # space_object_position_y = rotator(r11, r12, r13, r21, r22, r23, space_object.position[0], space_object.position[1], space_object.position[2])[1]
            space_object_position_x = (r11 * space_object[position][0] + r12 * space_object[position][1] + r13 * space_object[position][2])
            space_object_position_y = (r21 * space_object[position][0] + r22 * space_object[position][1] + r23 * space_object[position][2])
            correction_x = space_object_position_x
            correction_y = space_object_position_y

    for i in range(len(space_objects)):
        if space_objects[i][visible]:
            sor += 1
            space_object_mean_radius = int(space_objects[i][mean_radius] / scale_divider)
            if space_object_mean_radius < 5:
                space_object_mean_radius = 5

            axis_scaler = np.array([[space_objects[i][mean_radius] * 1.5, space_objects[i][mean_radius] * 1.5, space_objects[i][mean_radius] * 1.5], [space_objects[i][mean_radius] * 1.5, space_objects[i][mean_radius] * 1.5, space_objects[i][mean_radius] * 1.5]], dtype=float)

            space_object_position_x = (r11 * space_objects[i][position][0] + r12 * space_objects[i][position][1] + r13 * space_objects[i][position][2])
            space_object_position_y = (r21 * space_objects[i][position][0] + r22 * space_objects[i][position][1] + r23 * space_objects[i][position][2])

            # space_object_position_x = rotator(r11, r12, r13, r21, r22, r23, space_object.position[0], space_object.position[1], space_object.position[2])[0]
            # space_object_position_y = rotator(r11, r12, r13, r21, r22, r23, space_object.position[0], space_object.position[1], space_object.position[2])[1]

            space_object_display_pos_x = int(display_x_half - (space_object_position_x - correction_x) // scale_divider)
            space_object_display_pos_y = int(display_y_half - (space_object_position_y - correction_y) // scale_divider)
            # try:
            if space_object_display_pos_x < 1000 and space_object_display_pos_y < 1000 and space_object_mean_radius < 1000:
                print(str(space_objects[i][name]) + ' ' + str(sys.maxsize) + ' ' + str(space_object_display_pos_x) + ' ' + str(space_object_display_pos_y) + ' ' + str(space_object_mean_radius))
                pg.draw.circle(screen, space_objects[i][color], (space_object_display_pos_x, space_object_display_pos_y), space_object_mean_radius)

                space_object_name_text = font.render(space_objects[i][name], True, space_objects[i][color])
                screen.blit(space_object_name_text, (space_object_display_pos_x + space_object_mean_radius + 5, space_object_display_pos_y + space_object_mean_radius + 5))
            # except:
            #     print("SZOPI")
        
            tracing(space_objects[i], r11, r12, r13, r21, r22, r23, correction_x, correction_y)

            if space_objects[i][line_drow]:
                for axis in axles:
                    axis_scaled = axis.position * axis_scaler
                    axis_fitted = axis_scaled + space_objects[i][position]

                    # axis_display_pos_x, axis_display_pos_y = rotator()

                    axis_pos_x_1 = int(r11 * axis_fitted[0][0] + r12 * axis_fitted[0][1] + r13 * axis_fitted[0][2])
                    axis_pos_y_1 = int(r21 * axis_fitted[0][0] + r22 * axis_fitted[0][1] + r23 * axis_fitted[0][2])

                    axis_pos_x_2 = int(r11 * axis_fitted[1][0] + r12 * axis_fitted[1][1] + r13 * axis_fitted[1][2])
                    axis_pos_y_2 = int(r21 * axis_fitted[1][0] + r22 * axis_fitted[1][1] + r23 * axis_fitted[1][2])
                    
                    axis_display_pos_x_1 = int(display_x_half - (axis_pos_x_1 - correction_x) // scale_divider)
                    axis_display_pos_y_1 = int(display_y_half - (axis_pos_y_1 - correction_y) // scale_divider)

                    axis_display_pos_x_2 = int(display_x_half - (axis_pos_x_2 - correction_x) // scale_divider)
                    axis_display_pos_y_2 = int(display_y_half - (axis_pos_y_2 - correction_y) // scale_divider)

                    pg.draw.lines(screen, axis.color, False, [(axis_display_pos_x_1, axis_display_pos_y_1), (axis_display_pos_x_2, axis_display_pos_y_2)], 2)
                    pg.draw.circle(screen, axis.color, (axis_display_pos_x_2, axis_display_pos_y_2), 5, 1)
                    pg.draw.circle(screen, axis.color, (axis_display_pos_x_1, axis_display_pos_y_1), 5)

            try:
                if run:
                    for j in range(i + 1, len(space_objects)):
                        if space_objects[j][visible]:
                            f = - (6.6743 * 10 ** -11) * ((space_objects[i][mass] * space_objects[j][mass]) / (np.linalg.norm(space_objects[i][position] - space_objects[j][position]) ** 2)) * ((space_objects[i][position] - space_objects[j][position]) / np.linalg.norm(space_objects[i][position] - space_objects[j][position]))
                            ai = f/space_objects[i][mass] 
                            aj = f/space_objects[j][mass]

                            space_objects[i][speed][0] += ai[0] * resolution
                            space_objects[i][speed][1] += ai[1] * resolution
                            space_objects[i][speed][2] += ai[2] * resolution

                            space_objects[j][speed][0] += aj[0] * resolution
                            space_objects[j][speed][1] += aj[1] * resolution
                            space_objects[j][speed][2] += aj[2] * resolution

                    space_objects[i][position] -= space_objects[i][speed] * resolution
            
                space_object_pos_text_base = str(space_objects[i][name]) + ' ' + str(space_objects[i][position]) + ' ' + str(space_objects[i][speed]) + ' ' + str(round(np.linalg.norm(space_objects[i][speed]), 1))
                space_object_pos_text = font.render(space_object_pos_text_base, True, green)
                space_object_pos_text_x = 40
                space_object_pos_rectangle_x = 20
                space_object_pos_text_y = 25 + (sor + 1) * 20
                screen.blit(space_object_pos_text, (space_object_pos_text_x, space_object_pos_text_y))
                space_objects[i][rect_pos] = space_object_pos_text_y + 2
                if space_objects[i][center]:
                    space_object_pos_rectangle_color = white
                else:
                    space_object_pos_rectangle_color = grey
                pg.draw.rect(screen,space_object_pos_rectangle_color,[space_object_pos_rectangle_x, space_objects[i][rect_pos], space_object_pos_rectangle_size, space_object_pos_rectangle_size])
            except:
                run = False
                data_fault.warning_on = True
                running_time2 = running_time // fpsClock.get_fps()

    for button in buttons:
        pg.draw.rect(screen,grey,[button.pos_x, button.pos_y, button.size_x, button.size_y])
        screen.blit(button.text, (button.pos_x + button.size_x // 2 - button.text.get_width() // 2, button.pos_y + button.size_y // 2 - button.text.get_height() // 2))

    view_pos_text = font.render(str(view_pos) + ' ' + str(fps) + ' ' + str(int(fpsClock.get_fps())) + ' ' + str(running_d) + 'd '+ str(running_h) + 'h '+ str(running_m) + 'm', True, green)
    screen.blit(view_pos_text, (20, 20))
    resolution_pos_text = font.render('Felbontás: ' + str(resolution) + 's', True, green)
    screen.blit(resolution_pos_text, (20, 40))

    rolling = 70
    
    if editing_on:
        pg.draw.rect(screen,grey,[20, display_y - 140, 800, 120])
        editing_control_draw(False, None, None)
        list_end = False
        for i in range(len(space_objects)):
            if not list_end:
                try:
                    space_objects[i + 1]
                except:
                    roll_base_adding = False
                if i >= roll_base:
                    list_text = font.render(space_objects[i][name], True, green)
                    screen.blit(list_text, (rolling, display_y - 130))
                    rolling += list_text.get_width()
                    if rolling > 560 and i + 1 < len(space_objects):
                        rolling2 = rolling - list_text.get_width()
                        last_name = ''
                        last_name_with_dots = ''
                        space_objects[i][control_list_position] = pg.Rect(rolling - list_text.get_width(), display_y - 130, list_text.get_width(), list_text.get_height())
                        for letter in space_objects[i + 1][name]:
                            last_name += letter
                            last_name_with_dots = last_name + '...'
                            text_last_name_with_dots = font.render(last_name_with_dots, True, green)
                            text_last_name_with_dots_too_much = font.render(last_name_with_dots, True, green)
                            if rolling2 + 20 + text_last_name_with_dots.get_width() > 560 and rolling2 + 20 < 560:
                                screen.blit(text_last_name_with_dots, (rolling + 20, display_y - 130))
                                space_objects[i + 1][control_list_position] = pg.Rect(rolling + 20, display_y - 130, text_last_name_with_dots.get_width(), text_last_name_with_dots.get_height())
                                break
                        list_end = True
                    else:
                        space_objects[i][control_list_position] = pg.Rect(rolling - list_text.get_width(), display_y - 130, list_text.get_width(), list_text.get_height())
                    rolling += 20
                else:
                    space_objects[i][control_list_position] = None
            if space_objects[i][editing]:
                editing_control_draw(True, space_objects[i][visible], space_objects[i][line_drow])
                editing_name_text = font.render(space_objects[i][name], True, green)
                screen.blit(editing_name_text, (30, display_y - 105))
                visible_text = font.render('Szimulációban megjelenik', True, green)
                screen.blit(visible_text, (250, display_y - 105))
                visible_text = font.render('Tengelyek', True, green)
                screen.blit(visible_text, (450, display_y - 105))
                visible_text = font.render('Név', True, green)
                screen.blit(visible_text, (30, display_y - 85))
                visible_text = font.render('Tömeg: ' + str(space_objects[i][mass]), True, green)
                screen.blit(visible_text, (190, display_y - 85))
                visible_text = font.render('Fő sugár: ' + str(space_objects[i][mean_radius]), True, green)
                screen.blit(visible_text, (30, display_y - 65))
                visible_text = font.render('Hely X', True, green)
                screen.blit(visible_text, (300, display_y - 65))
                visible_text = font.render('Hely Y', True, green)
                screen.blit(visible_text, (470, display_y - 65))
                visible_text = font.render('Hely Z', True, green)
                screen.blit(visible_text, (640, display_y - 65))

                visible_text = font.render('Szín: ' + str(space_objects[i][color]), True, green)
                screen.blit(visible_text, (30, display_y - 45))
                visible_text = font.render('Seb. X', True, green)
                screen.blit(visible_text, (300, display_y - 45))
                visible_text = font.render('Seb. Y', True, green)
                screen.blit(visible_text, (470, display_y - 45))
                visible_text = font.render('Seb. Z', True, green)
                screen.blit(visible_text, (640, display_y - 45))

                # visible_text = font.render('OBJEKTUM HOZZÁADÁSA', True, green)
                # screen.blit(visible_text, (640, display_y - 85))

                for box in input_boxes:
                    box.space_object = space_objects[i]
                    box.update()                    
                    box.draw(screen)

    for warning in warnings:
        if warning.warning_on:
            warning.warning()
            

        
            


    mouse = pg.mouse.get_pos()

    fpsClock.tick(fps)

    pg.display.flip()



pg.quit()