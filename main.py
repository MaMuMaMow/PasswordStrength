import string
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import requests
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
#_________________________API and Rate Limiter Setup______________________________________

app = FastAPI(
    title="Password Strength Checker API",
    description="API for checking password strength and leaked status",
    version="1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# ________________________Security Middlewares__________________________________________
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff" #MIME
    response.headers["X-Frame-Options"] = "DENY" #clickjacking
    response.headers["Content-Security-Policy"] = "default-src 'self';" #XSS
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains" #HTTPS
    return response

# _____________________________Rate Limits & CORS______________________________________

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

logging.basicConfig(
    filename='api_security.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],       #fix CORS policy here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#___________________________function for checking leaked password____________________________

def pwned(password):
    sha = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    pre = sha[:5]
    suf = sha[5:]
    try:
        res = requests.get(f"https://api.pwnedpasswords.com/range/{pre}", timeout=3)
    except Exception as e:
        logging.error(f"Error calling pwned API: {e}")
        return {"id": "Error", "reason": "Could not check leaked status, external service error"}
    
    if res.status_code != 200:
        return {"id": "Error", "reason": "Could not check leaked status, external service error"}

    hashes = (line.split(':') for line in res.text.splitlines())
    for h,count in hashes:
        if h == suf:
            return 1
    return 0


#___________________________________Rate limite handler__________________________________


@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):


    logging.warning(
        f"Rate limit exceeded - IP: {request.client.host} - "
        f"Path: {request.url.path} - "
        f"User-Agent: {request.headers.get('user-agent')}"
    )  
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "detail": "Too many requests. Please try again later.",
            "retry_after": exc.retry_after
        }
    )



#<<____________________________________Password strength Check_______________________________________>>
class PasswordInput(BaseModel):
    password: str
    request_id: Optional[str] = None

@app.post("/checkStrength")
@limiter.limit("60/minute")     #change the rate limit here
async def password_strength_checker(request: Request, pass_input: PasswordInput):
    password = pass_input.password
    responses = []

    if len(password) > 128: #128 Because hashcat limits at 128 characters
        responses.append({
            "id": "Error",
            "reason": "Password length cannot exceed 128 characters"
        })
        return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": responses,
            "metadata": {
                "time": datetime.now().isoformat(),
                "API version": "1.0"
            }
        })

    elif len(password) == 0:
        responses.append({
            "id": "Error",
            "reason": "Password cannot be empty"
        })

        return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": responses,
            "metadata": {
                "time": datetime.now().isoformat(),
                "API version": "1.0"
            }
        })



#___________________________Main Logic_____________________________________
    if len(password) < 8:
        responses.append({
            "id": 1,
            "reason": "password should be longer than 8 characters"
        })     

    if password.lower() == password or password.upper() == password:
        responses.append({
            "id": 2,
            "reason": "password should have uppercase and lowercase letters"
        })

    if not any(char.isdigit() for char in password):
        responses.append({
            "id": 3,
            "reason": "password should have numbers"
        })
        
    if not any(char in string.punctuation for char in password):
        responses.append({
            "id": 4,
            "reason": "password should have special characters"
        })
        
    if pwned(password) :
        responses.append({
            "id": 5,
            "reason": "password has been leaked before"
        })

    password = None  #in case hacker know how to read memory someway somehow.

    if len(responses) == 0:
        responses.append({
            "id": 0,
            "reason": "Strong Password"
        })
        
#_______________________________________Return Result___________________________________________


    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": responses,
            "metadata": {
                "time": datetime.now().isoformat(),
                "API version": "1.0"
            }
        }
    )