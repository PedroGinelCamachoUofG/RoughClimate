# holds the classes for the cities
import random
import math
import logic
import display
from functools import reduce
from operator import add
city_names = ["Tokyo", "Delhi", "Shanghai", "Sao Paulo", "Mexico City", "Cairo", "Mumbai", "Beijing", "Dhaka", "Osaka", "New York", "Karachi", "Buenos Aires", "Chongqing", "Istanbul", "Kolkata", "Manila", "Lagos", "Rio de Janeiro", "Tianjin", "Kinshasa", "Guangzhou", "Los Angeles", "Moscow", "Shenzhen", "Lahore", "Bangalore", "Paris", "Bogota", "Jakarta", "Chennai", "Lima", "Bangkok", "Seoul", "Nagoya", "Hyderabad", "London", "Tehran", "Chicago", "Luanda", "Kuala Lumpur", "Riyadh", "Madrid", "Dar es Salaam", "Singapore", "Khartoum", "Alexandria", "Yangon", "Guadalajara", "Glasgow"]
country_names = ["Moldova", "Greater Albania", "Ivan"]
disasters = ["Flood", "Hurricane", "Heatwave"]

def clamp(number, min=-100, max=0) -> int:
    if number < min:
        return min
    elif number > max:
        return max
    return number

def ord_add(word):
    return reduce(add, [ord(letter) for letter in word])

class Game:

    def __init__(self, city_num) -> None:
        self.cities = self.setup_cities(city_num)
        self.round_num = 0
        self.window = display.Window("Game", (700, 450))
        self.window.setup_circular(self.cities)
        
    def setup_cities(city_num) -> dict:
        # State is hardcoded now but could be edited or randomized
        city_name_sections = len(city_names//city_num)
        city_dict = {}
        for i in range(city_num):
            random_name = city_names[random.randint(i*city_name_sections, (i+1)*city_name_sections)]
            random_country = random.choice(country_names)
            luck = ord_add(random_country)#I am assuming luck can not go over 2000
            population = random.randint(10000,1000000)
            city_dict[random_name] = City(random_name, 
                                          logic.first_action, 
                                          logic.response_action, 
                                          logic.last_action,
                                          random_country,
                                          population,#population
                                          random.randint(1,5)*(luck//500),#defences
                                          random.randint(1,5)*luck*100,#infrastructure
                                          random.randint(10,40)*population,#food *math.ceil(luck*0.0015)
                                          random.randint(50,700),#iron
                                          random.randint(1000, 80000)#wood
                                          )
        # create connections
        for from_city in city_dict.items():
            for to_city in city_dict.items():

                if to_city.name not in from_city.connections.keys():
                    if from_city.country == to_city.country:
                        if random.randint(1,10) > 3:
                            from_city[to_city.name] = to_city
                            to_city[from_city.name] = from_city
                    else:
                        if random.randint(1,10) > 7:
                            from_city[to_city.name] = to_city
                            to_city[from_city.name] = from_city
            
            # make sure all cities are connected
            if not from_city.connections:
                random_city = random.choice(city_dict)
                from_city[random_city.name] = random_city
                random_city[from_city.name] = from_city

        return city_dict

    def is_game_over(self) -> bool:
        for city in self.cities.items():
            if city.is_alive:
                return False
        return True

    def trigger_first(self) -> None:
        print(f"START Round {self.round_num}")
        for city in self.cities.items():
            city.first_action(self)

    def trigger_response(self) -> None:
        for city in self.cities.items():
            city.response_action(self)

    def trigger_last(self) -> None:
        for city in self.cities.items():
            city.last_action(self)
        print(f"END Round {self.round_num}")
        self.round_num += 1

    def trigger_climate(self) -> None:
        threshold = random.randint(0,25) * self.round_num
        for city in self.cities.items():
            if random.randint(1,1000) > threshold:
                city.receive_disaster(self.round_num)

    def count_damages(self) -> dict:
        report_dict = {}
        damage = 0
        for city in self.cities.items():
            report_dict[city.name] = city.report_damage()
            damage += report_dict[city.name]["total damage"]
        report_dict["damage"] = damage
        return report_dict
    
    def communicate_cities(self) -> None:
        report_list = []
        for city in self.cities.items():
            report_list.append(city.report_damages())
        for city in self.cities.items():
            city.receive_reports(report_list)

    def consume_food(self) -> None:
        for city in self.cities.items():
            city.food -= city.population

    def draw(self) -> None:
        self.window.draw()


class City:
    id = 0
    def __init__(self, name, first_action, response_action, last_action, country, population, defences, infrastructure, food, iron, wood) -> None:
        self.id = id
        id += 1
        self.name = name
        self.is_alive = True
        # Map setup
        self.country = country
        self.connections = {}
        self.disaster_distribution = [random.randint(0,2) for i in range(5)]
        # City setup
        self.prev_population = 0
        self.population = population
        self.prev_defences = 0
        self.defences = defences
        self.prev_infrastructure = 0
        self.infrastructure = infrastructure
        self.prev_wood = 0
        self.wood = wood # for reparing infrastructure
        self.prev_food = 0
        self.food = food # for feeding people, if you don't have enough damages start going up
        self.prev_iron = 0
        self.iron = iron # for making defences
        # Communications
        self.communications = []
        # Action setup
        self.first_action = first_action
        self.response_action = response_action
        self.last_action = last_action
        # Misc
        self.building_done = False
        self.infrastructure_used = 0
        # Display
        self.display_object = None

    def setup_display(self, x, y) -> None:
        self.display_object = display.DCity(x, y, self.name, None, ord_add(self.country))

    def get_connections(self) -> dict:
        return self.connections
    
    def get_reports(self) -> list:
        return self.communications

    def build_defences(self) -> bool:
        if self.iron > 10 and not self.building_done and self.defences < 100:
            self.iron -= 10
            self.defences += 10
            self.building_done = True
            return True
        return False
    
    def build_infrastructure(self) -> bool:
        if self.wood > 0 and not self.building_done:
            if self.wood < 500:
                self.infrastructure += self.wood
                self.wood = 0
            else:
                self.infrastructure += 500
                self.wood -= 500
            self.building_done = True
            return True
        return False
    
    # Please refactor this bologneise of a function
    def send_resources(self, type, quantity, receiver) -> bool:
        operation_performed = False
        if receiver in self.connections.keys and quantity > 0:
            if quantity > self.infrastructure-self.infrastructure_used:
                quantity = clamp(quantity, min=0, max=self.infrastructure-self.infrastructure_used)
                self.infrastructure_used = self.infrastructure
                print(f"Infrastructure only allowed to send {quantity} {type}")
            if type == "wood":
                if quantity < self.wood:
                    print(f"{self.name} sending {quantity} {type} to {receiver}")
                    non_received = self.connections[receiver].receive_resources(type, quantity, self.name)
                    self.wood -= quantity+non_received
                    operation_performed = True
                    if non_received == -1:
                        self.wood += 1
                        operation_performed = False
                else:
                    print(f"{self.name} wanted to send {quantity} {type} but only had {self.wood} {type}")
            elif type == "iron":
                if quantity < self.iron:
                    print(f"{self.name} sending {quantity} {type} to {receiver}")
                    non_received = self.connections[receiver].receive_resources(type, quantity, self.name)
                    self.iron -= quantity+non_received
                    operation_performed = True
                    if non_received == -1:
                        self.iron += 1
                        operation_performed = False
                else:
                    print(f"{self.name} wanted to send {quantity} {type} but only had {self.iron} {type}")
            elif type == "food":
                if quantity < self.food:
                    print(f"{self.name} sending {quantity} {type} to {receiver}")
                    non_received = self.connections[receiver].receive_resources(type, quantity, self.name)
                    self.iron -= quantity+non_received
                    operation_performed = True
                    if non_received == -1:
                        self.food += 1
                        operation_performed = False
                else:
                    print(f"{self.name} wanted to send {quantity} {type} but only had {self.food} {type}")
        return operation_performed
    
    def receive_resources(self, type, quantity, sender) -> int:
        if sender in self.connections.keys and quantity > 0:
            if quantity > self.infrastructure-self.infrastructure_used:
                quantity = clamp(quantity, min=0, max=self.infrastructure-self.infrastructure_used)
                self.infrastructure_used = self.infrastructure
                print(f"{self.name}'s infrastructure only allowed to receive {quantity} {type}")
            if type == "wood":
                self.wood += quantity
            elif type == "iron":
                self.iron += quantity
            elif type == "food":
                self.food += quantity
            print(f"{self.name} receiving {quantity} {type} from {sender}")
            return quantity
        return -1

    def first_action(self) -> None:
        self.building_done = False
        self.infrastructure_used = 0
        self.first_action(self)

    def response_action(self) -> None:
        self.response_action(self)

    def last_action(self) -> None:
        self.last_action(self)

    def report_damages(self) -> dict:
        #Make the report
        report = {"name" : self.name,
                  "country" : self.country,
                  "population difference" : self.population - self.prev_population,
                  "defences difference" : self.defences - self.prev_defences,
                  "infrastructure difference" : self.infrastructure - self.prev_infrastructure,
                  "total damage" : (self.population - self.prev_population) +  (self.defences - self.prev_defences) + (self.infrastructure - self.prev_infrastructure),
                  "food difference" : self.food - self.prev_food,
                  "iron difference" : self.iron - self.prev_iron,
                  "wood difference" : self.wood - self.prev_wood,
                  "population" : self.population,
                  "defences" : self.defences,
                  "infrastructure" : self.infrastructure,
                  "food" : self.food,
                  "iron" : self.iron,
                  "wood" : self.wood
                  }
        #Prepare for next round
        self.prev_population = self.population
        self.prev_defences = self.defences
        self.prev_infrastructure = self.infrastructure
        self.prev_food = self.food
        self.prev_iron = self.iron
        self.prev_wood = self.wood
        #Check if the city is alive or not
        if self.population <= 0 or self.infrastructure <= 0:
            self.is_alive = False
            print(f"City {self.name} is no more")

        return report
    
    def receive_reports(self, report_list) -> None:
        self.communications = report_list
    
    def receive_disaster(self, round_num) -> (str,int):
        event = Disaster(self.disaster_distribution, round_num)
        self.population -= clamp(self.defences - event.population_damage)
        self.infrastructure -= clamp(self.defences - event.infrastructure_damage)
        self.wood -= clamp(self.defences - event.wood_damage)
        self.food -= clamp(self.defences - event.food_damage)
        self.iron -= clamp(self.defences - event.iron_damage)
        return event.type, event.severity

    def draw(self):
        self.display_object.draw(self.win, self.is_alive)

class Disaster:

    def __init__(self, chances, modifier) -> None:
        self.type = disasters[int(random.choice(chances))]
        self.population_damage = 0
        self.infrastructure_damage = 0
        self.wood_damage = 0
        self.food_damage = 0
        self.iron_damage = 0
        # value between 1 and 100, the lower the worse it is
        self.severity = random.randint(1,10) * random.randint(1,10) * (modifier/100)
        self.set_values()

    def set_values(self) -> None:
        if self.type == "Flood":
            self.population_damage = math.ceil(50/self.severity)
            self.infrastructure_damage = math.ceil(100/self.severity)
            self.wood_damage = math.ceil(100/self.severity)
            self.food_damage = math.ceil(10/self.severity)
            self.iron_damage = math.ceil(10/self.severity)
        elif self.type == "Hurricane":
            self.population_damage = math.ceil(10/self.severity)
            self.infrastructure_damage = math.ceil(70/self.severity)
            self.wood_damage = math.ceil(50/self.severity)
            self.food_damage = math.ceil(50/self.severity)
            self.iron_damage = math.ceil(50/self.severity)
        elif self.type == "Heatwave":
            self.population_damage = math.ceil(20/self.severity)
            self.infrastructure_damage = math.ceil(30/self.severity)
            self.wood_damage = math.ceil(10/self.severity)
            self.food_damage = math.ceil(100/self.severity)
            self.iron_damage = math.ceil(10/self.severity)