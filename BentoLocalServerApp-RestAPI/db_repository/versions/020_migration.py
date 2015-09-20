from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
menuitem = Table('menuitem', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('item_number', Integer),
    Column('item_name', String(length=64)),
    Column('price', Numeric(precision=2)),
    Column('short_description', String(length=128)),
    Column('long_description', String(length=256)),
    Column('availability', Boolean),
    Column('ingrediants', String(length=256)),
    Column('allergens', String(length=256)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menuitem'].columns['item_number'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menuitem'].columns['item_number'].drop()
