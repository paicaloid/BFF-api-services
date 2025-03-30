import jwt
from app.config import settings
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

jwks_url = f"{settings.OIDC_ISSUER}/.well-known/jwks.json"
jwk_client = PyJWKClient(jwks_url)

security = HTTPBearer()


def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    try:
        # Reuse the initialized jwk_client to get the signing key
        signing_key = jwk_client.get_signing_key_from_jwt(token.credentials)

        # Decode and validate the token
        decoded_token = jwt.decode(
            token.credentials,
            signing_key.key,
            algorithms=["RS256"],
            audience=settings.OIDC_AUDIENCE,
            issuer=f"{settings.OIDC_ISSUER}/",
        )
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired.",
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}",
        )
