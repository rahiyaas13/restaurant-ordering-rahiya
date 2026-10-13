# Ember & Leaf - Smart Restaurant Ordering & Kitchen Dashboard

Django capstone project: customers browse a menu, build a cart, place an order and
track it by Order ID, while kitchen staff move orders Received -> Preparing -> Ready -> Completed.

Stack: Django, SQLite (db.sqlite3), Bootstrap 5, vanilla JS, Gunicorn, WhiteNoise, Render.

## Run locally

    python -m venv venv
    source venv/bin/activate          # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py makemigrations   # should say "No changes detected"
    python manage.py migrate
    python manage.py seed_menu        # sample categories + 21 menu items
    python manage.py createsuperuser  # staff account for /admin/ and /kitchen/
    python manage.py runserver

Open http://127.0.0.1:8000/ . Kitchen dashboard: /kitchen/ (staff login). Admin: /admin/.

## Deploy to Render

1. `git init && git add . && git commit -m "Prepare Django project for Render" && git push origin main`
2. Render -> New + -> Blueprint (uses render.yaml) and connect the repo.
3. render.yaml generates SECRET_KEY and DJANGO_SUPERUSER_PASSWORD. Read the password in the
   service's Environment tab, then log in at /admin/ or /kitchen/ as `admin`.
4. DEBUG is automatically off on Render (it sets the RENDER env var).

SQLite on Render's free tier is ephemeral: orders reset on restart/redeploy. The menu is
re-seeded automatically on every start.

## How the requirements are met

- Cart: browser localStorage drives the UI (static/js/cart.js); every change is POSTed (with CSRF
  token) to /cart/sync/, which validates it and stores it in the Django session.
- Checkout: totals (subtotal, GST, total) are recalculated on the server from database prices;
  quantities must be 1-20 and items must be available; the session cart is cleared after success.
- Kitchen: /kitchen/ is staff-only; status changes are CSRF-protected POSTs.
- Tracking: /track/ then /track/<order id>/ (auto-refreshes).
