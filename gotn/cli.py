#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

# === Logger simplifié ===
def info(msg): print(f"[gopuTN] ℹ️ {msg}")
def success(msg): print(f"[gopuTN] ✅ {msg}")
def error(msg): print(f"[gopuTN] ❌ {msg}")

# === Transpileur minimal gopuTN → Dockerfile ===
mapping = {
    "REC": "FROM", "DO": "RUN", "BY": "COPY", "PUT": "ADD",
    "LOC": "WORKDIR", "SET": "ENV", "ASK": "ARG", "SPA": "EXPOSE",
    "GO": "CMD", "IN": "ENTRYPOINT", "BOX": "VOLUME", "WHO": "USER",
    "TAG": "LABEL", "TRIG": "ONBUILD", "SHL": "SHELL", "SIG": "STOPSIGNAL",
    "MED": "HEALTHCHECK", "LIB": "RUN apt-get install -y",
    "SEC": "USER", "NET": "EXPOSE", "LOG": "# LOG"
}

def transpile(path):
    lines = Path(path).read_text().splitlines()
    docker_lines = []
    for line in lines:
        parts = line.strip().split(" ", 1)
        if not parts or not parts[0]:
            continue
        keyword = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        docker_keyword = mapping.get(keyword, keyword)
        docker_lines.append(f"{docker_keyword} {args}")
    return "\n".join(docker_lines)

# === Commandes gopuTN ===
def const(path, tag):
    info(f"Construction (const) de '{tag}'...")
    dockerfile = transpile(path)
    Path("Dockerfile").write_text(dockerfile)
    result = subprocess.run(["docker", "build", "-t", tag, "."], capture_output=True, text=True)
    if result.returncode == 0:
        success(f"const terminé → image: {tag}")
    else:
        error(f"Erreur const:\n{result.stderr}")

def lest(image):
    info(f"Exécution (lest) de '{image}'...")
    result = subprocess.run(["docker", "run", image], capture_output=True, text=True)
    if result.returncode == 0:
        success("lest terminé")
    else:
        error(f"Erreur lest:\n{result.stderr}")

def flow(path):
    info("Transpilation (flow)...")
    print(transpile(path))

def rise():
    print("""
    ╔══════════════════════════════════╗
    ║   gopuTN :: sovereign CLI boost  ║
    ║   Commands: const, lest, flow... ║
    ╚══════════════════════════════════╝
    """)

def send(tag):
    info(f"Push (send) de '{tag}' vers registry...")
    subprocess.run(["docker", "push", tag])

def draw(tag):
    info(f"Pull (draw) de '{tag}' depuis registry...")
    subprocess.run(["docker", "pull", tag])

def halt(container):
    info(f"Arrêt (halt) du conteneur '{container}'...")
    subprocess.run(["docker", "stop", container])

def view():
    info("Liste des images (view)...")
    subprocess.run(["docker", "images"])

def cast(container, cmd):
    info(f"Exécution (cast) dans '{container}'...")
    subprocess.run(["docker", "exec", container] + cmd)

def drop(container):
    info(f"Suppression (drop) du conteneur '{container}'...")
    subprocess.run(["docker", "rm", container])

# === CLI principal ===
def main():
    parser = argparse.ArgumentParser(prog="gotn", description="CLI pour gopuTN boosté")
    subparsers = parser.add_subparsers(dest="command")

    const_parser = subparsers.add_parser("const")
    const_parser.add_argument("path")
    const_parser.add_argument("-t", "--tag", default="gotn-image")

    lest_parser = subparsers.add_parser("lest")
    lest_parser.add_argument("image")

    flow_parser = subparsers.add_parser("flow")
    flow_parser.add_argument("path")

    subparsers.add_parser("rise")

    send_parser = subparsers.add_parser("send")
    send_parser.add_argument("tag")

    draw_parser = subparsers.add_parser("draw")
    draw_parser.add_argument("tag")

    halt_parser = subparsers.add_parser("halt")
    halt_parser.add_argument("container")

    subparsers.add_parser("view")

    cast_parser = subparsers.add_parser("cast")
    cast_parser.add_argument("container")
    cast_parser.add_argument("cmd", nargs=argparse.REMAINDER)

    drop_parser = subparsers.add_parser("drop")
    drop_parser.add_argument("container")

    args = parser.parse_args()
    if args.command == "const": const(args.path, args.tag)
    elif args.command == "lest": lest(args.image)
    elif args.command == "flow": flow(args.path)
    elif args.command == "rise": rise()
    elif args.command == "send": send(args.tag)
    elif args.command == "draw": draw(args.tag)
    elif args.command == "halt": halt(args.container)
    elif args.command == "view": view()
    elif args.command == "cast": cast(args.container, args.cmd)
    elif args.command == "drop": drop(args.container)
    else: parser.print_help()

if __name__ == "__main__":
    main()
