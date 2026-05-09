from fastapi import FastAPI, Request
from webauthn import (generate_registration_options, 
                      options_to_json, 
                      verify_registration_response, 
                      base64url_to_bytes,
                      generate_authentication_options,
                      verify_authentication_response,
                )
import json
from fastapi.responses import JSONResponse, FileResponse 
from fastapi.staticfiles import StaticFiles 
from webauthn.helpers.structs import PublicKeyCredentialDescriptor, UserVerificationRequirement
import os 


api = FastAPI()

RP_ID = "surprise-zigzagged-undecided.ngrok-free.dev"   # ngrok domain 
RP_NAME = "My WebAuthn Service"

db = {
    "challenges": {}, # {"username": "challenge"}
    "users": {}  # {"username":{"credential_id":bytes,"public_key":bytes,"sign_count":int}}
}

# Methods: GET, POST, PUT, DELETE 
@api.get("/")   # path: "/"
def index():
    return {"message": "Hello World!"}   # json object


# Registration Ceremony
@api.get("/register/options") 
def get_registration_options(username: str):
    user_id_bytes = username.encode("utf-8")  # bytes
    
    options  = generate_registration_options(
        rp_id = RP_ID,
        rp_name = RP_NAME,
        user_id = user_id_bytes,   # Unique user id 
        user_name = username,
    )
    
    # Storing challenge for later verification
    db["challenges"][username] = options.challenge  
    
    # return options_to_json(options)  # For JSON response 
    return JSONResponse(content=json.loads(options_to_json(options)))
  
@api.post("/register/verify") 
async def verify_registrationv(request: Request, username: str): 
    registration_credential = await request.json()  # JSON body from request
    stored_challenge = db["challenges"].get(username)  # Stored challenge for verification
    
    try:
        verification = verify_registration_response(
            credential = registration_credential,
            expected_challenge = stored_challenge,
            expected_origin = f"https://{RP_ID}",    # ORIGIN / f"http://{RP_ID}"
            expected_rp_id = RP_ID,
            require_user_verification=True,
        ) 
        
        db["users"][username] = {
            "credential_id": verification.credential_id,
            "public_key": verification.credential_public_key,
            "sign_count": verification.sign_count,
        }
        
        return {"status": "ok", "message": "Registration successful!"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
 
# Authentication Ceremony 
@api.get("/login/options")
def get_login_options(username: str):
    user_data = db["users"].get(username)
    if not user_data:
        return JSONResponse(status_code=404, content={"message": "User not found"})

    allowed_credential = PublicKeyCredentialDescriptor(
        id=user_data["credential_id"]
    )

    options = generate_authentication_options(
        rp_id=RP_ID,
        allow_credentials = [allowed_credential],
        user_verification = UserVerificationRequirement.REQUIRED,
    )
    
    db["challenges"][username] = options.challenge
    return JSONResponse(content=json.loads(options_to_json(options)))


@api.post("/login/verify")
async def verify_login(request: Request, username: str):
    auth_credential = await request.json()
    user_data = db["users"].get(username)
    stored_challenge = db["challenges"].get(username)
    
    credential_id_bytes = base64url_to_bytes(auth_credential['id'])
    if credential_id_bytes != user_data["credential_id"]:
        return {"status": "error", "message": "Credential ID mismatch!"}

    try:
        verification = verify_authentication_response(
            credential = auth_credential,
            expected_challenge = stored_challenge,
            expected_rp_id = RP_ID,
            expected_origin = f"https://{RP_ID}",
            credential_public_key = user_data["public_key"],
            credential_current_sign_count = user_data["sign_count"],
            require_user_verification = True,
        )
        
        # Update sign count 
        db["users"][username]["sign_count"] = verification.new_sign_count
        return {"status": "ok", "message": "Login successful!"}
    
    except Exception as e:
        print(f"Verification Error: {e}")
        return {"status": "error", "message": str(e)}
 
    
@api.get("/gui")
def get_gui():
    return FileResponse("index.html")
    

