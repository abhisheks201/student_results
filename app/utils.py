# import jwt
# from datetime import timedelta,datetime
# # from rest_framework.exceptions import AuthenticationFailed
# from django.conf import settings

# JWT_SECRET_KEY ='django-insecure-os=&ban#mr3zsr*62t_3-glp&b+e@p9*un!soxk5_5)r=!78l9'
# JWT_ACCESS_TOKEN_EXPIRATION = 60
# JWT_REFRESH_TOKEN_EXPIRATION = 1440
# JWT_ALGORITHM = 'HS256'

# def token_required(func):
#     def inner(request, *args, **kwargs):
#         pass
#     return inner

# def get_token_for_user(user):
#     token_payload = {
#         'user_id': str(user.id),
#         'exp': datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRATION),
#         'iat': datetime.utcnow()
#     }
#     access_token = jwt.encode(token_payload, JWT_SECRET_KEY, JWT_ALGORITHM)

#     refresh_token_payload = {
#         'user_id': str(user.id),
#         'exp': datetime.utcnow() + timedelta(days=JWT_REFRESH_TOKEN_EXPIRATION),
#         'iat': datetime.utcnow()
#     }
#     refresh_token = jwt.encode(refresh_token_payload, JWT_SECRET_KEY, JWT_ALGORITHM)
#     return {
#         'access': access_token,
#         'refresh': refresh_token
#     }
