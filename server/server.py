import socket
import threading
import pickle

HOST = "localhost"
PORT = 5555

players = {}
lock = threading.Lock()

def handle_client(conn, addr):
    global players
    print(f"[NEW CONNECTION] {addr} connected.")
    
    conn.send(pickle.dumps(players))
    
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            player_data = pickle.loads(data)

            with lock:
                players[addr] = player_data[:3]
                if len(player_data) > 3:
                    del players[player_data[3]]
                conn.sendall(pickle.dumps(players))
    except:
        print(f"[DISCONNECT] {addr} disconnected.")
    finally:
        with lock:
            if addr in players.keys():
                del players[addr]
        conn.close()

def update_bullets():
    global bullets
    print("[ TEST ] Updating bullets...")
    for bullet in bullets:
        print("[TEST] Bullet:", bullet)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTING] Server is starting...{HOST=}, {PORT=}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
