import socket
import json
import time

HEARTBEAT_TIMEOUT = 15  # secondes
LISTEN_IP = "127.0.0.4"   # IP boîte 4
LISTEN_PORT = 9998        # port dédié pour heartbeat de boîte 5

last_heartbeat_box5 = None

def listen_heartbeat_box5():
    global last_heartbeat_box5
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_IP, LISTEN_PORT))
    sock.settimeout(5)

    print(f"[CHECK5 BOX4] Écoute heartbeat de BOX5 sur {LISTEN_IP}:{LISTEN_PORT}")

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = json.loads(data.decode())
            if message.get("boite") == "BOX5":
                last_heartbeat_box5 = time.time()
                print(f"[CHECK5 BOX4] Reçu heartbeat de BOX5")
        except socket.timeout:
            pass
        except Exception as e:
            print(f"[CHECK5 BOX4] Erreur: {e}")

def check_box5_alive():
    global last_heartbeat_box5
    while True:
        now = time.time()
        if last_heartbeat_box5 is None or (now - last_heartbeat_box5) > HEARTBEAT_TIMEOUT:
            print(f"[CHECK5 BOX4] ⚠️ BOX5 ne répond plus (dernier heartbeat à {last_heartbeat_box5})")
            # Ici tu peux décider de lancer le checkvie en backup
        time.sleep(5)

if __name__ == "__main__":
    import threading

    thread_check = threading.Thread(target=check_box5_alive, daemon=True)
    thread_check.start()
    listen_heartbeat_box5()
