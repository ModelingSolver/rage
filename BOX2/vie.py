import socket
import time
import json
import platform

def send_heartbeat(ip="127.0.0.5", port=9999, nom_boite="BOX2"):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while True:
            message = {
                "boite": nom_boite,
                "etat": "OK",
                "time": time.time(),
                "systeme": platform.system()
            }
            sock.sendto(json.dumps(message).encode(), (ip, port))
            print(f"[VIE] Heartbeat envoyé par {nom_boite}")
            time.sleep(10)

if __name__ == "__main__":
    send_heartbeat(nom_boite="BOX2")
