import jwt
import datetime
import uuid


def jwt_token(client_id, secret_id, secret_key, user):
    token = jwt.encode(
        payload={
            "iss": client_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            "jti": str(uuid.uuid4()),
            "aud": "tableau",
            "sub": user,
            "scp": ["tableau:views:embed", "tableau:metrics:embed"],
        },
        key=secret_key,
        algorithm="HS256",
        headers={"kid": secret_id, "iss": client_id},
    )
    return token