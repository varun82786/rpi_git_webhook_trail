from flask import Flask, request, abort
import git
import os
import subprocess

app = Flask(__name__)

REPO_DIR = "/path/to/your/repo"  # Set your repo path here
BRANCH_NAME = "master"  # Set the branch name you want to track
SECRET_TOKEN = "kalki82786"  # Set your secret token from GitHub Webhook settings

@app.route("/webhook", methods=["POST"])
def webhook():
    # Verify that the request is from GitHub using the secret token
    if request.headers.get("X-Hub-Signature") is None:
        abort(403)
    
    payload = request.json
    if "ref" in payload and payload["ref"] == f"refs/heads/{BRANCH_NAME}":
        # Git pull when the specified branch is updated
        repo = git.Repo(REPO_DIR)
        origin = repo.remotes.origin
        origin.pull()

        # Restart the Flask app (or trigger some action)
        restart_flask()

        return "Updated the code and restarted the app!", 200
    else:
        return "No updates made.", 200

def restart_flask():
    """Restart the Flask app using system command."""
    # Assuming you are running the app using nohup or another background process
    # Kill any running Flask instances
    subprocess.run(["pkill", "-f", "flask"])

    # Start Flask again (you may need to adjust the command based on your app)
    subprocess.run(["nohup", "flask", "run", "--host=0.0.0.0", "--port=5000", "&"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
