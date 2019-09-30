Advanced SQL with SQLAlchemy
============================

Slides: pygotham-2019.pptx

Using the code:

1) Install PostgreSQL and create a database
2) Create a virtualenv, source it, run `python setup.py develop`
3) `export PYGOTHAM_2019_DB_URL="postgresql://db-user:db-password@db-host:db-port/database-name"`
4) Run `python code/pygotham_2019/bootstrap.py` to setup the database model

You should then be able to run each of the examples from the presentation
(numbered as indicated in the slides).

If you're looking for the table definitions themselves or how the database
connection is set up, see `code/pygotham_2019/model.py for the model
definitions and `code/pygotham_2019/meta.py` for the engine/session/metadata
definitions.
