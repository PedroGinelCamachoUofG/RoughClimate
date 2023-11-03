import pygame as py
import math

class Text:

    def __init__(self, x, y, text, font=None) -> None:
        self.text = text
        self.pos = (x,y)
        if not font:
            self.font = py.font.Font(None, 32)
        else:
            self.font = font

    def change_text(self, text) -> None:
        self.text = text

    def add_text(self,char) -> None:
        self.text += char

    def is_over(self, pointer) -> bool:
        if (self.pos[0] < pointer.get_pos()[0] < self.font.size(self.text)[0]+self.pos[0]) and (self.pos[1] < pointer.get_pos()[1] < self.font.size(self.text)[1]+self.pos[1]):
            return True
        return False

    def draw(self, win) -> None:
        win.blit(self.font.render(self.text, True, (0,0,0)), self.pos)

class Line:

    def __init__(self, start, end, color=None) -> None:
        self.start = start
        self.end = end
        if not color:
            self.color = (0,0,0)
        else:
            self.color = color
        self.length = int(math.sqrt(((start[0]-end[0])**2)+((start[1]-end[1])**2)))
        self.direction = [(end[0] - start[0]), (end[1] - start[1])]
        #this to avoid division by 0 if the line is parallel
        if self.direction[0] == 0 or self.direction[1] == 0:
            self.direction[0] = 1
            self.direction[1] = 1
        self.direction = (self.direction[0]/math.sqrt((self.direction[0]**2)+(self.direction[1]**2)), self.direction[1]/math.sqrt((self.direction[0]**2)+(self.direction[1]**2)))
        self.tangent = (-self.direction[1], self.direction[0])
        """
        Points
        a ----------------- b
        |                   |
        c ----------------- d
        """
        self.a = (start[0]+(self.tangent[0]*5), start[1]+(self.tangent[1]*5))
        self.b = (self.a[0]+(self.direction[0]*(self.length-10))), (self.a[1]+(self.direction[1]*(self.length-10)))
        self.c = (start[0]-(self.tangent[0] * 5), start[1]-(self.tangent[1] * 5))
        self.e = (self.f[0]+(self.direction[0]*(self.length-10))), (self.f[1]+(self.direction[1]*(self.length-10)))

    def draw(self, win) -> None:
        py.draw.polygon(win, (255,0,0), [self.a, self.b, self.d, self.c])

class Connection:

    def __init__(self, name1, name2, pos1, pos2) -> None:
        self.name = [name1, name2]
        self.pos = [pos1, pos2]
        self.line = Line(pos1, pos2)

    def draw(self, win) -> None:
        self.line.draw(win)

class DCity:

    def __init__(self, x, y, name, image, country_value) -> None:
        self.name = name
        self.name_text = Text(x, y+40, self.name)
        self.image = image
        self.color = ((country_value % 10)*(255//10), (country_value % 9)*(255//9), (country_value % 15)*(255//15))
        self.pos = (x, y)

    def is_over(self, pointer) -> bool:
        if (self.pos[0] < pointer.get_pos()[0] < self.font.size(self.text)[0]+self.pos[0]) and (self.pos[1] < pointer.get_pos()[1] < self.font.size(self.text)[1]+self.pos[1]):
            return True
        return False

    def draw(self, win, is_alive) -> None:
        if is_alive:
            py.draw.circle(win, self.color, self.pos, 20)
            if self.image is not None:
                win.blit(self.image, self.pos)
        else:
            py.draw.circle(win, (0,0,0), self.pos, 20)
        

class Window:

    def __init__(self, caption, window_dimensions) -> None:
        py.init()
        py.display.set_caption(caption)
        self.win = py.display.set_mode(window_dimensions)
        self.centre = (window_dimensions[0]/2, window_dimensions[1]/2)
        self.objects = {}

    # Place cities in a circle around the centre of the screen
    def setup_circular(self, cities) -> None:
        for i,city in enumerate(cities.values()):
            city.setup_display(self.centre[0] + math.cos(((2*math.pi)/len(cities))*i)*100), self.centre[1] + (math.sin(((2*math.pi)/len(cities))*i)*100)
            self.objects[city.name] = city
        self.setup_connections()
    
    def setup_connections(self) -> None:
        for city in self.objects.values():
            for city_name in city.self.objects.keys():
                connection_name = f"{city.name}-{city_name}"
                reversed_name = f"{city_name}-{city.name}"
                if connection_name not in self.objects.keys() and reversed_name not in self.objects.keys():
                    self.objects[f"{city.name}-{city_name}"] = Connection(city.name, city_name, city.pos, city.connections[city_name].pos)

    def display_disasters(self) -> None:
        pass

    def draw(self) -> None:
        self.win.fill((255,255,255))
        for obj in reversed(list(self.objects.values())):
            obj.draw(self.win)
        py.display.update()

