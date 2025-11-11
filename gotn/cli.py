#!/usr/bin/env python3
import argparse, requests, json
from pathlib import Path

ROOT = Path.home() / ".gotn"
IMAGES = ROOT / "images"
CONTAINERS = ROOT / "containers"
ROOT.mkdir(exist_ok=True)
IMAGES.mkdir(exist_ok=True)
CONTAINERS.mkdir(exist_ok=True)

CACHE_FILE = Path("__gocache__")
RC_FILE = Path(".gotnrc")

SERVER = "https://gophub.onrender.com"

def info(msg): print(f"[gopuTN] ℹ️ {msg}")
def success(msg): print(f"[gopuTN] ✅ {msg}")
def error(msg): print(f"[gopuTN] ❌ {msg}")

def save_token(token):
    RC_FILE.write_text(json.dumps({"token": token}, indent=2))
    success("Token enregistré dans .gotnrc")

def load_token():
    if RC_FILE.exists():
        return json.loads(RC_FILE.read_text()).get("token")
    return None

# === Commandes ===
def login(email, password):
    info("Connexion à gopHub...")
    res = requests.post(f"{SERVER}/login", json={"email": email, "password": password})
    if res.status_code == 200:
        token = res.json()["token"]
        save_token(token)
    else:
        error(res.text)

def view():
    info("Liste des packages...")
    res = requests.get(f"{SERVER}/list")
    if res.status_code == 200:
        for pkg in res.json()["packages"]:
            print(f"- {pkg}")
    else:
        error(res.text)

def draw(name):
    info(f"Téléchargement du package '{name}'...")
    res = requests.get(f"{SERVER}/pull/{name}")
    if res.status_code == 200:
        pkg_dir = IMAGES / name
        pkg_dir.mkdir(exist_ok=True)
        (pkg_dir / "manifest.json").write_text(json.dumps(res.json(), indent=2))
        CACHE_FILE.write_text(f"Package {name} téléchargé\n")
        success(f"Package '{name}' stocké dans {pkg_dir}")
    else:
        error(res.text)

def send(name, file_path):
    info(f"Publication du package '{name}'...")
    token = load_token()
    if not token:
        error("Pas de token. Faites 'gotn login' d'abord.")
        return
    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {"name": name}
        headers = {"Authorization": f"Bearer {token}"}
        res = requests.post(f"{SERVER}/push", data=data, files=files, headers=headers)
    if res.status_code == 200:
        success(f"Package '{name}' publié")
    else:
        error(res.text)

# === CLI principal ===
def main():
    parser = argparse.ArgumentParser(prog="gotn", description="CLI pour gopuTN connecté à gopHub")
    subparsers = parser.add_subparsers(dest="command")

    login_parser = subparsers.add_parser("login")
    login_parser.add_argument("email")
    login_parser.add_argument("password")

    subparsers.add_parser("view")

    draw_parser = subparsers.add_parser("draw")
    draw_parser.add_argument("name")

    send_parser = subparsers.add_parser("send")
    send_parser.add_argument("name")
    send_parser.add_argument("file")

    args = parser.parse_args()
    if args.command == "login": login(args.email, args.password)
    elif args.command == "view": view()
    elif args.command == "draw": draw(args.name)
    elif args.command == "send": send(args.name, args.file)
    else: parser.print_help()

if __name__ == "__main__":
    main()
