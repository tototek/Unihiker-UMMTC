from unihiker import GUI
import requests  # Para hacer las solicitudes HTTP
import time
# Inicializar GUI
gui = GUI()

# Estados iniciales de luces y tomas
relay_states = {1: "OFF", 2: "OFF", 3: "OFF", 4: "OFF"}

# Crear LEDs para mostrar estado (cuadrados)
led_colors = {1: "red", 2: "red", 3: "red", 4: "red"}

# Función para manejar los clics de los botones individuales
def toggle_relay(relay_num, on_url, off_url):
    if relay_states[relay_num] == "OFF":
        relay_states[relay_num] = "ON"
        led_colors[relay_num] = "green"  # LED verde si está encendido
        requests.get(on_url)  # Enviar comando para encender el relé
    else:
        relay_states[relay_num] = "OFF"
        led_colors[relay_num] = "red"    # LED rojo si está apagado
        requests.get(off_url)  # Enviar comando para apagar el relé
    # Redibujar LED
    draw_led(relay_num)

# Función para dibujar los LEDs cuadrados
def draw_led(relay_num):
    x_pos = 150  # Posición en X fija para los LEDs
    y_pos = 60 + (relay_num - 1) * 60  # Posición en Y, según el botón
    gui.fill_rect(x=x_pos, y=y_pos, w=20, h=20, color=led_colors[relay_num])  # Dibujar LED cuadrado

# Función para manejar los botones TODO ON y TODO OFF  
def toggle_all(state, on_urls, off_urls):
    for i in range(1, 5):
        if state == "ON":
            requests.get(on_urls[i-1])  # Enviar comando para encender el relé
            relay_states[i] = "ON"
            led_colors[i] = "green"
        else:
            requests.get(off_urls[i-1])  # Enviar comando para apagar el relé
            relay_states[i] = "OFF"
            led_colors[i] = "red"
        draw_led(i)

# Dibujar texto en la parte superior
gui.draw_text(text="UMMTC control X10", x=120, y=10, font_size=16, origin="center", color="blue")

# Añadir los botones para controlar luces y tomas en formato vertical
def draw_button(relay_num, label, on_url, off_url):
    x_pos = 50  # Posición en X fija para los botones
    y_pos = 50 + (relay_num - 1) * 60  # Posición en Y, según el botón
    gui.add_button(x=x_pos, y=y_pos, w=80, h=40, text=label, 
                   onclick=lambda: toggle_relay(relay_num, on_url, off_url))

# Añadir los botones TODO ON y TODO OFF
def draw_special_button(x, y, label, state, on_urls, off_urls):
    gui.add_button(x=x, y=y, w=100, h=50, text=label, 
                   onclick=lambda: [toggle_all(state, on_urls, off_urls),
                                    gui.draw_text(text=label, x=x + 50, y=y + 25, 
                                                  font_size=20, color="blue")])

# URLs para encender/apagar los relés (asumiendo un ESP controlado por HTTP)
on_urls = [
    "http://192.168.100.40:8001/a/1/on",   # URL para encender LUZ1
    "http://192.168.100.40:8001/a/2/on",   # URL para encender LUZ2
    "http://192.168.100.40:8001/a/3/on",   # URL para encender TOMA1
    "http://192.168.100.40:8001/a/4/on"    # URL para encender TOMA2
]

off_urls = [
    "http://192.168.100.40:8001/a/1/off",  # URL para apagar LUZ1
    "http://192.168.100.40:8001/a/2/off",  # URL para apagar LUZ2
    "http://192.168.100.40:8001/a/3/off",  # URL para apagar TOMA1
    "http://192.168.100.40:8001/a/4/off"   # URL para apagar TOMA2
]

# Dibuja los botones para luces y tomas con LEDs cuadrados
labels = ["Luces1", "Luces2", "Toma1", "Toma2"]
for i in range(1, 5):
    draw_button(i, labels[i-1], on_urls[i-1], off_urls[i-1])  # Dibujar botones en formato vertical
    draw_led(i)  # Dibujar LEDs cuadrados al lado de cada botón



# Bucle para mantener el programa en ejecución
while True:
    time.sleep(1)
