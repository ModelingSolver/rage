
import socket
import time
import json
import platform
import psutil

def send_heartbeat(ip="127.0.0.5", port=9999, nom_boite="BOX3", interval=10):
    print(f"[INIT] {nom_boite} démarrée. Envoi des heartbeats toutes les {interval} secondes.")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while True:
            try:
                # Vérification de la charge CPU de ce processus
                cpu_load = psutil.Process().cpu_percent(interval=None)
                if cpu_load > 80:
                    print(f"[WARN] CPU élevé ({cpu_load}%). Pause d'urgence.")
                    time.sleep(1)  # Délai pour calmer le jeu

                message = {
                    "boite": nom_boite,
                    "etat": "OK",
                    "time": time.time(),
                    "systeme": platform.system()
                }

                sock.sendto(json.dumps(message).encode(), (ip, port))
                print(f"[VIE] {nom_boite} OK à {time.strftime('%H:%M:%S')}")

                time.sleep(interval)

            except Exception as e:
                print(f"[ERREUR] {e}")
                time.sleep(5)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--nom", default="BOX3", help="Nom de la boîte")
    parser.add_argument("--ip", default="127.0.0.5", help="Adresse IP cible")
    parser.add_argument("--port", type=int, default=9999, help="Port UDP cible")
    parser.add_argument("--interval", type=int, default=10, help="Intervalle entre les heartbeats (secondes)")
    args = parser.parse_args()

    send_heartbeat(ip=args.ip, port=args.port, nom_boite=args.nom, interval=args.interval)
