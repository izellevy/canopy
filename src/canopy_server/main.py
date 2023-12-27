# # main.py
# from fastapi import FastAPI, Request
# from auth import authenticate, TokenPayload
# from datetime import timedelta
#
# app = FastAPI()
#
#
#
# @app.get("/protected")
# async def protected_route(request: Request):
#     current_user: TokenPayload = request.state.current_user
#     return {"message": "This is a protected route", "current_user": current_user.sub}
#
#
# @app.get("/generate_token")
# async def generate_token():
#     # Generate a JWT token with a 30-minute expiration time
#     token_subject = "example_user"
#     token_expiration = timedelta(minutes=30)
#     jwt_token = create_jwt_token(token_subject, token_expiration)
#     return {"jwt_token": jwt_token}å
