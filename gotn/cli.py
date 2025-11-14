#!/usr/bin/env python3
import argparse
import os
import sys
import json
import requests
import websocket

API = "https://gophub.onrender.com"
CONFIG = os.path.expanduser("~/.gotnrc")

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

def auth_header():
    token = load_token()
    if not token:
        print("[gopuTN] ❌ Aucun token trouvé, fais 'gotn login' d'abord")
        sys.exit(1)
    return {"Authorization": f"Bearer {token}"}

def safe_print_response(res):
    print(f"[HTTP {res.status_code}]")
    try:
        print(json.dumps(res.json(), indent=2))
    except Exception:
        print("[gopuTN] ℹ️ Réponse brute du serveur:", res.text)

# ---------------------------
# Commandes CLI
# ---------------------------

def cmd_login(args):
    print("[gopuTN] ℹ️ Connexion à gopHub...")
    res = requests.post(API+"/login", json={"email": args.email, "password": args.password})
    safe_print_response(res)
    if res.ok and "token" in res.json():
        save_token(res.json()["token"])

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
    res = requests.get(f"{API}/search?q=@{args.scope}/")
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
        tags = args.tags or []
        print(f"[gopuTN] ℹ️ Publication du package '{pkg_name}:{version}' avec {len(files)} fichiers...")
        file_objs = [("files", open(f, "rb")) for f in files if os.path.exists(f)]
        res = requests.post(API+"/push",
            headers={"Authorization": f"Bearer {token}"},
            data={"name": pkg_name, "version": version, "tags": json.dumps(tags)},
            files=file_objs)
        safe_print_response(res)
    else:
        print("[gopuTN] ❌ gotn.json introuvable, fais 'gotn init' d'abord")

def cmd_init(args):
    config = {
        "name": args.name,
        "version": args.version,
        "files": args.files,
        "tags": args.tags
    }
    with open("gotn.json", "w") as f:
        json.dump(config, f, indent=2)
    print("[gopuTN] ✅ Fichier gotn.json créé")

def cmd_exec(args):
    res = requests.post(API+"/terminal",
                        headers=auth_header(),
                        json={"env": args.env, "command": args.command})
    safe_print_response(res)

def cmd_env_create(args):
    res = requests.post(API+"/env/create",
                        headers=auth_header(),
                        data={"name": args.name,
                              "version": args.version,
                              "description": args.description,
                              "tags": json.dumps(args.tags)})
    safe_print_response(res)

def cmd_update(args):
    res = requests.post(f"{API}/update/{args.name}/{args.version}",
                        headers=auth_header(),
                        json={"description": args.description, "tags": args.tags})
    safe_print_response(res)

def cmd_delete(args):
    res = requests.delete(f"{API}/delete/{args.name}/{args.version}",
                          headers=auth_header())
    safe_print_response(res)

def cmd_pull(args):
    res = requests.get(f"{API}/pull/{args.name}/{args.version}/{args.filename}",
                       headers=auth_header())
    if res.ok:
        with open(args.filename, "wb") as f:
            f.write(res.content)
        print(f"[gopuTN] ✅ Fichier téléchargé: {args.filename}")
    else:
        safe_print_response(res)

def cmd_shell(args):
    ws_url = API.replace("http", "ws") + "/terminal/ws"
    ws = websocket.WebSocket()
    ws.connect(ws_url)
    print(ws.recv())
    try:
        while True:
            cmd = input(f"{args.env}:{args.version}$ ")
            ws.send(cmd)
            print(ws.recv())
    except KeyboardInterrupt:
        ws.close()

# ---------------------------
# Main
# ---------------------------

def main():
    parser = argparse.ArgumentParser(prog="gotn", description="gopHub CLI 🚀")
    sub = parser.add_subparsers(dest="command")

    # login / register
    p_login = sub.add_parser("login"); p_login.add_argument("email"); p_login.add_argument("password"); p_login.set_defaults(func=cmd_login)
    p_register = sub.add_parser("register"); p_register.add_argument("email"); p_register.add_argument("password"); p_register.set_defaults(func=cmd_register)

    # list / search / readme / stats / assoc
    sub.add_parser("list").set_defaults(func=cmd_list)
    p_search = sub.add_parser("search"); p_search.add_argument("query"); p_search.set_defaults(func=cmd_search)
    p_readme = sub.add_parser("readme"); p_readme.add_argument("name"); p_readme.add_argument("version"); p_readme.set_defaults(func=cmd_readme)
    p_stats = sub.add_parser("stats"); p_stats.add_argument("name"); p_stats.add_argument("version"); p_stats.set_defaults(func=cmd_stats)
    p_assoc = sub.add_parser("assoc"); p_assoc.add_argument("scope"); p_assoc.set_defaults(func=cmd_assoc)

    # send / init
    p_send = sub.add_parser("send"); p_send.add_argument("--tags", nargs="+", default=[]); p_send.set_defaults(func=cmd_send)
    p_init = sub.add_parser("init"); p_init.add_argument("name"); p_init.add_argument("version"); p_init.add_argument("files", nargs="+"); p_init.add_argument("--tags", nargs="+", default=[]); p_init.set_defaults(func=cmd_init)

    # env / exec / shell
    p_env = sub.add_parser("env"); p_env.add_argument("name"); p_env.add_argument("version"); p_env.add_argument("--description", default=""); p_env.add_argument("--tags", nargs="+", default=[]); p_env.set_defaults(func=cmd_env_create)
    p_exec = sub.add_parser("exec"); p_exec.add_argument("env"); p_exec.add_argument("command"); p_exec.set_defaults(func=cmd_exec)
    p_shell = sub.add_parser("shell"); p_shell.add_argument("env"); p_shell.add_argument("version"); p_shell.set_defaults(func=cmd_shell)

    # update / delete / pull
    p_update = sub.add_parser("update"); p_update.add_argument("name"); p_update.add_argument("version"); p_update.add_argument("--description", default=""); p_update.add_argument("--tags", nargs="+", default=[]); p_update.set_defaults(func=cmd_update)
    p_delete = sub.add_parser("delete"); p_delete.add_argument("name"); p_delete.add_argument("version"); p_delete.set_defaults(func=cmd_delete)
    p_pull = sub.add_parser("pull"); p_pull.add_argument("name"); p_pull.add_argument("version"); p_pull.add_argument("filename");
    p_pull.set_defaults(func=cmd_pull)

    # Parse args et exécution
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
