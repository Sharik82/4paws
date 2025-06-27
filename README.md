# 4paws 

This is a web app for pet store 4Paws that allows you to browse and buy pet products.  
Developed using Flask, PostgreSQL and Jinja2.

## Functionality
- Browse products
- Adding products to the cart
- Placing an order

## Installation
1. Create and activate a virtual environment.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database tables. The tables will be created automatically on
   first run thanks to `db.create_all()` inside the app factory.

## Environment variables
The application expects a few variables to be present in the environment (for
local development they can be put into a `.env` file):

- `SECRET_KEY` – secret key used by Flask for sessions.
- `DATABASE_URL` – PostgreSQL connection string.
- `LIQPAY_PUBLIC_KEY` – LiqPay API public key.
- `LIQPAY_PRIVATE_KEY` – LiqPay API private key.

## Running the app
- Development server:
  ```bash
  python server.py
  ```
- Production example with Gunicorn:
  ```bash
  gunicorn server:app
  ```

## Deploying to Render
1. Push the repository to GitHub.
2. Create a new **Web Service** on [Render](https://render.com/).
3. Set the required environment variables from the section above.
4. Render will install the dependencies and run the command from `Procfile` which
   starts the app via `gunicorn server:app`.

