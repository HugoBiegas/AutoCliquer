#!/usr/bin/env python3
"""
Auto-Clicker - Application de clic automatique avec interface moderne
"""

import sys
import os
import socket
import threading

# Ajouter le chemin src au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Port pour la communication single-instance
SINGLE_INSTANCE_PORT = 47891


def is_already_running():
    """Verifie si une instance est deja en cours d'execution"""
    try:
        # Essayer de se connecter a une instance existante
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(1)
        client.connect(("127.0.0.1", SINGLE_INSTANCE_PORT))
        client.send(b"SHOW")
        client.close()
        return True
    except (socket.error, socket.timeout):
        return False


def start_instance_server(app):
    """Demarre le serveur qui ecoute les demandes d'autres instances"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(("127.0.0.1", SINGLE_INSTANCE_PORT))
        server.listen(1)
        server.settimeout(1)

        def listen_loop():
            while True:
                try:
                    client, _ = server.accept()
                    data = client.recv(1024)
                    if data == b"SHOW":
                        # Ramener la fenetre au premier plan
                        app.after(0, bring_to_front, app)
                    client.close()
                except socket.timeout:
                    continue
                except OSError:
                    break

        thread = threading.Thread(target=listen_loop, daemon=True)
        thread.start()
        return server
    except OSError:
        return None


def bring_to_front(app):
    """Ramene l'application au premier plan"""
    app.deiconify()  # Restaurer si minimise
    app.lift()  # Mettre au premier plan
    app.focus_force()  # Forcer le focus
    # Sur Windows, utiliser des methodes supplementaires
    try:
        app.state('normal')
        app.attributes('-topmost', True)
        app.after(100, lambda: app.attributes('-topmost', False))
    except Exception:
        pass


def main():
    # Verifier si une instance existe deja
    if is_already_running():
        # Une instance existe, on a envoye le signal SHOW, on quitte
        sys.exit(0)

    from src.ui.app import App
    app = App()

    # Demarrer le serveur single-instance
    server = start_instance_server(app)

    # Lancer l'application
    app.mainloop()

    # Fermer le serveur proprement
    if server:
        server.close()


if __name__ == "__main__":
    main()
