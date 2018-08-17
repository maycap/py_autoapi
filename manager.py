# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from flask_script import Manager
from app.routes import app

manager = Manager(app)

@manager.command
def init_db():
    from app.models import Base, some_enginne
    Base.metadata.create_all(some_enginne)

@manager.command
def run():
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    manager.run()