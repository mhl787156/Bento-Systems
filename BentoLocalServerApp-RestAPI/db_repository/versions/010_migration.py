from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
menu_item = Table('menu_item', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('item_name', VARCHAR(length=64)),
    Column('price', INTEGER),
    Column('short_description', VARCHAR(length=128)),
    Column('long_description', VARCHAR(length=256)),
    Column('availability', BOOLEAN),
    Column('ingrediants', VARCHAR(length=256)),
    Column('allergens', VARCHAR(length=256)),
    Column('menuSection_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['menu_item'].columns['menuSection_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['menu_item'].columns['menuSection_id'].create()
