#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

# === Fonctions principales ===

def const(path, tag):
    """Construire une image à partir d’un fichier gopuTN"""
    print(f"[gopuTN] 🔨 Construction (const) de '{tag}'...")
    # Ici on transpile gopuTN → Dockerfile
    lines = Path(path).read_text().splitlines()
    dockerfile = []
    mapping = {
        "REC": "FROM", "DO": "RUN", "BY": "COPY", "PUT": "ADD",
        "LOC": "WORKDIR", "SET": "ENV", "ASK": "ARG", "SPA": "EXPOSE",
        "GO": "CMD", "IN": "ENTRYPOINT", "BOX": "VOLUME", "WHO": "USER",
        "TAG": "LABEL", "TRIG": "ONBUILD", "SHL": "SHELL", "SIG": "STOPSIGNAL",
        "MED": "HEALTHCHECK"
    }
    for line in lines:
        parts = line.strip().split(" ", 1)
        if not parts or not parts[0]:
            continue
        keyword = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        docker_keyword = mapping.get(keyword, keyword)
        dockerfile.append(f"{docker_keyword} {args}")
    Path("Dockerfile").write_text("\n".join(dockerfile))

    result = subprocess.run(
        ["docker", "build", "-t", tag, "."],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"[gopuTN] ✅ const terminé → image: {tag}")
    else:
        print(f"[gopuTN] ❌ Erreur const:\n{result.stderr}")

def lest(image):
    """Exécuter une image"""
    print(f"[gopuTN] ▶️ Exécution (lest) de '{image}'...")
    result = subprocess.run(
        ["docker", "run", image],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"[gopuTN] ✅ lest terminé")
    else:
        print(f"[gopuTN] ❌ Erreur lest:\n{result.stderr}")

def flow(path):
    """Transpiler un fichier gopuTN en Dockerfile"""
    print(f"[gopuTN] 🔄 Transpilation (flow)...")
    lines = Path(path).read_text().splitlines()
    mapping = {
        "REC": "FROM", "DO": "RUN", "BY": "COPY", "PUT": "ADD",
        "LOC": "WORKDIR", "SET": "ENV", "ASK": "ARG", "SPA": "EXPOSE",
        "GO": "CMD", "IN": "ENTRYPOINT", "BOX": "VOLUME", "WHO": "USER",
        "TAG": "LABEL", "TRIG": "ONBUILD", "SHL": "SHELL", "SIG": "STOPSIGNAL",
        "MED": "HEALTHCHECK"
    }
    dockerfile = []
    for line in lines:
        parts = line.strip().split(" ", 1)
        if not parts or not parts[0]:
            continue
        keyword = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        docker_keyword = mapping.get(keyword, keyword)
        dockerfile.append(f"{docker_keyword} {args}")
    print("\n".join(dockerfile))

def rise():
    """Intro stylisée"""
    print("""
    ╔══════════════════════════════╗
    ║   gopuTN :: sovereign CLI    ║
    ║   Commands: const, lest, flow║
    ║   Simplified syntax engine   ║
    ╚══════════════════════════════╝
    """)

# === CLI principal ===

def main():
    parser = argparse.ArgumentParser(prog="gotn", description="CLI pour gopuTN")
    subparsers = parser.add_subparsers(dest="command")

    const_parser = subparsers.add_parser("const")
    const_parser.add_argument("path", help="Chemin du fichier .gopuTN")
    const_parser.add_argument("-t", "--tag", default="gotn-image", help="Nom de l'image")

    lest_parser = subparsers.add_parser("lest")
    lest_parser.add_argument("image", help="Nom de l'image à exécuter")

    flow_parser = subparsers.add_parser("flow")
    flow_parser.add_argument("path", help="Chemin du fichier .gopuTN")

    subparsers.add_parser("rise")

    args = parser.parse_args()

    if args.command == "const":
        const(args.path, args.tag)
    elif args.command == "lest":
        lest(args.image)
    elif args.command == "flow":
        flow(args.path)
    elif args.command == "rise":
        rise()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

