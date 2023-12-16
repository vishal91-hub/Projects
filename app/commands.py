
import click
from flask.cli import with_appcontext
  # Import app and db objects from your application

@click.command("create_tables")
@with_appcontext
def create_tables():
    from app import app, db
    db.create_all()
    print("hii bo")
    click.echo("Tables created successfully.")
