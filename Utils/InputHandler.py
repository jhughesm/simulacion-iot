class InputHandler:

    @staticmethod
    def welcome():
        print("Bienvenido a XSim!")
    
    @staticmethod
    def show_commands():
        print("""
        Los comandos posibles que puedes usar son:
        - start/restart: Comienza una nueva simulación. Te pedirá ingresar el número de pisos y luego el número de habitaciones por piso.
        - progress: Avanza un día
        - progress n: Avanza n días
        - display: abre la interfaz para ver el estado de pisos/habitaciones.
        - sensors: muestra el estado detallado de todos los sensores IoT
        - quit: Termina la ejecución del programa
        - commands: ver la lista de comandos
        """)

    @staticmethod
    def require_start(command):
        print(f"Por favor comienza una nueva simulación antes de usar el comando '{command}'")

    @staticmethod
    def get_valid_integer(prompt, error_message, min_value=1):
        """Solicita al usuario un número entero válido."""
        print(prompt)
        while True:
            user_input = input().strip()
            
            # Verificar si el usuario quiere cancelar
            if user_input.lower() == 'cancel':
                return None
                
            # Validar entrada
            if user_input.isdigit() and int(user_input) >= min_value:
                return int(user_input)
            else:
                print(error_message)
                print("Ingresa un número válido o escribe 'cancel' para cancelar:")

    @staticmethod
    def require_start_params():
        print("""
                Para usar el comando 'start' y comenzar una nueva
                simulación, deberás escribir 'start X Y' donde X es el
                número de pisos e Y es el número de habitaciones. 
            
                Ej: 'start 2 3' simulará un edificio de 2 pisos y 
                3 habitaciones por piso.""")

    @staticmethod
    def unknown_command(command):
        print(f'Comando desconocido: {command}')

    @staticmethod
    def unknown_progress_days(param):
        print(f'Valor no aceptado de días de progreso: {param}')
            
    @staticmethod
    def _translate_input(user_input):
        user_input = user_input.strip(' \n\t')
        if len(user_input) == 0: 
            return {'command':'', 'params':[]}
        user_input_list = user_input.split(' ')
        if len(user_input_list) == 1:
            return {'command': user_input_list[0], 'params':[]}
        return {'command': user_input_list[0], 'params': user_input_list[1:]}
    
    @staticmethod
    def require_display():
        print(f"Para poder mostrar más habitaciones requieres primero de usar el comando 'display'")
    
    @classmethod
    def wait_for_input(cls):
        user_input = input()
        return cls._translate_input(user_input)
        


        
    