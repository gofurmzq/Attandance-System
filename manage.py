import sys
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from src import db, app

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()