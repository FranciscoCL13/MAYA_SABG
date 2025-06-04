# app/api_efirma/__init__.py
from .routes import efirma_bp


@efirma_bp.route("/login")
def login_page():
    return render_template("login.html")
