from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/version")
def version():
    import subprocess
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])

if __name__ == "__main__":
    app.run()
