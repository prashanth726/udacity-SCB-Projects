from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


moment = Moment()
db = SQLAlchemy()
migrate = Migrate()
