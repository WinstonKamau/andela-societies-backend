"""Entry point for app, contain commands to configure and run the app."""

import os
import sys

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, prompt_bool

from api.utils.initial_data import test_data, production_data
from api.models import Activity, Society, User, db
from app import create_app
from run_tests import test


app = create_app(environment=os.environ.get('APP_SETTINGS', "Development"))
manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def drop_database():
    """Drop database tables."""
    if prompt_bool("Are you sure you want to lose all your data"):
        try:
            db.drop_all()
            print("Dropped all tables successfully.")
        except Exception:
            print("Failed, make sure your database server is running!")


@manager.command
def create_database():
    """Create database tables from sqlalchemy models."""
    try:
        db.create_all()
        print("Created tables successfully.")
    except Exception:
        db.session.rollback()
        print("Failed, make sure your database server is running!")


@manager.command
def seed():
    """Seed database tables with initial data."""
    environment = os.getenv("APP_SETTINGS", "Production")
    if environment.lower() in ["production", "staging"] and \
            os.getenv("PRODUCTION_SEED") != "True":
        print("\n\t\tYou probably don't wanna do that.\n")
        sys.exit()

    data_mapping = {
        "Production": production_data,
        "Development": test_data,
        "Testing": test_data,
        "Staging": production_data
    }
    if environment == "Testing" or \
        prompt_bool("\n\n\nThis operation will remove all existing data."
                    " Are you sure you want to continue?"):
        try:
            db.drop_all()
            db.create_all()
            db.session.add_all(data_mapping.get(environment))
            db.session.commit()
            print("\n\n\nTables seeded successfully.\n\n\n")
        except Exception as e:
            db.session.rollback()
            print("\n\n\nFailed:\n", e, "\n\n")


def shell():
    """Make a shell/REPL context available."""
    return dict(app=app,
                db=db,
                User=User,
                Society=Society,
                Activity=Activity)


manager.add_command("shell", Shell(make_context=shell))
manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    if sys.argv[1] == 'test':
        test()
    else:
        manager.run()
