import os
import json
import pytest
import types

import gotn.cli as cli

class DummyResponse:
    def __init__(self, status_code=200, json_data=None, text="OK"):
        self.status_code = status_code
        self._json = json_data or {}
        self.text = text
        self.ok = status_code == 200
    def json(self):
        return self._json

# ---------------------------
# Tests simples
# ---------------------------

def test_cmd_version_current(monkeypatch, capsys):
    def fake_get(url, timeout=5):
        return DummyResponse(json_data={
            "info": {"version": "1.2.3"},
            "releases": {"1.0.0": {}, "1.2.3": {}}
        })
    monkeypatch.setattr(cli.requests, "get", fake_get)
    args = types.SimpleNamespace(pear=False)
    cli.cmd_version(args)
    out = capsys.readouterr().out
    assert "1.2.3" in out

def test_cmd_version_previous(monkeypatch, capsys):
    def fake_get(url, timeout=5):
        return DummyResponse(json_data={
            "info": {"version": "2.0.0"},
            "releases": {"1.0.0": {}, "2.0.0": {}}
        })
    monkeypatch.setattr(cli.requests, "get", fake_get)
    args = types.SimpleNamespace(pear=True)
    cli.cmd_version(args)
    out = capsys.readouterr().out
    assert "1.0.0" in out

def test_save_and_load_token(tmp_path):
    cfg = tmp_path / ".gotnrc"
    cli.CONFIG = str(cfg)
    cli.save_token("abc123")
    token = cli.load_token()
    assert token == "abc123"

def test_auth_header(monkeypatch):
    cli.CONFIG = "tmp_token.json"
    with open(cli.CONFIG, "w") as f:
        json.dump({"token": "xyz"}, f)
    headers = cli.auth_header()
    assert headers["Authorization"] == "Bearer xyz"

def test_cmd_login(monkeypatch, capsys):
    def fake_post(url, json=None):
        return DummyResponse(json_data={"token": "tok123"})
    monkeypatch.setattr(cli.requests, "post", fake_post)
    args = types.SimpleNamespace(email="a@b.c", password="pw")
    cli.CONFIG = "tmp_token.json"
    cli.cmd_login(args)
    out = capsys.readouterr().out
    assert "Connexion" in out

def test_cmd_init(tmp_path, capsys):
    os.chdir(tmp_path)
    args = types.SimpleNamespace(name="pkg", version="0.1", files=["a.py"], tags=["demo"])
    cli.cmd_init(args)
    assert os.path.exists("gotn.json")
    out = capsys.readouterr().out
    assert "gotn.json" in out

def test_cmd_const_and_let(tmp_path, capsys):
    gopu_file = tmp_path / "demo.gopuTN"
    gopu_file.write_text("CREATE ENV:demo\nDO echo hello")
    args = types.SimpleNamespace(file=str(gopu_file))
    cli.cmd_const(args)
    out = capsys.readouterr().out
    assert "Manifest généré" in out

    # Exécution du manifest
    args2 = types.SimpleNamespace(file=str(gopu_file))
    cli.cmd_let(args2)
    out2 = capsys.readouterr().out
    assert "Création d'environnement" in out2
