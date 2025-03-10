class Sensor:
    def __init__(self, room):
        self.status = 'normal'  # 'normal', 'alert', 'critical'
        self.room = room
        self.activation_history = []  
        self.current_turn = 0
        
    def check_zombies(self):
        if self.room.current_zombies == 0:
            new_status = 'normal'
        elif self.room.current_zombies >= 10: 
            new_status = 'critical'
        else:
            new_status = 'alert'
            
        if new_status != self.status:
            self.change_status(new_status)
            
    def change_status(self, new_status):
        old_status = self.status
        self.status = new_status
        
        if old_status != new_status:
            room_id, floor_id = self.room.position
            
            # Transición de normal a alert
            if old_status == 'normal' and new_status == 'alert':
                print(f"\033[93m⚠️  Sensor activado en F{floor_id:02d}/R{room_id:02d} - zombi detectado\033[0m")
            
            # Transición de normal o alert a critical
            elif new_status == 'critical':
                print(f"\033[91m🔴 ALERTA CRÍTICA en F{floor_id:02d}/R{room_id:02d} - muchos zombis detectados\033[0m")
            
            # Transición de critical a alert (reducción de zombis)
            elif old_status == 'critical' and new_status == 'alert':
                print(f"\033[93m⚠️  Reducción de amenaza en F{floor_id:02d}/R{room_id:02d} - nivel de alerta\033[0m")
            
            # Transición a normal
            elif new_status == 'normal':
                print(f"\033[92m✅ Sensor vuelve a estado normal en F{floor_id:02d}/R{room_id:02d}\033[0m")
                
    def get_status_symbol(self):
        if self.status == 'normal':
            return "\033[92m●\033[0m"  # Verde
        elif self.status == 'alert':
            return "\033[93m●\033[0m"  # Amarillo
        elif self.status == 'critical':
            return "\033[91m●\033[0m"  # Rojo
        return "○"  # Por defecto
        
    def get_summary(self):
        if not self.activation_history:
            return "Sin activaciones"
            
        first_activation = self.activation_history[0][0]
        activations_count = len(self.activation_history)
        max_zombies = max([count for _, count in self.activation_history])
        
        return f"Primera detección: turno {first_activation}, {activations_count} activaciones, máx zombis: {max_zombies}"