from flask import Blueprint, render_template, flash
from app.utils import redirect_back

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

