import requests
import firebase_admin
from firebase_admin import credentials, firestore
import time

# ======= CONFIGURAÇÕES FIREBASE =======
firebase_config = {
    "apiKey": "AIzaSyBMJ_OR41iCIMGDEmGYUkf1mI6Aym9W04w",
    "projectId": "dashboard-f0217",
    "authDomain": "dashboard-f0217.firebaseapp.com",
}

# Inicializa o Firebase Admin SDK

cred = credentials.Certificate(r"C:\Users\produ\Desktop\AI\PYTHON BACKEND\dashboard-f0217-firebase-adminsdk-fbsvc-afee65e5ba.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ======= CONFIGURAÇÕES TWITCH =======
TWITCH_CLIENT_ID = "1s3dfohdt6t7wfjq1adycz4iel5t98"
TWITCH_CLIENT_SECRET = "a9nxmsa7e5xy7fy5gd7erzp81uoqf3"
TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
TWITCH_STREAMS_URL = "https://api.twitch.tv/helix/streams"

# ======= FUNÇÕES AUXILIARES =======

def get_twitch_access_token():
    """Obtém token temporário de acesso à API da Twitch."""
    response = requests.post(TWITCH_TOKEN_URL, params={
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    })
    response.raise_for_status()
    return response.json()["access_token"]

def extract_channel_name(url: str) -> str:
    """Extrai o nome do canal a partir da URL da Twitch."""
    if not url:
        return None
    # Exemplo: https://www.twitch.tv/nick123
    parts = url.rstrip("/").split("/")
    return parts[-1] if len(parts) > 0 else None

def is_channel_live(channel_name: str, access_token: str) -> bool:
    """Verifica se o canal está online na Twitch."""
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }
    params = {"user_login": channel_name}
    response = requests.get(TWITCH_STREAMS_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return len(data["data"]) > 0  # True se estiver online

def update_streamer_status():
    """Atualiza o campo isOnline na coleção streamers."""
    print("🔄 Atualizando status dos streamers...")
    access_token = get_twitch_access_token()

    streamers_ref = db.collection("streamers")
    streamers = streamers_ref.stream()

    for doc in streamers:
        data = doc.to_dict()
        stream_url = data.get("streamUrl")

        channel = extract_channel_name(stream_url)
        if not channel:
            print(f"⚠️ Streamer {doc.id} sem URL válida.")
            continue

        try:
            online = is_channel_live(channel, access_token)
            streamers_ref.document(doc.id).update({"isOnline": online})
            print(f"✅ {channel}: {'Online' if online else 'Offline'}")
        except Exception as e:
            print(f"❌ Erro ao verificar {channel}: {e}")

if __name__ == "__main__":
    while True:
        update_streamer_status()
        print("⏳ Aguardando 5 minutos para próxima verificação...")
        time.sleep(300)  # 5 minutos
