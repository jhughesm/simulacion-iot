from Models.Floor import Floor

class Building:
    def __init__(self, floor_num, room_num):
        self.floor_num = floor_num
        self.room_num = room_num
        self.floors = {i+1: Floor(i+1 , self.room_num) for i in range(self.floor_num)}

    def display(self):
        floor_displays = [self.floors[floor_id].display() for floor_id in self.floors]

        def visible_length(s):
            # Los codigos ANSI comienzan con \033[ y terminan con m
            length = 0
            i = 0
            while i < len(s):
                if s[i:i+2] == '\033[':
                    # Saltar hasta encontrar 'm' que cierra el código ANSI
                    while i < len(s) and s[i] != 'm':
                        i += 1
                    i += 1  # Saltar la 'm'
                else:
                    length += 1
                    i += 1
            return length

        # Usa la función visible_length para calcular el ancho real
        max_length = max(visible_length(display) for display in floor_displays)

        top_border = "<^ " + "-" * (max_length - 4) + " ^>"


        bottom_border = "<V " + "-" * (max_length - 4) + " V>"

        all_building = [top_border]
        all_building.extend(floor_displays[::-1])
        all_building.append(bottom_border)
        return "\n".join(all_building)


    def allocate_zombies(self, position, amount):
        room_id, floor_id = position
        self.floors[floor_id].rooms[room_id].allocate_zombies(amount)

    def get_room_neighbors(self, room_position):
        room_id, floor_id = room_position
        neighbors = []

        ## If room_id is 1 (the one with stairs): Floor 1...f_id...n-1 neighbors room in floor f_id+1
        if room_id == 1 and self.floor_num > 1 and floor_id < self.floor_num:
            neighbors.append(self.floors[floor_id + 1].rooms[1])

        ## If room_id is 1 (the one with stairs): Floor 2...f_id...n neighbors room in floor f_id-1
        if room_id == 1 and self.floor_num > 1 and floor_id > 1:
            neighbors.append(self.floors[floor_id - 1].rooms[1])


        ## If 1...r_id...n-1 then add r_id+1 as neighbor
        if self.room_num > 1 and room_id < self.room_num:
            neighbors.append(self.floors[floor_id].rooms[room_id+1])

        ## If 2...r_id...n then add r_id-1 as neighbor
        if self.room_num > 1 and room_id > 1:
            neighbors.append(self.floors[floor_id].rooms[room_id-1])

        return neighbors

    def commit_allocations(self):
        for floor_id in self.floors:
            self.floors[floor_id].commit_allocations()




        