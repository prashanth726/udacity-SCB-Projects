#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from forms import *
from flask_wtf import Form
from logging import Formatter, FileHandler
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask import Flask, render_template, request, Response, flash, redirect, url_for
import babel
import dateutil.parser
import json
import collections
import collections.abc

from forms import ShowForm
collections.Callable = collections.abc.Callable
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)


# Migrate DB

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    print(id)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text)
    website = db.Column(db.String(200))
    genres = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue', lazy='dynamic')


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    website = db.Column(db.String(200))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text)
    past_shows_count = db.Column(db.Integer, default=0)
    shows = db.relationship('Show', backref='artist', lazy='dynamic')

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

    view_data = []
    venuesData = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()

    for venue in venuesData:
        upcoming_shows_count = Show.query.filter_by(venue_id=venue.id).filter(
            Show.start_time > datetime.now().strftime('%Y-%m-%d %H:%S:%M')).all()
        view_data.append({
            "city": venue.city,
            "state": venue.state,
            "venues": [{
                "id": venue.id,
                "name": venue.name,
                "upcoming_shows_count": len(upcoming_shows_count)
            }]
        })

    return render_template('pages/venues.html', areas=view_data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')

    view_data = []
    venuesData = Venue.query.filter(
        Venue.name.ilike('%' + search_term + '%')).all()

    for venue in venuesData:
        upcoming_shows_count = Show.query.filter_by(venue_id=venue.id).filter(
            Show.start_time > datetime.now().strftime('%Y-%m-%d %H:%S:%M')).all()
        view_data.append({
            "id": venue.id,
            "name": venue.name,
            "upcoming_shows_count": len(upcoming_shows_count)
        })

    response = {
        "count": len(venuesData),
        "data": view_data
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venueData = Venue.query.get(venue_id)
    showsData = Show.query.filter_by(venue_id=venue_id).all()
    past_shows = []
    upcoming_shows = []
    for show in showsData:
        if str(show.start_time) < str(datetime.now().strftime('%Y-%m-%d %H:%S:%M')):
            past_shows.append({
                "artist_image_link": show.artist.image_link,
                "start_time": format_datetime(str(show.start_time)),
                "artist_id": show.artist_id,
                "artist_name": show.artist.name})
        else:
            upcoming_shows.append({
                "artist_image_link": show.artist.image_link,
                "start_time": format_datetime(str(show.start_time)),
                "artist_id": show.artist_id,
                "artist_name": show.artist.name})

    venue = {
        "id": venueData.id,
        "name": venueData.name,
        "genres": venueData.genres,
        "address": venueData.address,
        "city": venueData.city,
        "state": venueData.state,
        "phone": venueData.phone,
        "website": venueData.website,
        "facebook_link": venueData.facebook_link,
        "seeking_talent": venueData.seeking_talent,
        "seeking_description": venueData.seeking_description,
        "image_link": venueData.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)

    name = form.name.data
    city = form.city.data
    state = form.state.data
    address = form.address.data
    phone = form.phone.data
    genres = form.genres.data
    facebook_link = form.facebook_link.data
    image_link = form.image_link.data
    website_link = form.website_link.data
    seeking_talent_checkbox = form.seeking_talent.data
    seeking_description_box = form.seeking_description.data

    if form.validate():
        try:
            # on successful db insert, flash success message
            new_venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link,
                              image_link=image_link, website=website_link, seeking_talent=seeking_talent_checkbox, seeking_description=seeking_description_box)
            db.session.add(new_venue)
            db.session.commit()
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')
            return render_template('pages/home.html')
        except Exception as e:
            print(e)
            # db insert failed, flash failed message and log the error
            flash('Something went wrong, Unable to insert venue')
            return render_template('pages/home.html')

    else:
        print(form.errors)
        flash('An error occurred. Venue ' + name + ' could not be listed.')
        return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue = Venue.query.get(venue_id)
        db.session.delete(Venue)
        db.session.commit()
        return None
    except Exception as e:
        print(e)
        return None
        # db delete failed

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():

    view_data = []
    artistData = Artist.query.all()
    print(artistData)
    for artist in artistData:
        view_data.append(
            {
                "id": artist.id,
                "name": artist.name,
            }
        )
    print(view_data)
    return render_template('pages/artists.html', artists=view_data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')

    view_data = []
    artistData = Artist.query.filter(
        Artist.name.ilike('%' + search_term + '%')).all()

    for artist in artistData:
        view_data.append({
            "id": artist.id,
            "name": artist.name,
        })

    response = {
        "count": len(artistData),
        "data": view_data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artistData = Artist.query.get(artist_id)
    showsData = Show.query.filter_by(artist_id=artist_id).all()
    past_shows = []
    upcoming_shows = []
    for show in showsData:
        if str(show.start_time) < str(datetime.now().strftime('%Y-%m-%d %H:%S:%M')):
            past_shows.append({
                "venue_image_link": show.venue.image_link,
                "start_time": format_datetime(str(show.start_time)),
                "venue_id": show.venue_id,
                "venue_name": show.venue.name})
        else:
            upcoming_shows.append({
                "venue_image_link": show.venue.image_link,
                "start_time": format_datetime(str(show.start_time)),
                "venue_id": show.venue_id,
                "venue_name": show.venue.name})

    artist = {
        "id": artistData.id,
        "name": artistData.name,
        "genres": artistData.genres,
        "city": artistData.city,
        "state": artistData.state,
        "phone": artistData.phone,
        "website": artistData.website,
        "facebook_link": artistData.facebook_link,
        "seeking_venue": artistData.seeking_venue,
        "seeking_description": artistData.seeking_description,
        "image_link": artistData.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)

    if form.validate():
        try:
            artist = Artist.query.get(artist_id)
            artist.name = form.name.data
            artist.city = form.city.data
            artist.state = form.state.data
            artist.phone = form.phone.data
            artist.genres = form.genres.data
            artist.facebook_link = form.facebook_link.data
            artist.image_link = form.image_link.data
            artist.website = form.website_link.data
            artist.seeking_venue = form.seeking_venue.data
            artist.seeking_description_box = form.seeking_description.data
            # on successful db insert, flash success message
            db.session.commit()
            flash('Artist ' + form.name.data +
                  ' was successfully updated!')
            return redirect(url_for('show_artist', artist_id=artist_id))
        except Exception as e:
            print(e)
            # db insert failed, flash failed message and log the error
            flash('Something went wrong, Unable to update Artist')
            return redirect(url_for('show_artist', artist_id=artist_id))

    else:
        print(form.errors)
        flash('An error occurred. Artist ' +
              str(artist_id) + ' could not be updated.')
        return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm(request.form)

    if form.validate():
        try:
            venue = Venue.query.get(venue_id)
            venue.name = form.name.data
            venue.city = form.city.data
            venue.state = form.state.data
            venue.phone = form.phone.data
            venue.genres = form.genres.data
            venue.facebook_link = form.facebook_link.data
            venue.image_link = form.image_link.data
            venue.website = form.website_link.data
            venue.seeking_talent = form.seeking_talent.data
            venue.seeking_description = form.seeking_description.data
            # on successful db insert, flash success message
            db.session.commit()
            flash('Venue ' + form.name.data +
                  ' was successfully updated!')
            return redirect(url_for('show_venue', venue_id=venue_id))
        except Exception as e:
            print(e)
            # db insert failed, flash failed message and log the error
            flash('Something went wrong, Unable to update Venue')
            return redirect(url_for('show_venue', venue_id=venue_id))

    else:
        print(form.errors)
        flash('An error occurred. Venue ' +
              str(venue_id) + ' could not be updated.')
        return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form)

    name = form.name.data
    city = form.city.data
    state = form.state.data
    phone = form.phone.data
    genres = form.genres.data
    facebook_link = form.facebook_link.data
    image_link = form.image_link.data
    website_link = form.website_link.data
    seeking_venue_checkbox = form.seeking_venue.data
    seeking_description_box = form.seeking_description.data

    if form.validate():
        try:
            # on successful db insert, flash success message
            new_artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link,
                                image_link=image_link, website=website_link, seeking_venue=seeking_venue_checkbox, seeking_description=seeking_description_box)
            db.session.add(new_artist)
            db.session.commit()
            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')
            return render_template('pages/home.html')
        except Exception as e:
            print(e)
            # db insert failed, flash failed message and log the error
            flash('Something went wrong, Unable to insert Artist')
            return render_template('pages/home.html')

    else:
        print(form.errors)
        flash('An error occurred. Artist ' + name + ' could not be listed.')
        return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():

    view_data = []
    showsData = Show.query.all()

    for show in showsData:
        print(show)
        view_data.append({
            "artist_image_link": show.artist.image_link,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "start_time": format_datetime(str(show.start_time)),
            "venue_id": show.venue_id,
            "venue_name": show.venue.name})
    print(view_data)
    return render_template('pages/shows.html', shows=view_data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm(request.form)

    artist_id = form.artist_id.data
    venue_id = form.venue_id.data
    start_time = form.start_time.data

    if form.validate():
        try:
            # on successful db insert, flash success message
            new_show = Show(artist_id=artist_id,
                            venue_id=venue_id, start_time=start_time)
            db.session.add(new_show)
            db.session.commit()
            flash('Show with artist_id' + artist_id +
                  ' was successfully listed!')
            return render_template('pages/home.html')
        except Exception as e:
            print(e)
            # db insert failed, flash failed message and log the error
            flash('Something went wrong, Unable to insert Show')
            return render_template('pages/home.html')

    else:
        print(form.errors)
        flash('An error occurred. Show with artist ID ' +
              artist_id + ' could not be listed. Please make sure you entered correct artist ID and Venue ID')
        return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
