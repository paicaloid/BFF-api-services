import requests
from app.config import settings
from app.deps import get_current_user
from app.models import Token
from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

security = HTTPBearer()

app = FastAPI(
    title="BFF-Service",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/access-token", response_model=Token)
async def get_access_token() -> Token:
    url = f"http://{settings.LOGIN_SERVICE_URL}:{settings.LOGIN_SERVICE_PORT}/access-token"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return Token(
                access_token=data["access_token"],
                token_type=data["token_type"],
            )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to retrieve access token",
            )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Request to login service failed: {str(e)}",
        )


@app.get("/protected", dependencies=[Depends(get_current_user)])
async def protected_route():
    return {"message": "This is a protected route."}


# @app.get("/test_auth")
# def read_current_user(
#     credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
# ):
#     return {"scheme": credentials.scheme, "credentials": credentials.credentials}
