import os
import subprocess

def pull_latest_model():
    """
    Pulls the latest model from DagsHub DVC remote.
    """
    print("🔄 Pulling latest model from DVC remote...")
    subprocess.run(["dvc", "pull", "models/model.pkl.dvc"], check=True)
    print("✅ Latest model fetched.")
