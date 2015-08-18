from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
menu = Table('menu', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('menu_name', VARCHAR(length=64)),
    Column('last_date_changed', DATETIME),
    Column('total_number_of_sections', INTEGER),
    Column('total_number_of_items', INTEGER),
)

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

menu_section = Table('menu_section', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('section_name', VARCHAR(length=64)),
    Column('total_number_of_items', INTEGER),
    Column('menu_id', INTEGER),
)

order = Table('order', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('table_number', INTEGER),
    Column('number_of_customers', INTEGER),
    Column('current_number_of_items', INTEGER),
    Column('total_price', INTEGER),
)

order_counter = Table('order_counter', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('current_number_of_orders', INTEGER),
)

order_item = Table('order_item', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('item_number', INTEGER),
    Column('quantity', INTEGER),
    Column('sub_price', INTEGER),
)

order_logger = Table('order_logger', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('date', DATETIME),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['menu'].drop()
    pre_meta.tables['menu_item'].drop()
    pre_meta.tables['menu_section'].drop()
    pre_meta.tables['order'].drop()
    pre_meta.tables['order_counter'].drop()
    pre_meta.tables['order_item'].drop()
    pre_meta.tables['order_logger'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['menu'].create()
    pre_meta.tables['menu_item'].create()
    pre_meta.tables['menu_section'].create()
    pre_meta.tables['order'].create()
    pre_meta.tables['order_counter'].create()
    pre_meta.tables['order_item'].create()
    pre_meta.tables['order_logger'].create()
