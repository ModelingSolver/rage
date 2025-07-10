import socket
import time
import json
import platform

def send_heartbeat_to_box4(ip="127.0.0.4", port=9998, nom_boite="BOX5"):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while True:
            message = {
                "boite": nom_boite,
                "etat": "OK",
                "time": time.time(),
                "systeme": platform.system()
            }
            sock.sendto(json.dumps(message).encode(), (ip, port))
            print(f"[SURVIE] Heartbeat envoyé par {nom_boite} à BOX4")
            time.sleep(5)  # heartbeat toutes les 5 secondes

if __name__ == "__main__":
    send_heartbeat_to_box4()
