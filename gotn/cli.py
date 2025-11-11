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

def safe_print_response(res):
    try:
        print(res.json())
    except ValueError:
        print("[gopuTN] ℹ️ Réponse brute du serveur:", res.text)

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
    safe_print_response(res)

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
        safe_print_response(res)

def cmd_send(args):
    token = load_token()
    if not token:
        print("[gopuTN] ❌ Aucun token trouvé, fais 'gotn login' d'abord")
        return

    if os.path.exists("gotn.json"):
        with open("gotn.json") as f:
            config = json.load(f)
        pkg_name = config["name"]
        version = config["version"]
        files = config["files"]
        print(f"[gopuTN] ℹ️ Publication du package '{pkg_name}:{version}' avec {len(files)} fichiers...")
        for file in files:
            if not os.path.exists(file):
                print(f"[gopuTN] ❌ Fichier introuvable: {file}")
                continue
            with open(file, "rb") as fobj:
                res = requests.post(API+"/push",
                    headers={"Authorization": f"Bearer {token}"},
                    files={"files": fobj},
                    data={"name": pkg_name, "version": version, "path": file})
                safe_print_response(res)
    else:
        print(f"[gopuTN] ℹ️ Publication du package '{args.package}'...")
        with open(args.file, "rb") as f:
            res = requests.post(API+"/push",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": f},
                data={"name": args.package})
        safe_print_response(res)

def cmd_lest(args):
    pkg = args.package
    path = os.path.join(IMAGES_DIR, pkg, f"{pkg}.pkg")
    if not os.path.exists(path):
        print(f"[gopuTN] ❌ Package '{pkg}' introuvable, fais 'gotn draw {pkg}' d'abord")
        return
    print(f"[gopuTN] ℹ️ Exécution du package '{pkg}'...")
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

def cmd_let(args):
    """Exécute un manifest JSON généré par const"""
    infile = args.file
    manifest = infile.replace(".gopuTN", ".json")
    if not os.path.exists(manifest):
        print("[gopuTN] ❌ Manifest introuvable, fais 'gotn const' d'abord")
        return

    with open(manifest) as f:
        data = json.load(f)

    print("[gopuTN] ℹ️ Exécution du manifest...")
    for entry in data["commands"]:
        cmd = entry["cmd"]
        arg = entry["arg"]
        print(f" → {cmd} {arg}")
        if cmd == "DO":
            os.system(arg)
        elif cmd == "NET":
            print(f"[gopuTN] 🌐 Port exposé: {arg}")
        elif cmd == "REC":
            if arg.startswith("gotn:"):
                env_name = arg.split(":")[1]
                version = arg.split(":")[2] if len(arg.split(":")) > 2 else "latest"
                print(f"[gopuTN] 📦 Environnement gopHub: {env_name}:{version}")
                res = requests.get(f"{API}/pull/{env_name}-{version}")
                if res.ok:
                    env_path = os.path.join(IMAGES_DIR, f"{env_name}-{version}")
                    ensure_dir(env_path)
                    with open(os.path.join(env_path, f"{env_name}.env"), "wb") as f:
                        f.write(res.content)
                    print(f"[gopuTN] ✅ Environnement {env_name}:{version} installé")
                else:
                    safe_print_response(res)
            else:
                print(f"[gopuTN] 📦 Base image: {arg}")
        elif cmd == "LOC":
            print(f"[gopuTN] 📂 Workdir: {arg}")
        elif cmd == "BY":
            print(f"[gopuTN] 📥 Copie: {arg}")
        elif cmd == "GO":
            os.system(" ".join(json.loads(arg)))

def cmd_init(args):
    """Crée un fichier gotn.json listant les fichiers à publier"""
    config = {
        "name": args.name,
        "version": args.version,
        "files": args.files
    }
    with open("gotn.json", "w") as f:
        json.dump(config, f, indent=2)
    print("[gopuTN] ✅ Fichier gotn.json créé")

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
    p_send.add_argument("package", nargs="?")
    p_send.add_argument("file", nargs="?")
    p_send.set_defaults(func=cmd_send)

    # lest
    p_lest = subparsers.add_parser("lest")
    p_lest.add_argument("package")
    p_lest.set_defaults(func=cmd_lest)

    # const
    p_const = subparsers.add_parser("const")
    p_const.add_argument("file")
    p_const.set_defaults(func=cmd_const)

    # let
    p_let = subparsers.add_parser("let")
    p_let.add_argument("file")
    p_let.set_defaults(func=cmd_let)

    # init
    p_init = subparsers.add_parser("init")
    p_init.add_argument("name")
    p_init.add_argument("version")
    p_init.add_argument("files", nargs="+")
    p_init.set_defaults(func=cmd_init)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
