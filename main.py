from funcs import *
import pygame

pygame.init()
mainWindow = pygame.display.set_mode(Data.window_size)      # setting the window x and y
pygame.display.set_caption("Solar System")                  # setting the window title

input_boxes = (InputBox(Data.window_size[0] - 355, 5, 80, 32, "Year"), InputBox(Data.window_size[0] - 265, 5, 80, 32, "Month"),
               InputBox((Data.window_size[0] - 175), 5, 80, 32, "Day"))   # creating input boxes for year, month and day

buttons = {"Go to date": Button((30, 203, 225), Data.window_size[0] - 85, 5, 75, 32, "Go to", "dubai", 30),
           "Fast forward on": Button((30, 203, 225), Data.window_size[0] - 420, 5, 50, 32, ">>", "dubai", 30),
           "Fast forward off": Button((30, 203, 225), Data.window_size[0] - 475, 5, 50, 32, "<<", "dubai", 30)}


count = 0
while True:
    pos, events = pygame.mouse.get_pos(), pygame.event.get()
    planets = CosmicObject(mainWindow)
    mainWindow.fill((5, 5, 5))
    planets.drawObjects()
    Sun(mainWindow).cursorIsOver(pos)
    for btn in buttons: buttons[btn].draw(mainWindow)
    fast_forward(count)
    data = InfoScreen(mainWindow)
    data.drawPlanetsData(planets.isOver(pos))

    for event in events:
        if event.type == pygame.QUIT: quit("Game closed. Goodbye!")

        if event.type == pygame.MOUSEBUTTONDOWN and buttons["Go to date"].isOver(pos):
            buttons["Go to date"].color = (30, 100, 225)               # changes color when the button is clicked
            Data.changing_date = True
            Data.to_add = get_new_planet_pos(input_boxes[0].text, input_boxes[1].text, input_boxes[2].text)

        if event.type == pygame.MOUSEBUTTONUP and buttons["Go to date"].isOver(pos):
            buttons["Go to date"].color = (30, 203, 225)
            # changes the color to the original color when mouse 1 is released.

        if event.type == pygame.MOUSEBUTTONDOWN and buttons["Fast forward on"].isOver(pos):
            buttons["Fast forward on"].color = (30, 100, 225)
            count = count + 1
            if count > 3: count = 3      # return count to 3 if the button is pressed more then 3 times

        if event.type == pygame.MOUSEBUTTONUP and buttons["Fast forward on"].isOver(pos):
            buttons["Fast forward on"].color = (30, 203, 225)

        if event.type == pygame.MOUSEBUTTONDOWN and buttons["Fast forward off"].isOver(pos):
            buttons["Fast forward off"].color = (30, 100, 225)
            count = count - 1
            if count < 0: count = 0      # return count to 0 if the backwards button is clicked when count is 0

        if event.type == pygame.MOUSEBUTTONUP and buttons["Fast forward off"].isOver(pos):
            buttons["Fast forward off"].color = (30, 203, 225)

        for box in input_boxes: box.handle_event(event)

    for box in input_boxes:
        box.update()
        box.draw(mainWindow)

    if Data.changing_date: change_planets_pos()

    pygame.display.update()