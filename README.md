# Password Strength Checker API

API source code built with **FastAPI** to check password strength.  
Includes security headers, rate limiting, and ready-to-deploy Docker support.

## Features

- Check passwords strength via API. (length, special characters, pwned passwords, etc.).
- Basic security middleware. (anti-XSS, clickjacking protection, MIME sniffing protection, HSTS).
- Rate limiting with **SlowAPI**.
- Dockerfile included.
- Ready for deployment on Render.

## Getting start

### Clone project

1. Clone the repository
   ```bash
   git clone https://github.com/MaMuMaMow/PasswordStrength
   ```
2. Create a virtual environment by :
   ```cmd
   cd PasswordStrength
   python -m venv venv
   ```
3. To activate the environment :

- on Linux / Mac :
  ```cmd
  source venv/bin/activate
  ```
- on Window run :
  ```cmd
  venv\Scripts\activate
  ```

4. Install dependencies :

   ```cmd
   -pip install -r requirements.txt
   ```

5. Run the project :
   ```cmd
   uvicorn main:app --reload
   ```

- Optional : try test the project by run the script inside the testAPI folder

## Note

1. This project was build for learning how APIs work.
   Please review the code carefully before using it in production.

2. in case you deploy this on your own website. Make sure to change CORS polices in main.py (line 48)

3. Rate limite can also be adjust in main.py (line 105)

### Thank you for your attention!
