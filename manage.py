import unittest
import coverage

from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from models import db, app
import os


COV = coverage.coverage(
    branch=True,
    include='/*',
    omit=[
        'tests/*','venv/*','/usr/*','manage.py'

    ]
)
COV.start()


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('tests/')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1

@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def initdb():
    db.create_all()

    print("Successfully created")

@manager.command
def dropdb():
    if prompt_bool("Are you sure ?"):
        db.drop_all()
        print("Db dropp")

if __name__=='__main__':
    manager.run()