import json
import requests
from flask import render_template, Blueprint, url_for, redirect, flash
from flask_login import login_required, current_user

from app import db
from app.decorators import check_confirmed
from app.main.forms import EditMyHomebaseForm


main = Blueprint('main', __name__)


with open('api_keys.json') as api_keys_file:
    api_keys = json.load(api_keys_file)


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.myhomebase'))
    else:
        return render_template('index.html')


@login_required
@check_confirmed
@main.route('/myhomebase', methods=['GET', 'POST'])
def myhomebase():
    lat = current_user.latitude
    long = current_user.longitude

    url = f"https://api.darksky.net/forecast/{api_keys.get('DARKSKY_KEY')}/{lat},{long}"
    weather_json = requests.get(url).json()

    return render_template('myhomebase.html', weather=weather_json)


@login_required
@check_confirmed
@main.route('/myhomebase/edit', methods=['GET', 'POST'])
def edit_myhomebase():
    form = EditMyHomebaseForm()

    if form.validate_on_submit():
        new_city = form.city.data.strip()
        geocoord_url = f"http://open.mapquestapi.com/geocoding/v1/address?key={api_keys.get('MAPQUEST_KEY')}&location={new_city}"
        geo_api_call = requests.get(geocoord_url).json()
        lat_long = geo_api_call['results'][0]['locations'][0]['latLng']
        lat = lat_long.get('lat')
        long = lat_long.get('lng')

        current_user.city = new_city
        current_user.latitude = lat
        current_user.longitude = long

        db.session.commit()

        flash('Your homebase has been edited.', 'success')
        return redirect(url_for('main.edit_myhomebase'))

    return render_template('edit_myhomebase.html', form=form)


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', e=e), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


@main.app_errorhandler(403)
def page_not_found(e):
    return render_template('errors/403.html'), 403
