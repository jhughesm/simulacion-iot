from Utils.InputHandler import InputHandler
from Simulation import Simulation

class Orchestrator:

    def __init__(self):
        self.simulation = None
        self.input_handler = InputHandler()
        self.end = False


    def main(self):

        self.input_handler.welcome()
        self.input_handler.show_commands()
        while True:
            command_dict = self.input_handler.wait_for_input()

            if self.end:
                break
            
            if command_dict['command'] in ['progress', 'display'] and not self.simulation:
                self.input_handler.require_start(command_dict['command'])
                continue

            self.process_command(command_dict)

    def process_command(self, command_dict):
        command = command_dict['command']
        params = command_dict['params']
        command_map = {
            'start': (self.start, 0),
            'restart': (self.start, 0),
            'progress': (self.progress, 1),
            'display': (self.display, 1),  
            'sensors': (self.sensors, 0),
            'quit': (self.quit, 0),
            'commands': (self.commands, 0)
        }
        if command in command_map:
            method, max_params = command_map[command]
            return method(*params[:max_params])
        
        self.input_handler.unknown_command(command)
        return
                

    def start(self, *args):
        prompt_pisos = "Ingresa el número de pisos (debe ser un número entero mayor o igual a 1):"
        error_pisos = "Número de pisos inválido. Debe ser un número entero mayor o igual a 1."
        floor_num = self.input_handler.get_valid_integer(prompt_pisos, error_pisos)
        
        if floor_num is None:
            return 
        
        prompt_habitaciones = "Ingresa el número de habitaciones por piso (debe ser un número entero mayor o igual a 1):"
        error_habitaciones = "Número de habitaciones inválido. Debe ser un número entero mayor o igual a 1."
        room_num = self.input_handler.get_valid_integer(prompt_habitaciones, error_habitaciones)
        
        if room_num is None:
            return  
        
        self.simulation = Simulation(floor_num, room_num)
        return
    
    
    def progress(self, *args):
        if not self.simulation:
            self.input_handler.require_start('progress')

        elif len(args) < 1:
            self.simulation.progress()

        elif args[0].isdigit() and int(args[0]) >= 1:
            self.simulation.progress(days=args[0])

        else: 
            self.input_handler.unknown_progress_days(args[0])

        return
    
    def display(self, floor_id=None):
        if not self.simulation:
            self.input_handler.require_start('display')
            return
            
        if floor_id and floor_id.isdigit() and int(floor_id) in self.simulation.building.floors:
            floor = self.simulation.building.floors[int(floor_id)]
            print(f"Mostrando estado del piso {floor_id}:")
            print(floor.display())
        else:
            self._display()
        return
    
    def _display(self):
        self.simulation.display()

    def quit(self):
        self.end = True
        print("Terminando ejecución del programa...\nPresiona cualquier tecla para salir")
        return
    

    def commands(self):
        self.input_handler.show_commands()
        return
    
    def sensors(self):
        if not self.simulation:
            self.input_handler.require_start('sensors')
            return
                
        print("\n===== Estado de los Sensores IoT =====")
        
        floors_to_show = self.simulation.building.floors
        
        for f_id, floor in floors_to_show.items():
            print(f"\nPiso {f_id}:")
            for r_id, room in floor.rooms.items():
                status_text = {
                    'normal': "\033[92mNormal\033[0m",
                    'alert': "\033[93mAlerta\033[0m",
                    'critical': "\033[91mCrítico\033[0m"
                }.get(room.sensor.status, room.sensor.status)
                
                print(f"  Habitación {r_id}: {status_text} - {room.sensor.get_summary()}")



if __name__ == "__main__":
    orch = Orchestrator()
    orch.main()


