import socket
import json
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

HOST ='aqui la ip del hotspot'  # IP del servidor (hotspot)
PORT = 65432

def generar_datos(id_dron): # Genera datos aleatorios para el dron
    return {
        "Dron": id_dron,
        "Latitud": round(np.random.uniform(-33.5, -33.4), 6), # Latitud de Santiago, Chile
        "Longitud": round(np.random.uniform(-70.7, -70.6), 6), # Longitud de Santiago, Chile
        "Batería": round(np.random.uniform(0, 100), 2), # Porcentaje de batería
        "Peso Paquete": round(np.random.uniform(0.5, 5), 2) # Peso del paquete en kg
    }

def graficar_datos(lista_datos, id_dron): # Grafica los datos enviados por el dron
    lat = [d['Latitud'] for d in lista_datos] # Latitud
    lon = [d['Longitud'] for d in lista_datos] # Longitud
    bat = [d['Batería'] for d in lista_datos] # Porcentaje de batería
    peso = [d['Peso Paquete'] for d in lista_datos] # Peso del paquete en kg

    fig = plt.figure() # Crear una figura para las gráficas
    ax = fig.add_subplot(121, projection='3d')
    ax.scatter(lat, lon, bat, c='blue', marker='o')
    ax.set_title(f'{id_dron} - Latitud vs Longitud vs Batería')
    ax.set_xlabel('Latitud')
    ax.set_ylabel('Longitud')
    ax.set_zlabel('Batería')

    ax2 = fig.add_subplot(122) # Crear un segundo subplot para la gráfica 2D
    ax2.plot(bat, peso, 'r*-')
    ax2.set_title(f'{id_dron} - Batería vs Peso')
    ax2.set_xlabel('Batería (%)')
    ax2.set_ylabel('Peso (kg)')

    plt.tight_layout() # Ajustar el layout para que no se solapen
    plt.show() # Mostrar las gráficas

def main(): # Función principal del cliente
    id_dron = input("ID del dron: ").strip() # Solicitar ID del dron al usuario
    datos_enviados = [] # Lista para almacenar los datos enviados

    try: # Conectar al servidor y enviar datos
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crear un socket TCP
        s.connect((HOST, PORT)) # Conectar al servidor
        print(f"[{id_dron}] Conectado al servidor.") # Conectar al servidor

        for _ in range(5): # Enviar 5 conjuntos de datos
            datos = generar_datos(id_dron) # Generar datos aleatorios
            datos_enviados.append(datos) # Almacenar los datos enviados
            s.sendall(json.dumps(datos).encode()) # Enviar los datos al servidor
            print(f"[{id_dron}] ENVIADO: {datos}") # Imprimir los datos enviados
            time.sleep(2) # Esperar 2 segundos antes de enviar el siguiente conjunto de datos

        s.close() # Cerrar el socket
        print(f"[{id_dron}] Desconectado.") # Desconectar del servidor
        graficar_datos(datos_enviados, id_dron) # Graficar los datos enviados

    except Exception as e: # Manejar excepciones
        print(f"[{id_dron}] ERROR: {e}") # Imprimir el error

if __name__ == "__main__": # Punto de entrada del script
    main()
