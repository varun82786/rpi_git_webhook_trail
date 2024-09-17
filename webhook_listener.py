import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Pull latest changes
    os.chdir('/Users/Data/Software_dev/weather_union')
    subprocess.call(['git', 'pull'])

    # Start the build process
    build_process()

    return 'Build started', 200

def build_process():
    # Add your build commands here
    # Example: subprocess.call(['python3', 'setup.py', 'install'])
    subprocess.call(['python3', 'weather_server.py'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
