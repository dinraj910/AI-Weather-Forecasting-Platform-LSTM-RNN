
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/report')
def report():
    return render_template('report.html')
