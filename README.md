# Lab Status — DevOps Lab 1

A tiny Python web service for practicing Git, local testing, branches, and pull
requests. This is the application we will later containerize and deploy through
GitHub Actions, a self-hosted runner, Kubernetes, and Jenkins.

## Prerequisites

- Linux shell (commands below assume Bash).
- Python 3.10 or newer, Git, and a GitHub account.
- `curl` for optional HTTP checks; `unzip` to extract the download.

No external Python packages are needed. We use Python's standard-library WSGI
server and unittest so setup does not distract from the Git workflow. The server
is for learning; a later deployment lab can use a production WSGI server.

## Start here

From the directory containing the ZIP:

```bash
unzip lab-status-lab1.zip
cd lab-status
python3 --version
git --version
python3 -m unittest discover -s tests -v
python3 app.py
```

The test run should report **9 tests**, then **OK**. The last command starts the
server and occupies your terminal. Open http://127.0.0.1:8000 or use a second
terminal:

```bash
curl -i http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/version
```

Stop the server with Ctrl+C. If it runs on a VM, localhost means the VM itself.
To access it from another machine on your trusted lab network, start it with
`HOST=0.0.0.0 python3 app.py`, then visit `http://VM_IP:8000`. Allow TCP 8000
through the VM firewall only from your lab network if necessary.

**Next: follow [the Lab 1 walkthrough](docs/LAB_1.md).**

## Files

| File | Purpose |
| --- | --- |
| `app.py` | Application routes and local web server |
| `tests/test_app.py` | Endpoint and configuration behavior tests |
| `.gitignore` | Keeps generated files and local secrets out of commits |
| `requirements.txt` | Documents that Lab 1 has no third-party dependencies |
| `docs/LAB_1.md` | Initialize Git, push, branch, test, open a PR, merge |
| `docs/LEARNING_NOTES.md` | Record observations and troubleshooting |

## HTTP endpoints

| Path | Response |
| --- | --- |
| `/` | HTML page with a message and application version |
| `/health` | JSON: `{"status": "ok"}`; checks that the app can respond |
| `/version` | JSON with application version and supplied Git commit |

Only GET and HEAD are supported. Unknown routes return 404; other methods return
405. Health does not yet check external dependencies because there are none.

## Configuration

| Environment variable | Default | Purpose |
| --- | --- | --- |
| `HOST` | `127.0.0.1` | Local server bind address |
| `PORT` | `8000` | Local server port |
| `APP_MESSAGE` | `Hello from my home lab!` | Text shown on the homepage |
| `GIT_COMMIT` | `unknown` | Build/source identity exposed by `/version` |

After your first Git commit, try:

```bash
APP_MESSAGE="John's infrastructure lab" GIT_COMMIT="$(git rev-parse --short HEAD)" python3 app.py
```

The app does not invoke Git itself. A later build pipeline will supply the source
commit. Restart the server after source edits; there is no automatic reload.

## Scope

This ZIP contains source files, not an existing Git repository. You create the
history yourself. Dockerfiles, workflow YAML, and Kubernetes manifests will be
added in later labs. Passing tests here is a manual check; no automated merge
gate or CI job has been configured yet.
