## Urban Dining Restaurant Management Website

Urban Dining is a web-based restaurant management and menu ordering application. It allows users to browse the menu, add items to their cart, and place orders. Admin users have additional privileges, including adding, editing, and deleting menu items, as well as managing orders. The app supports authentication via Google Identity Services (popup/token) and a fallback username/password login system.

---

## Tech Stacks
- **Frontend**: HTML, CSS, JavaScript (with Google Identity Services)
- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-CORS
- **Database:** PostgreSQL
- **Authentication:** JWT (JSON Web Tokens)

---

## Deployment

1. Install requirements
   `pip install -r requirements.txt`
2. Configure Environment Variables with your JWT_SECRET_KEY and GOOGLE_CLIENT_ID
3. Setup PostgreSQL Database
4. Start the Flask backend
   `python backend/app.py`
5. Access the frontend from your browser

---

## Improvements

1. Enhanced UI accessible with phones and laptops
2. Order Management Dashboard for admins as well as order placing feature for users
3. Search and filters in menu
4. Payment Integration
5. Full scale deployment
