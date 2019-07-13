from flask_script import Manager
from main import app, db
from flask_migrate import Migrate, MigrateCommand
import models
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()