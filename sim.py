import db
import particles
import click
import os
import yaml
import config

default_sql = os.path.join(os.getcwd(), 'data/particles.db')

@click.group()
def cli():
    pass

@cli.command()
@click.argument('settings_filepath', type=click.Path(exists=True))
@click.argument('n_copies', type=int)
@click.argument('sqlite_filepath', type=click.Path(), required=False)
def simulate(settings_filepath, n_copies, sqlite_filepath,):
    if not sqlite_filepath:
        sqlite_filepath = default_sql
    with open(settings_filepath, "r") as f:
        conf = yaml.full_load(f)
    conf = config.check_yaml(conf)
    session = db.get_session(sqlite_filepath)

    print('Generating images')
    particles.generate_images(conf, session, n_copies)

        



@cli.command()
@click.argument('sqlite_path', default = None, required=False)
@click.confirmation_option(prompt='This will delete the current database, are you sure?')
def dbinit(sqlite_path):
    if not sqlite_path:
        sqlite_path = default_sql
    db.initialize_db_tool(sqlite_path)

if __name__ == '__main__':
    cli()
