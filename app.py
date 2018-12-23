#!/usr/bin/env python3

from os.path import exists
from models import *

database_name = "tcenter.db"
create_tables = not exists(database_name)
db = open_database(database_name)

if create_tables:
    create_tables(db)

close_database(db)