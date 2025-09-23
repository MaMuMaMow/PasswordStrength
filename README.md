# Password Strength Checker API

API source code built with **FastAPI** to check password strength.  
Includes security headers, rate limiting, and ready-to-deploy Docker support.

## Features

- Check passwords strength via API. (pwned, length, special characters, and more).
- Basic security middleware. (anti-XSS, clickjacking protection, MIME sniffing protection, HSTS).
- Rate limiting by **SlowAPI**.
- Dockerfile included.
- Ready for deployment on Render.

## How to Get start?

### clone project

1. run **$git clone https://github.com/MaMuMaMow/PasswordStrength** on your Git Bash terminal. this will clone the project floder
2. run **cd PasswordStrength** on your cmd and then follow by **python -m venv venv**
3. if you use Linux / Mac. Run **source venv/bin/activate**.
   if you use Window run **venv\Scripts\activate** instead.

4. loading libaries **-pip install -r requirements.txt**

5. run the project by **uvicorn main:app --reload**. and test the project by run the file in testAPI folder.

## Note

1. This project was build for learning how APIs work.
   Please check the code carefully before you use it in your own website.

2. CORS polices

3. Rate limite

Thank you for your attention!
