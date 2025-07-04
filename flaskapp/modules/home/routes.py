# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, request, Blueprint
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from flaskapp.modules.home.service import DashboardService

from flaskapp.database.models import db

home_blueprint = Blueprint(
    'home_blueprint',
    __name__,
    url_prefix=''
)

@home_blueprint.route('/index')
@login_required
def index():
    stats = DashboardService.get_dashboard_stats()
    return render_template('home/index.html', segment='index', stats=stats)


@home_blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
