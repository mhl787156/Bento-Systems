from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
menu_item = Table('menu_item', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('item_name', String(length=64)),
    Column('price', Integer),
    Column('short_description', String(length=128)),
    Column('long_description', String(length=256)),
    Column('availability', Boolean),
    Column('ingrediants', String(length=256)),
    Column('allergens', String(length=256)),
    Column('menusection_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menu_item'].columns['menusection_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menu_item'].columns['menusection_id'].drop()
