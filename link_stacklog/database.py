"""Module for initializing and connecting to the SQLite database"""
import datetime
import os
import pathlib
import shutil

import click
import sqlite_utils

DATABASE_FILE = "linkstacklog.db"

def user_dir():
    link_stacklog_user_path = os.environ.get("LINK_STACKLOG_USER_PATH")
    if link_stacklog_user_path:
        path = pathlib.Path(link_stacklog_user_path)
    else:
        path = pathlib.Path(click.get_app_dir("link_stacklog"))
    path.mkdir(exist_ok=True, parents=True)
    return path

def get_database(init=False) -> sqlite_utils.Database:
    if not init and not (user_dir() / DATABASE_FILE).exists():
        click.echo("Database not found. Run 'link-stacklog init' first.")
        raise click.Abort()
    return sqlite_utils.Database(user_dir() / DATABASE_FILE)

def init_db():
    db = get_database(init=True)

    db["links"].create({
        "id": int,
        "log_name": str,
        "url": str,
        "title": str,
        "description": str,
        "timestamp": str,
    }, pk="id", defaults={"timestamp": datetime.datetime.now().isoformat()})

    return user_dir() / DATABASE_FILE

def backup_db():
    """Makes a copy of the entire SQLite database with a filename
    containing the ISO date time.
    """
    backup_filename = f"{DATABASE_FILE}_backup_{datetime.datetime.now().isoformat()}.db"
    backup_path = user_dir() / backup_filename
    shutil.copyfile(user_dir() / DATABASE_FILE, backup_path)
    return backup_path
