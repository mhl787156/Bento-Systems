from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('table_number', INTEGER),
    Column('number_of_customers', INTEGER),
    Column('current_number_of_items', INTEGER),
    Column('total_price', INTEGER),
    Column('currently_active', BOOLEAN),
    Column('paid', BOOLEAN),
    Column('time_arrived', DATETIME),
    Column('time_finished', DATETIME),
    Column('time_elapsed', DATETIME),
    Column('staggered_service', BOOLEAN),
)

order_item = Table('order_item', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('item_number', INTEGER),
    Column('quantity', INTEGER),
    Column('sub_price', INTEGER),
    Column('menu_item', INTEGER),
)

order = Table('order', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('table_number', Integer),
    Column('number_of_customers', Integer),
    Column('current_number_of_items', Integer),
    Column('total_price', Numeric(precision=2)),
    Column('currently_active', Boolean),
    Column('staggered_service', Boolean),
    Column('paid', Boolean),
    Column('time_arrived', DateTime),
    Column('time_finished', DateTime),
    Column('time_elapsed', DateTime),
)

ordercounter = Table('ordercounter', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('day', Date),
    Column('current_number_of_active_orders', Integer),
    Column('total_number_of_orders', Integer),
    Column('total_income', Numeric(precision=2)),
)

orderitem = Table('orderitem', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('item_id', String(length=64)),
    Column('quantity', Integer),
    Column('sub_price', Numeric(precision=2)),
)

menuitem = Table('menuitem', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('item_id', String(length=64)),
    Column('item_name', String(length=64)),
    Column('price', Numeric(precision=2)),
    Column('short_description', String(length=128)),
    Column('long_description', String(length=256)),
    Column('availability', Boolean),
    Column('ingrediants', String(length=256)),
    Column('allergens', String(length=256)),
)

menusection = Table('menusection', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('section_name', String(length=64)),
    Column('number_of_groups', Integer),
    Column('total_number_of_items', Integer),
    Column('visibility', Boolean),
    Column('staggered_service_order', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].drop()
    pre_meta.tables['order_item'].drop()
    post_meta.tables['order'].create()
    post_meta.tables['ordercounter'].create()
    post_meta.tables['orderitem'].create()
    post_meta.tables['menuitem'].columns['item_id'].create()
    post_meta.tables['menusection'].columns['staggered_service_order'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    pre_meta.tables['order_item'].create()
    post_meta.tables['order'].drop()
    post_meta.tables['ordercounter'].drop()
    post_meta.tables['orderitem'].drop()
    post_meta.tables['menuitem'].columns['item_id'].drop()
    post_meta.tables['menusection'].columns['staggered_service_order'].drop()
