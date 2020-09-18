import datetime
import pygame
import solarsystem
from pygame import gfxdraw

pygame.font.init()


def flip_planets_vertically(coords: tuple, window_y: int):  # this function flips the planets position vertically
    return int(coords[0]), int(coords[1] + (((window_y / 2) - coords[1]) * 2))


def draw_circle(surface, color, x, y, radius, fill: bool):  # draws a circle with anti-aliasing and returns
    if fill:  # a pygame rect so that Rect.collidepoint() can
        gfxdraw.filled_circle(surface, x, y, radius, color)  # later be used on it.
        return pygame.Rect(x - radius, y - radius,
                           radius + radius, radius + radius)

    gfxdraw.aacircle(surface, x, y, radius, color)  # these calculations are made to optimize the collision
    return pygame.Rect(x - radius, y - radius,  # point between the mouse and the Rect
                       radius + radius, radius + radius)


def get_new_planet_pos(year, month, day):
    now = Data.now
    current_year, current_month, current_day = now.year * 365.2422, now.month * Data.month_length, float(now.day)

    try: year_to_days = float(year) * 365.2422
    except ValueError: year_to_days = Data.year * 365.2422

    try:months_to_days = float(month) * Data.month_length                   # using the current day's dates if nothing
    except ValueError: months_to_days = Data.month * Data.month_length      # was written in the input boxes

    try: day_day = float(day)
    except ValueError: day_day = Data.day

    return round((day_day + year_to_days + months_to_days)) - \
           round((current_year + current_month + current_day))      # returning the amount of days between today's date
                                                                    # and the date inputted


def change_planets_pos():
    # this function changes the position of the planets by the amount of days between today's date and the date inputted
    # which are taken from get_new_planet_pos()
    now = Data.now
    if Data.to_add == 0: Data.changing_date = False   # when there are no more days to add/subtract, the animation stops

    else:            # checks if the number is negative
        if str(Data.to_add).startswith("-"):
            if Data.to_add > -100: new, Data.to_add = (now + datetime.timedelta(days=-1)), Data.to_add + 1

            if Data.to_add < -100: new, Data.to_add = (now + datetime.timedelta(days=-10)), Data.to_add + 10

            if Data.to_add < -1000: new, Data.to_add = (now + datetime.timedelta(days=-110)), Data.to_add + 100
            Data.day, Data.month, Data.year, Data.now = new.day, new.month, new.year, new
        # adds or decreases Data.to_add with the days added to today's date so that when Data.to_add reaches 0 it means
        # that the function has reached the date inputted.

        else:
            if Data.to_add < 100: new, Data.to_add = (now + datetime.timedelta(days=1)), Data.to_add - 1

            if Data.to_add > 100: new, Data.to_add = (now + datetime.timedelta(days=10)), Data.to_add - 10

            if Data.to_add > 1000: new, Data.to_add = (now + datetime.timedelta(days=110)), Data.to_add - 100

            Data.day, Data.month, Data.year, Data.now = new.day, new.month, new.year, new
                                    # updates the date in Data with the new ones


def fast_forward(count):  # this function speeds up time by adding a day, month or year to the current time
    now = Data.now        # count increments every time the user clicked on the forward button and
    if count == 1:        # decrements when the backwards button is clicked
        new = (now + datetime.timedelta(days=1))
        Data.day, Data.month, Data.year, Data.now = new.day, new.month, new.year, new

    if count == 2:
        new = (now + datetime.timedelta(days=Data.month_length))
        Data.day, Data.month, Data.year, Data.now = new.day, new.month, new.year, new

    if count == 3:
        if ((now.year % 4) % 100) % 400 == 0: new = (now + datetime.timedelta(days=366))
        # detecting whether current year is is a leap year
        else: new = (now + datetime.timedelta(days=365))

        Data.day, Data.month, Data.year, Data.now = new.day, new.month, new.year, new


class Button:
    def __init__(self, color, x, y, width, height, text='', font_family='', font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font_family = font_family
        self.font_size = font_size

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline: pygame.draw.rect(win, outline, self.rect, 0)

        else: pygame.draw.rect(win, self.color, self.rect, 0)

        if self.text != '':
            text = pygame.font.SysFont(self.font_family, self.font_size).render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.rect.x + (self.rect.width / 2 - text.get_width() / 2),
                            self.rect.y + (self.rect.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):  # function returns true or false depending if the cursor is on top of the button
        # Pos is the mouse position as a tuple of (x,y) coordinates
        if self.rect.collidepoint(pos[0], pos[1]): return True

        else: return False


class Data:
    window_size = (1280, 800)
    window_center = int(window_size[0] / 2), int(window_size[1] / 2)
    now = datetime.datetime.now(datetime.timezone.utc)
    year, month, day, hour, minute = now.year, now.month, now.day, now.hour, now.minute
    scale_factor = 200
    planet_colors = [(225, 130, 43), (242, 200, 162), (0, 80, 220), (255, 47, 47), (255, 255, 200)]
    color_inactive = pygame.Color('#8DB6CD')
    color_active = pygame.Color("#00FFFF")
    font = pygame.font.SysFont("dubai", 20, False)
    planet_radius = 10
    title_font = pygame.font.SysFont("dubai", 30, True)
    month_length = 30.4368499
    to_add = 0
    changing_date = False
    planets_data = {"Mercury": {"Mass": "3.285 x 10^23 kg", "Radius": "2,439.7 km", "Orbital period": "88 days",
                                "Length of day": "58d 15h 30m", "Surface Gravity": "3.7 m/s²", "Diameter": "4,880 km",
                                "Distance from Sun": "58 million km"},

                    "Venus": {"Mass": "4.8675 x 10^24 kg", "Radius": "6,051.8 km", "Orbital period": "225 days",
                              "Length of day": "116d 18h 0m", "Surface Gravity": "8.87 m/s²", "Diameter": "12,103 km",
                              "Distance from Sun": "108 million km"},

                    "Earth": {"Mass": "5.9724 x 10^24 kg", "Radius": "6,371.0 km", "Orbital period": "365.25 days",
                              "Length of day": "0d 23h 56m", "Surface Gravity": "9.80665 m/s²", "Diameter": "12,742 km",
                              "Distance from Sun": "151 million km"},

                    "Mars": {"Mass": "6.4171 x 10^23 kg", "Radius": "3,389.5 km", "Orbital period": "687 days",
                             "Length of day": "1d 0h 37m", "Surface Gravity": "3.711 m/s²", "Diameter": "6,779 km",
                             "Distance from Sun": "209 million km"},

                    "Sun": {"Mass": "1.9884 x 10^30 kg", "Radius": "696,342 km", "Surface Gravity": "274 m/s²",
                            "Diameter": "1.39 million km"}}


class Sun:
    def __init__(self, window_name):
        self.window_name = window_name
        self.sun = draw_circle(window_name, (255, 100, 0), Data.window_center[0], Data.window_center[1], 25, True)

    def cursorIsOver(self, pos):
        # Pos is the mouse position
        keys = []
        if self.sun.collidepoint(pos[0], pos[1]):
            for data in Data.planets_data["Sun"]:
                keys.append(data)  # writing the planet name

            self.window_name.blit(Data.title_font.render("Sun", True, (30, 100, 255)), (60, 50))
            for i in range(keys.__len__()):
                text = Data.font.render(keys[i] + ": " + Data.planets_data["Sun"][keys[i]], True, (30, 203, 225))
                self.window_name.blit(text, (10, (i * 40) + 100))


class CosmicObject:
    def __init__(self, window_name):
        self.window_name = window_name
        self.solar_system = solarsystem.Heliocentric(Data.year, Data.month, Data.day, Data.hour, Data.minute, 0,
                                                     view='rectangular')
        self.planet_name = self.solar_system.planetnames()
        self.positions = []
        for key in self.solar_system.planets():
            self.positions.append(self.solar_system.planets()[key])
        self.name_and_coords = {}

    def drawObjects(self):
        for i in range(4):  # orbits of the planets
            draw_circle(self.window_name, (255, 255, 255), Data.window_center[0], Data.window_center[1],
                        int(((abs(self.positions[i][0]) ** 2 +
                              abs(self.positions[i][1]) ** 2) ** 0.498) * Data.scale_factor), False)

            # getting the x and y positions for the planets
            x, y = flip_planets_vertically((int(Data.window_center[0] + (self.positions[i][0] * Data.scale_factor)),
                                            int(Data.window_center[1] + self.positions[i][1] * Data.scale_factor)),
                                           Data.window_size[1])

            planet = draw_circle(self.window_name, Data.planet_colors[i], x, y, Data.planet_radius, True)
            # drawing the planets

            text = pygame.font.SysFont('dubai', 18).render(self.planet_name[i], 1, Data.planet_colors[i])
            self.window_name.blit(text, (x - (Data.planet_radius * 2), y))  # writing the name of the planets

            self.name_and_coords[self.planet_name[i]] = planet
            # creating a dictionary with planet name as key and pygame.Rect as the value

    def isOver(self, pos):  # returns the planet name with which the cursor colided with.
        for planet in self.name_and_coords:
            if self.name_and_coords[planet].collidepoint(pos[0], pos[1]): return planet


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = Data.color_inactive
        self.text = text
        self.txt_surface = Data.font.render(text, True, self.color)
        self.box_active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable and clear the placeholder text when clicked.
                self.text = ""
                self.box_active = True

            else: self.box_active = False

            # Change the current color of the input box.
            self.color = Data.color_active if self.box_active else Data.color_inactive

        if event.type == pygame.KEYDOWN and self.box_active:
            if event.key == pygame.K_RETURN:
                self.box_active = False
                self.color = Data.color_inactive

            elif event.key == pygame.K_BACKSPACE: self.text = self.text[:-1]

            else: self.text += event.unicode

            # Re-render the text.
            self.txt_surface = Data.font.render(self.text, True, self.color)

    def update(self):
        if self.text.__len__() > 5:  # delete last character if the length of the text exceeds 5
            self.text = self.text[:-1]
            self.txt_surface = Data.font.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y))   # input box gets drawn on the screen along with
        pygame.draw.rect(screen, self.color, self.rect, 2)              # the text


class InfoScreen:
    def __init__(self, window_name):
        self.window_name = window_name
        self.date = Data.font.render(f"{Data.year}/{Data.month}/{Data.day}", True, (30, 203, 225))
        self.window_name.blit(self.date, (10, 5))

    def drawPlanetsData(self, planet_name):
        keys = []  # this list is used to store the keys of a planet in Data.planets_data. e.g. "Mass"
        # this function loops over Data.planets_data, checks if the name received as argument is in Data.planets_date
        # then stores the keys of that planet in a list.
        for name in Data.planets_data:
            if name == planet_name:
                for data in Data.planets_data[name]: keys.append(data)

                                                    # writing the name of the planet on which the cursor is on top of.
                self.window_name.blit(Data.title_font.render(name, True, (30, 100, 255)), (60, 50))
                for i in range(keys.__len__()):
                    text = Data.font.render(f"{keys[i]}: {Data.planets_data[planet_name][keys[i]]}", True, (30, 203, 225))
                    self.window_name.blit(text, (10, (i * 40) + 100))
                    # writing info about the planet on which the cursor is on top of.
