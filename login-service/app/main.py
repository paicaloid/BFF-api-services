import requests
from app.config import settings
from app.models import Token
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Login-Service",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/access-token", response_model=Token)
async def get_access_token() -> Token:
    url = f"{settings.OIDC_ISSUER}/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": settings.OIDC_CLIENT_ID,
        "client_secret": settings.OIDC_CLIENT_SECRET,
        "audience": settings.OIDC_AUDIENCE,
    }
    headers = {"content-type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        access_token = data["access_token"]
        token_type = data["token_type"]
        expires_in = data["expires_in"]
        return Token(
            access_token=access_token,
            token_type=token_type,
            expires_in=expires_in,
        )
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to retrieve access token",
        )
