import os
import json
import pickle
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube"
]

def generate_refresh_token():
    print("=" * 70)
    print("🔑 ONE-TIME YOUTUBE REFRESH TOKEN GENERATOR (FOR GITHUB ACTIONS)")
    print("=" * 70)
    
    client_secrets_file = "client_secret.json"
    if not os.path.exists(client_secrets_file):
        # Look for any client_secret*.json in current directory
        candidates = [f for f in os.listdir(".") if f.startswith("client_secret") and f.endswith(".json")]
        if candidates:
            client_secrets_file = candidates[0]
            print(f"Found client secrets file: {client_secrets_file}")
        else:
            print(f"❌ Error: Could not find '{client_secrets_file}'.")
            print("Please place the downloaded JSON file from Google Cloud into this directory and rename it 'client_secret.json'.")
            return

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES
    )
    
    # Run local webserver to handle Google OAuth login
    print("\nOpening your browser to log into Google and authorize AI Tools Lab...")
    creds = flow.run_local_server(port=8080, prompt="consent", access_type="offline")

    print("\n" + "=" * 70)
    print("🎉 SUCCESS! YOUR YOUTUBE TOKENS HAVE BEEN GENERATED")
    print("=" * 70)
    
    # Read the client secret file to extract client_id and client_secret
    with open(client_secrets_file, "r") as f:
        cs_data = json.load(f)
        key_type = "installed" if "installed" in cs_data else "web"
        client_id = cs_data[key_type]["client_id"]
        client_secret = cs_data[key_type]["client_secret"]

    print("\nAdd these 3 secrets to your GitHub Repository (Settings > Secrets and variables > Actions):\n")
    print("1. Secret Name: YOUTUBE_CLIENT_ID")
    print(f"   Value: {client_id}\n")
    print("2. Secret Name: YOUTUBE_CLIENT_SECRET")
    print(f"   Value: {client_secret}\n")
    print("3. Secret Name: YOUTUBE_REFRESH_TOKEN")
    print(f"   Value: {creds.refresh_token}\n")
    print("=" * 70)
    print("✅ Keep these secret! GitHub Actions will use them to upload videos offline forever.")

if __name__ == "__main__":
    generate_refresh_token()
