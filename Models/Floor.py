from Models.Room import Room

class Floor:
    def __init__(self, z, room_num):
        self.z = z
        self.room_num = room_num
        self._generate_rooms()
        

    def _generate_rooms(self):
        self.rooms = {i+1:Room((i+1, self.z)) for i in range(self.room_num)}

    def display(self):
        room_displays = [self.rooms[room_id].display() for room_id in self.rooms]
        return f"  F{self.z:02d} {' |'.join(room_displays)}\n"
    
    def commit_allocations(self):
        for room_id in self.rooms:
            self.rooms[room_id].commit_allocations()