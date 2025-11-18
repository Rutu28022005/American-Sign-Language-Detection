from flask import Flask, send_from_directory, jsonify
import subprocess, sys, os, time

# ---- PATHS ----
APP_DIR = os.path.dirname(os.path.abspath(__file__))        # Sign-Language-To-Text folder
PROJECT_ROOT = os.path.dirname(APP_DIR)                     # One folder above
FRONT_HTML = "front.html"
PY_SCRIPT = os.path.join(APP_DIR, "final_pred.py")
LOG_FILE = os.path.join(APP_DIR, "launch_log.txt")

# Alphabet folder is now at: SGP/Alphabet
ALPHABET_DIR = os.path.join(PROJECT_ROOT, "Alphabet")

app = Flask(__name__, static_folder=APP_DIR, static_url_path='/static')
launched_proc = None


# ---- ROUTES ----

@app.route('/')
def index():
    return send_from_directory(APP_DIR, FRONT_HTML)


@app.route('/launch', methods=['POST'])
def launch():
    global launched_proc

    if launched_proc and launched_proc.poll() is None:
        return jsonify(started=True)

    if not os.path.exists(PY_SCRIPT):
        return jsonify(started=False, error="final_pred.py not found"), 500

    try:
        with open(LOG_FILE, "a", buffering=1) as logf:
            logf.write(f"\n=== Launch requested at {time.ctime()} ===\n")

            if os.name == 'nt':
                CREATE_NEW_CONSOLE = 0x00000010
                launched_proc = subprocess.Popen(
                    [sys.executable, PY_SCRIPT],
                    creationflags=CREATE_NEW_CONSOLE,
                    cwd=APP_DIR,
                    stdout=logf, stderr=logf
                )
            else:
                launched_proc = subprocess.Popen(
                    [sys.executable, PY_SCRIPT],
                    cwd=APP_DIR,
                    stdout=logf, stderr=logf,
                    start_new_session=True
                )

        return jsonify(started=True)

    except Exception as e:
        return jsonify(started=False, error=str(e)), 500


@app.route('/status', methods=['GET'])
def status():
    running = launched_proc is not None and launched_proc.poll() is None
    return jsonify(running=running)


# ---- SERVE ALPHABET IMAGES ----
@app.route('/alphabet/<path:filename>')
def alphabet_files(filename):
    return send_from_directory(ALPHABET_DIR, filename)


# ---- STATIC FILES (CSS, JS, etc.) ----
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(APP_DIR, filename)


if __name__ == '__main__':# No filepath, shell command only
    print("Server running at http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
