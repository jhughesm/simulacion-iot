# Simulación de Edificio con Sensores IoT y Zombis

Este proyecto implementa una simulación de un edificio infestado de zombis, monitoreado por sensores IoT. La aplicación permite visualizar y controlar la propagación de zombis a través de una interfaz CLI.

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/edificio-zombis-iot.git
   cd edificio-zombis-iot
   ```

2. **Requisitos**:
   - Python 3.6 o superior

   No se requieren dependencias adicionales ni instalación de paquetes mediante pip, ya que el proyecto utiliza únicamente módulos estándar de Python.

3. **Ejecutar el programa**:
   ```bash
   python Orchestrator.py
   ```

## Comandos

Al iniciar la aplicación, verás un mensaje de bienvenida y los comandos disponibles:

- **start/restart**: Inicia una nueva simulación.
  - Te pedirá ingresar el número de pisos (entero ≥ 1)
  - Luego te pedirá el número de habitaciones por piso (entero ≥ 1)

- **progress**: Avanza la simulación un día (turno).

- **progress X**: Avanza la simulación X días de una vez (donde X es un número entero positivo).

- **display**: Muestra el estado actual del edificio, con la cantidad de zombis y el estado de los sensores.
  - Los sensores se muestran con un indicador de color:
    - 🟢 Verde: Estado normal, sin zombis
    - 🟡 Amarillo: Estado de alerta, presencia de zombis (1-9)
    - 🔴 Rojo: Estado crítico, alta presencia de zombis (≥10)
  - La notación utilizada es:
    - **F01, F02, F03, etc.**: Indica el número de piso (Floor)
    - **(R01), (R02), (R03), etc.**: Indica el número de habitación (Room) en ese piso
    - El número después de los dos puntos indica la cantidad de zombis en esa habitación

- **sensors**: Muestra información detallada sobre todos los sensores.

- **quit**: Termina la ejecución del programa.

- **commands**: Muestra la lista de comandos disponibles.

## Arquitectura

El proyecto utiliza una arquitectura orientada a objetos que modela de manera jerárquica la estructura del edificio y la lógica de simulación:

### Estado Inicial

Al iniciar una nueva simulación:
- **100 zombis** se generan automáticamente en una habitación aleatoria del edificio
- Los sensores de las habitaciones con zombis entrarán inmediatamente en estado crítico (indicador rojo)
- A partir de ahí, los zombis comenzarán a propagarse siguiendo las reglas de movimiento

### Clases Principales

- **Orchestrator**: Punto de entrada de la aplicación que gestiona la interacción con el usuario y coordina la lógica general.

- **InputHandler**: Maneja la lectura de comandos y validación de entrada del usuario.

- **Simulation**: Controla la lógica de la simulación, incluyendo la generación y propagación de zombis.

- **Building**: Representa la estructura completa del edificio, conteniendo varios pisos.

- **Floor**: Representa un piso del edificio, que contiene varias habitaciones.

- **Room**: Modela una habitación individual que puede contener zombis y tiene un sensor.

- **Sensor**: Representa un sensor IoT que monitorea y reporta la presencia de zombis.

### Patrones de Diseño Implementados

1. **State Buffering**: La simulación implementa un sistema donde:
   - Los cambios en un turno se acumulan primero en variables de incremento (`next_zombis`)
   - Solo después de calcular todos los movimientos, estos se aplican al estado actual con `commit_allocations()`
   - Esto garantiza que todos los movimientos se calculan basados en el mismo estado inicial, evitando por ejemplo que un zombi se mueva dos veces en un mismo día.

2. **Programación Orientada a Objetos (OOP)**: El diseño respeta los principios de encapsulamiento, permitiendo que cada componente maneje su propia lógica interna.

3. **Modelo Jerárquico**: Se utiliza una estructura jerárquica (Building > Floor > Room > Sensor) que emula la organización de un edificio.

### Lógica de Propagación

Los zombis siguen estas reglas de movimiento:
- Cada zombi tiene un 20% de probabilidad de moverse a una habitación adyacente en cada turno
- El 80% restante permanece en su habitación actual
- Las habitaciones adyacentes incluyen:
  - Habitaciones con números consecutivos en el mismo piso (p.ej., R01 es adyacente a R02)
  - **Importante**: Solamente la habitación R01 (la primera/más a la izquierda) de cada piso está conectada con la R01 de los pisos superior e inferior (simulando escaleras)
  - Las demás habitaciones (R02, R03, etc.) solo permiten movimiento horizontal dentro del mismo piso

## Ejemplo de Uso

```
Bienvenido a XSim!

        Los comandos posibles que puedes usar son:
        - start/restart: Comienza una nueva simulación. Te pedirá ingresar el número de pisos y luego el número de habitaciones por piso.
        - progress: Avanza un día
        - progress n: Avanza n días
        - display: abre la interfaz para ver el estado de pisos/habitaciones.
        - sensors: muestra el estado detallado de todos los sensores IoT
        - quit: Termina la ejecución del programa
        - commands: ver la lista de comandos
        

>start
Ingresa el número de pisos (debe ser un número entero mayor o igual a 1):
>3
Ingresa el número de habitaciones por piso (debe ser un número entero mayor o igual a 1):
>4
Simulando programa para 3 pisos y 4 habitaciones por piso.
🔴 ALERTA CRÍTICA en F02/R01 - muchos zombis detectados

>display
<^ --------------------------------------------------------------- ^>
  F03 (R01):   0 🟢 |(R02):   0 🟢 |(R03):   0 🟢 |(R04):   0 🟢
  F02 (R01): 100 🔴 |(R02):   0 🟢 |(R03):   0 🟢 |(R04):   0 🟢
  F01 (R01):   0 🟢 |(R02):   0 🟢 |(R03):   0 🟢 |(R04):   0 🟢
<V --------------------------------------------------------------- V>

>progress
Progresando 1 dia
⚠️  Sensor activado en F03/R01 - zombi detectado
⚠️  Sensor activado en F02/R02 - zombi detectado
⚠️  Sensor activado en F01/R01 - zombi detectado

>display
<^ -------------------------------------------------------------- ^>
  F03 (R01):   6 🟡 |(R02):   0 🟢 |(R03):   0 🟢 |(R04):   0 🟢
  F02 (R01):  80 🔴 |(R02):   9 🟡 |(R03):   0 🟢 |(R04):   0 🟢
  F01 (R01):   5 🟡 |(R02):   0 🟢 |(R03):   0 🟢 |(R04):   0 🟢
<V -------------------------------------------------------------- V>

>quit
Terminando ejecución del programa...
```

## Notas adicionales

- Los sensores cambian automáticamente entre estados normal, alerta y crítico según la cantidad de zombis en su habitación
- Los mensajes de alerta proporcionan información sobre los cambios de estado y la cantidad de zombis detectados
- El sistema está diseñado para ser fácilmente expandible con nuevas funcionalidades
- Para una mejor visualización, se recomienda usar 10 o menos habitaciones por piso. Con más de 10 habitaciones, el display en la terminal puede volverse menos legible dependiendo del ancho de la ventana
