from itsdangerous import URLSafeTimedSerializer
from flask import current_app as app

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='lynx-email-confirm-key')


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='lynx-email-confirm-key',
            max_age=expiration
        )
    except:
        return False
    return email