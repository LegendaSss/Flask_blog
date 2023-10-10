from core import app
from core.models import db, User
from datetime import datetime

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
