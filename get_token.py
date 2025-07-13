# get_token.py
from google_auth_oauthlib.flow import InstalledAppFlow  # <-- Make sure this import is present

def main():
  flow = InstalledAppFlow.from_client_secrets_file(
    'client_secrets.json',
    scopes=['https://www.googleapis.com/auth/adwords'],
    redirect_uri='https://supreme-couscous-46vrj5p5653rv5g-8080.app.github.dev/'
    )
  creds = flow.run_local_server(port=8080, open_browser=True)
  print("\n🎉 Your refresh token:\n", creds.refresh_token)

if __name__ == "__main__":
    main()









