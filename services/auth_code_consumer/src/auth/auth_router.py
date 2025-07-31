from fastapi import APIRouter, Response
from src.config import get_settings
from src.database.init_database import redis_client
import requests
import json

settings = get_settings()


router = APIRouter(
    prefix="/callback",
    tags=["callback"]
)

@router.get(
    path='/fb-bot'
)
async def save_token_fb_bot(code: str, state: str):
    try:
        token_data = {
            'grant_type': 'authorization_code',
            'client_id': settings.client_id,
            'client_secret': settings.client_secret_key,
            'code': code,
            'redirect_uri': settings.fb_bot_auth_url + "/callback/fb-bot"
        }
        token_response = requests.post(settings.kc_auth_server_url + "/protocol/openid-connect/token", data=token_data)
        token_response.raise_for_status()
        token_info = token_response.json()
        redis_client.set("{0}:{1}".format(settings.redis_keys_name, state), token_info['access_token'])
        redis_client.publish(settings.redis_chanel_name, json.dumps({"user_id": state}))

        return Response(status_code=302, headers={"Location": settings.bot_url})
    except requests.HTTPError as e:
        return {"HTTPError": "Error authorization"}
