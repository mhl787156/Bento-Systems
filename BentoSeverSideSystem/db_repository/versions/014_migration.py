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
    Column('menusection_id', INTEGER),
)

menu_section = Table('menu_section', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('section_name', VARCHAR(length=64)),
    Column('total_number_of_items', INTEGER),
    Column('menu_id', INTEGER),
)

menuitem = Table('menuitem', post_meta,
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

menusection = Table('menusection', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('section_name', String(length=64)),
    Column('total_number_of_items', Integer),
    Column('menu_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['menu_item'].drop()
    pre_meta.tables['menu_section'].drop()
    post_meta.tables['menuitem'].create()
    post_meta.tables['menusection'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['menu_item'].create()
    pre_meta.tables['menu_section'].create()
    post_meta.tables['menuitem'].drop()
    post_meta.tables['menusection'].drop()
