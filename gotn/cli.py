import argparse
import os
import sys
import json
import requests

API = "https://gophub.onrender.com"
CONFIG = os.path.expanduser("~/.gotnrc")
IMAGES_DIR = os.path.expanduser("~/.gotn/images")

# ---------------------------
# Utilitaires
# ---------------------------

def save_token(token):
    os.makedirs(os.path.dirname(CONFIG), exist_ok=True)
    with open(CONFIG, "w") as f:
        json.dump({"token": token}, f)
    print("[gopuTN] ✅ Token enregistré dans .gotnrc")

def load_token():
    if os.path.exists(CONFIG):
        with open(CONFIG) as f:
            return json.load(f).get("token")
    return None

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

# ---------------------------
# Commandes CLI
# ---------------------------

def cmd_login(args):
    print("[gopuTN] ℹ️ Connexion à gopHub...")
    res = requests.post(API+"/login", json={"email": args.email, "password": args.password})
    data = res.json()
    if "token" in data:
        save_token(data["token"])
    else:
        print("[gopuTN] ❌ Erreur de connexion:", data)

def cmd_view(args):
    res = requests.get(API+"/list")
    data = res.json()
    print("[gopuTN] 📦 Packages disponibles:")
    for p in data.get("packages", []):
        print(" -", p)

def cmd_draw(args):
    pkg = args.package
    print(f"[gopuTN] ℹ️ Téléchargement du package '{pkg}'...")
    res = requests.get(f"{API}/pull/{pkg}")
    if res.ok:
        path = os.path.join(IMAGES_DIR, pkg)
        ensure_dir(path)
        pkg_file = os.path.join(path, f"{pkg}.pkg")
        with open(pkg_file, "wb") as f:
            f.write(res.content)
        print(f"[gopuTN] ✅ Package '{pkg}' stocké dans {path}")
    else:
        print("[gopuTN] ❌ Erreur:", res.text)

def cmd_send(args):
    token = load_token()
    if not token:
        print("[gopuTN] ❌ Aucun token trouvé, fais 'gotn login' d'abord")
        return
    print(f"[gopuTN] ℹ️ Publication du package '{args.package}'...")
    with open(args.file, "rb") as f:
        res = requests.post(API+"/push",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": f},
            data={"name": args.package})
    print(res.json())

def cmd_lest(args):
    pkg = args.package
    path = os.path.join(IMAGES_DIR, pkg, f"{pkg}.pkg")
    if not os.path.exists(path):
        print(f"[gopuTN] ❌ Package '{pkg}' introuvable, fais 'gotn draw {pkg}' d'abord")
        return
    print(f"[gopuTN] ℹ️ Exécution du package '{pkg}'...")
    # Ici tu peux définir comment exécuter ton package
    # Exemple: si c’est du JS
    os.system(f"node {path}")

def cmd_const(args):
    """Transpile un fichier *.gopuTN en manifest JSON"""
    infile = args.file
    if not os.path.exists(infile):
        print("[gopuTN] ❌ Fichier introuvable:", infile)
        return

    manifest = {"commands": []}
    with open(infile) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(maxsplit=1)
            cmd = parts[0].upper()
            arg = parts[1] if len(parts) > 1 else ""
            manifest["commands"].append({"cmd": cmd, "arg": arg})

    out = infile.replace(".gopuTN", ".json")
    with open(out, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"[gopuTN] ✅ Manifest généré: {out}")

# ---------------------------
# Main
# ---------------------------

def main():
    parser = argparse.ArgumentParser(prog="gotn")
    subparsers = parser.add_subparsers(dest="command")

    # login
    p_login = subparsers.add_parser("login")
    p_login.add_argument("email")
    p_login.add_argument("password")
    p_login.set_defaults(func=cmd_login)

    # view
    p_view = subparsers.add_parser("view")
    p_view.set_defaults(func=cmd_view)

    # draw
    p_draw = subparsers.add_parser("draw")
    p_draw.add_argument("package")
    p_draw.set_defaults(func=cmd_draw)

    # send
    p_send = subparsers.add_parser("send")
    p_send.add_argument("package")
    p_send.add_argument("file")
    p_send.set_defaults(func=cmd_send)

    # lest
    p_lest = subparsers.add_parser("lest")
    p_lest.add_argument("package")
    p_lest.set_defaults(func=cmd_lest)

    # const (transpile *.gopuTN)
    p_const = subparsers.add_parser("const")
    p_const.add_argument("file")
    p_const.set_defaults(func=cmd_const)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
