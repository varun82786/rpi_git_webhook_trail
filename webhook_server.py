from flask import Flask, request, abort
import git
import os
import subprocess
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

REPO_DIR = "/home/rpiserver/projects/hashtag_webapp"  # Set your repo path here
BRANCH_NAME = "master"  # Set the branch name you want to track
SECRET_TOKEN = "kalki82786"  # Set your secret token from GitHub Webhook settings

@app.route("/webhook", methods=["POST"])
def webhook():
    logging.debug("Received webhook request.")
    
    # Verify that the request is from GitHub using the secret token
    signature = request.headers.get("X-Hub-Signature")
    if signature is None:
        logging.debug("No signature found in headers. Aborting request.")
        abort(403)
    
    payload = request.json
    logging.debug(f"Payload received: {payload}")
    
    if "ref" in payload and payload["ref"] == f"refs/heads/{BRANCH_NAME}":
        logging.debug(f"Branch {BRANCH_NAME} was updated. Pulling changes...")
        
        try:
            repo = git.Repo(REPO_DIR)
            origin = repo.remotes.origin
            origin.pull()
            logging.debug(f"Successfully pulled latest changes from {BRANCH_NAME}.")
        except Exception as e:
            logging.error(f"Error while pulling the repo: {e}")
            return f"Error pulling repo: {e}", 500

        # Restart the Flask app (or trigger some action)
        logging.debug("Restarting the Flask app.")
        restart_flask()

        return "Updated the code and restarted the app!", 200
    else:
        logging.debug(f"No relevant branch update (expected: {BRANCH_NAME}).")
        return "No updates made.", 200

def restart_flask():
    """Restart the Flask app using system command."""
    logging.debug("Restarting Flask process.")
    
    # Kill any running Flask instances
    try:
        subprocess.run(["pkill", "-f", "flask"])
        logging.debug("Killed existing Flask instances.")
    except Exception as e:
        logging.error(f"Error while killing Flask instances: {e}")

    # Start Flask again
    try:
        subprocess.run(["nohup", "flask", "run", "--host=0.0.0.0", "--port=5000", "&"])
        logging.debug("Restarted Flask successfully.")
    except Exception as e:
        logging.error(f"Error restarting Flask: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
