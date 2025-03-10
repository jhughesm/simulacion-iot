from Models.Building import Building
import random

class Simulation:

    def __init__(self, floor_num, room_num):
        self.building = Building(floor_num, room_num)
        self.floor_num = floor_num
        self.room_num = room_num
        self.simulate()

    def simulate(self):
        texto_pisos = f'{self.floor_num} pisos'
        if self.building.floor_num == 1:
            texto_pisos = '1 piso'

        texto_habitaciones = f'{self.room_num} habitaciones'
        if self.building.room_num == 1:
            texto_habitaciones = '1 habitación'
        print(f"Simulando programa para {texto_pisos} y {texto_habitaciones} por piso.")
        self.generate_zombies(total_zombies=100)


    def progress(self, days=1):
        days = int(days)
        print(f'Progresando {days} dia{'s' if days > 1 else ''}') 
        for _ in range(days):
            for floor_id in self.building.floors:
                for room_id in self.building.floors[floor_id].rooms:
                    room = self.building.floors[floor_id].rooms[room_id]
                    if room.current_zombies > 0:
                        ## Check which are the neighbooring rooms
                        neighbors = self.building.get_room_neighbors(room.position)

                        ## Allocate/Remove Zombies from corresponding rooms
                        self.move_room_zombies(room, neighbors)
        
            self.building.commit_allocations()

    def generate_zombies(self, total_zombies=10, mode='one'):

        if mode == 'random':
            allocated_zombies = 0
            while allocated_zombies < total_zombies:
                remaining_allocations = total_zombies - allocated_zombies 

                ## Randomize new allocation position
                next_allocation_position = random.randint(1, self.room_num), random.randint(1, self.floor_num)

                ## Randomize new allocation amount
                next_allocation_amount = random.randint(1, remaining_allocations)

                ## Allocate zombies
                self.building.allocate_zombies(next_allocation_position, next_allocation_amount)
                allocated_zombies += next_allocation_amount
        
        else:
            allocation_position = random.randint(1, self.room_num), random.randint(1, self.floor_num)
            self.building.allocate_zombies(allocation_position, total_zombies)
        
        self.building.commit_allocations()

            
    def move_room_zombies(self, room, neighbors):
        moved_zombies = 0

        if not neighbors:
            return

        for _ in range(room.current_zombies):

            ## 20% chance de moverse por cada zombi
            if (random.random() < 0.2):
                
                ## Se elige una pieza vecina a la que se moverá
                chosen_neighbor = random.choice(neighbors)
                chosen_neighbor.allocate_zombies(amount=1)
                
                ## Aumenta la cantidad de zombis moviendose
                moved_zombies += 1

        if moved_zombies > 0:
            room.remove_zombies(moved_zombies)

    def display(self):
        print(self.building.display())