from Models.Sensor import Sensor


class Room:
    def __init__(self, position, current_zombies=0):
        self.position = position
        self.current_zombies = current_zombies
        self.next_zombies = 0
        self.sensor = Sensor(self)

    def display(self):
        status_symbol = self.sensor.get_status_symbol()
        return f'(R{self.position[0]:02d}):{self.current_zombies:4d} {status_symbol}'
    
    def allocate_zombies(self, amount):
        self.next_zombies += amount
        self.sensor.check_zombies()

    def remove_zombies(self, amount):
        self.next_zombies -= amount
        self.sensor.check_zombies()

    def commit_allocations(self):
        self.current_zombies += self.next_zombies
        self.next_zombies = 0
        self.sensor.check_zombies()