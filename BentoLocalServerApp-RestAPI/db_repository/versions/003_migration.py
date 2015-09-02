from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
menu = Table('menu', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('menu_name', String(length=64)),
    Column('last_date_changed', DateTime),
    Column('total_number_of_sections', Integer),
    Column('total_number_of_items', Integer),
)

menu_item = Table('menu_item', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('item_name', String(length=64)),
    Column('price', Integer),
    Column('short_description', String(length=128)),
    Column('long_description', String(length=256)),
    Column('availability', Boolean),
    Column('ingrediants', String(length=256)),
    Column('allergens', String(length=256)),
    Column('menuSection_id', Integer),
)

menu_section = Table('menu_section', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('section_name', String(length=64)),
    Column('total_number_of_items', Integer),
    Column('menu_id', Integer),
)

order = Table('order', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('table_number', Integer),
    Column('number_of_customers', Integer),
    Column('current_number_of_items', Integer),
    Column('total_price', Integer),
)

order_counter = Table('order_counter', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('current_number_of_orders', Integer),
)

order_item = Table('order_item', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('item_number', Integer),
    Column('quantity', Integer),
    Column('sub_price', Integer),
)

order_logger = Table('order_logger', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('date', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menu'].create()
    post_meta.tables['menu_item'].create()
    post_meta.tables['menu_section'].create()
    post_meta.tables['order'].create()
    post_meta.tables['order_counter'].create()
    post_meta.tables['order_item'].create()
    post_meta.tables['order_logger'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menu'].drop()
    post_meta.tables['menu_item'].drop()
    post_meta.tables['menu_section'].drop()
    post_meta.tables['order'].drop()
    post_meta.tables['order_counter'].drop()
    post_meta.tables['order_item'].drop()
    post_meta.tables['order_logger'].drop()
