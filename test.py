from flask import Flask, request
import hmac
import hashlib
import subprocess

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/version")
def version():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])

@app.route("/deploy", methods=['POST'])
def deploy():
    signature = request.headers.get('X-Hub-Signature')
    data = request.data
    if verify_hmac_hash(data, signature):
        if request.headers.get('X-GitHub-Event') == "push":
            payload = request.get_json()
            if payload['commits'][0]['distinct'] == True:
                try:
                    cmd_output = subprocess.check_output(
                        ['git', 'pull', 'origin', 'master'],)
                    return cmd_output
                except subprocess.CalledProcessError as error:
                    return error.output
    else:
        return "Invalid hash"

def verify_hmac_hash(data, signature):
    GitHub_secret = bytes('secret', 'UTF-8')
    mac = hmac.new(GitHub_secret, msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
