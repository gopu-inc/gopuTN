#!/usr/bin/env python3
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

def cmd_register(args):
    print("[gopuTN] ℹ️ Création de compte...")
    res = requests.post(API+"/register", json={"email": args.email, "password": args.password})
    safe_print_response(res)

def cmd_list(args):
    res = requests.get(API+"/list")
    safe_print_response(res)

def cmd_search(args):
    res = requests.get(f"{API}/search?q={args.query}")
    safe_print_response(res)

def cmd_readme(args):
    res = requests.get(f"{API}/readme/{args.name}/{args.version}")
    if res.ok:
        print(res.text)
    else:
        safe_print_response(res)

def cmd_stats(args):
    res = requests.get(f"{API}/stats/{args.name}/{args.version}")
    safe_print_response(res)

def cmd_assoc(args):
    scope = args.scope
    res = requests.get(f"{API}/search?q=@{scope}/")
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
        tags = getattr(args, "tags", "[]")
        print(f"[gopuTN] ℹ️ Publication du package '{pkg_name}:{version}' avec {len(files)} fichiers...")
        file_objs = [("files", open(f, "rb")) for f in files if os.path.exists(f)]
        res = requests.post(API+"/push",
            headers={"Authorization": f"Bearer {token}"},
            data={"name": pkg_name, "version": version, "tags": tags},
            files=file_objs)
        safe_print_response(res)
    else:
        print("[gopuTN] ❌ gotn.json introuvable, fais 'gotn init' d'abord")

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
            print(f"[gopuTN] 📦 Environnement requis: {arg}")
        elif cmd == "LOC":
            print(f"[gopuTN] 📂 Workdir: {arg}")
        elif cmd == "BY":
            print(f"[gopuTN] 📥 Copie: {arg}")
        elif cmd == "GO":
            os.system(" ".join(json.loads(arg)))

# ---------------------------
# Main
# ---------------------------

def main():
    parser = argparse.ArgumentParser(prog="gotn", description="gopHub CLI 🚀")
    subparsers = parser.add_subparsers(dest="command")

    # login
    p_login = subparsers.add_parser("login", help="Connexion à gopHub")
    p_login.add_argument("email")
    p_login.add_argument("password")
    p_login.set_defaults(func=cmd_login)

    # register
    p_register = subparsers.add_parser("register", help="Créer un compte utilisateur")
    p_register.add_argument("email")
    p_register.add_argument("password")
    p_register.set_defaults(func=cmd_register)

    # list
    p_list = subparsers.add_parser("list", help="Liste tous les packages")
    p_list.set_defaults(func=cmd_list)

    # search
    p_search = subparsers.add_parser("search", help="Recherche par mot-clé ou tag")
    p_search.add_argument("query")
    p_search.set_defaults(func=cmd_search)

    # readme
    p_readme = subparsers.add_parser("readme", help="Affiche le README d’un package")
    p_readme.add_argument("name")
    p_readme.add_argument("version")
    p_readme.set_defaults(func=cmd_readme)

    # stats
    p_stats = subparsers.add_parser("stats", help="Affiche les stats d’un package")
    p_stats.add_argument("name")
    p_stats.add_argument("version")
    p_stats.set_defaults(func=cmd_stats)

    # assoc
    p_assoc = subparsers.add_parser("assoc", help="Liste les packages d’une association (@scope/*)")
    p_assoc.add_argument("scope")
    p_assoc.set_defaults(func=cmd_assoc)

    # send
    p_send = subparsers.add_parser("send", help="Publie un package")
    p_send.add_argument("--tags", help="Tags du package (JSON ou liste séparée par des virgules)", default="[]")
    p_send.set_defaults(func=cmd_send)

    # init
    p_init = subparsers.add_parser("init", help="Crée un fichier gotn.json")
    p_init.add_argument("--tags", nargs="+", help="Tags du package", default=[])
    p_init.add_argument("name")
    p_init.add_argument("version")
    p_init.add_argument("files", nargs="+")
    p_init.set_defaults(func=cmd_init)

    # const
    p_const = subparsers.add_parser("const", help="Transpile un fichier .gopuTN en manifest JSON")
    p_const.add_argument("file")
    p_const.set_defaults(func=cmd_const)

    # let
    p_let = subparsers.add_parser("let", help="Exécute un manifest JSON généré par const")
    p_let.add_argument("file")
    p_let.set_defaults(func=cmd_let)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
