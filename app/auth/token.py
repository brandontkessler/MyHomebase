from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


def gen_token(email, expires_sec=1800):
    s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_email': email}).decode('utf-8')


def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        user_email = s.loads(token)['user_email']
    except:
        return None
    return user_email
