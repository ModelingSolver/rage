import socket
import json
import time
import threading

HEARTBEAT_TIMEOUT = 20  # secondes avant de considérer une boîte morte
LISTEN_IP = "127.0.0.4"
LISTEN_PORT = 9998

# Dictionnaire pour stocker le dernier timestamp reçu par boîte
last_heartbeats = {

    "BOX5": None,
}

def check_boites_alive():
    while True:
        now = time.time()
        for boite, last_time in last_heartbeats.items():
            if last_time is None or (now - last_time) > HEARTBEAT_TIMEOUT:
                print(f"[CHECKVIE BOX4] ⚠️ {boite} ne répond plus (dernier heartbeat à {last_time})")
                # Action possible ici
        time.sleep(5)

def listen_heartbeats():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_IP, LISTEN_PORT))
    sock.settimeout(5)

    print(f"[CHECKVIE BOX4] Écoute les heartbeats sur {LISTEN_IP}:{LISTEN_PORT}")

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = json.loads(data.decode())
            boite = message.get("boite")
            if boite in last_heartbeats:
                last_heartbeats[boite] = time.time()
                print(f"[CHECKVIE BOX4] Reçu heartbeat de {boite}")
        except socket.timeout:
            pass  # Timeout pour permettre de checker les boîtes mortes
        except Exception as e:
            print(f"[CHECKVIE BOX4] Erreur: {e}")

if __name__ == "__main__":
    print("[CHECKVIE BOX4] Démarrage dans 10 secondes pour laisser démarrer les autres boîtes...")
    time.sleep(10)  # délai 10s, ajustable selon besoin

    thread_check = threading.Thread(target=check_boites_alive, daemon=True)
    thread_check.start()
    listen_heartbeats()
