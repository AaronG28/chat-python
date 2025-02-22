import socket # maneja la conexion entre computadoras.
import threading # Maneja multiples tareas a la vez.
import random # para generar codigos de conexion

# Función para recibir mensajes
def receive_messages(sock):
    '''
    Esta función se ejecuta en un hilo separado y recibe mensajes del socket.
    '''
    while True:
        try:
            message = sock.recv(1024).decode() # recibe el mensaje con maximo 1024 bytes.
            if message:
                print(f"\n{message}") # muestra el mensaje en la pantalla
        except:
            print("Se perdió la conexión.")
            sock.close() # Si se cierra la conexión termina el bucle
            break

# Función para enviar mensajes
def send_messages(sock, name):
    """
    Esta función permite al usuario escribir y enviar mensajes.
    """
    while True:
        message = input() # captura el mensaje desde la consola
        if message.lower() == "exit": # se cierra la conxión
            sock.close()
            break
        sock.send(f"{name}: {message}".encode()) #se envia el mensaje (Nombre: mensaje)

# Función principal
def main():
    print("Bienvenido al chat!")
    name = input("Ingresa tu nombre: ")
    mode = input("¿Quieres (1) crear una sala o (2) unirte a una? ")

    # Si el usuario elige crear una sala
    if mode == "1": 
        code = random.randint(1000, 9999) # genera un codigo de conexion aleatorio (puerto)
        print(f"Código de conexión: {code}") # muestra el codigo
        
        # crea un socket para recibir conexiones
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", code))
        server.listen(1) # pone el servidor en modo receptor (solo 1 conexion)
        print("Esperando conexión...")
        conn, addr = server.accept()
        print(f"Conectado con {addr}") #muestra la ip del otro ordenador
    
    # Si el ussuario elige unirse a una sala
    elif mode == "2":
        host = input("Ingresa la dirección IP del host: ")
        code = int(input("Ingresa el código de conexión: "))
        
        # Crea un socket para conectarse al servidor
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, code)) # para conectarse al servidor y puerto
        print("Conectado!")
    
    else:
        print("Opción no válida.")
        return

    # Iniciar hilos para enviar y recibir mensajes
    threading.Thread(target=receive_messages, args=(conn,)).start()
    send_messages(conn, name) # se envia el mensaje

if __name__ == "__main__":
    main()
