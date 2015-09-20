from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
order_item = Table('order_item', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('item_number', INTEGER),
    Column('quantity', INTEGER),
    Column('sub_price', INTEGER),
    Column('menu_item', INTEGER),
)

menuitem_to_orderitem = Table('menuitem_to_orderitem', post_meta,
    Column('orderitem_id', Integer),
    Column('menuitem_id', Integer),
)

orderitem = Table('orderitem', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('item_number', Integer),
    Column('quantity', Integer),
    Column('sub_price', Integer),
)

menusection = Table('menusection', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('section_name', String(length=64)),
    Column('number_of_groups', Integer),
    Column('total_number_of_items', Integer),
    Column('visibility', Boolean),
    Column('staggered_service_order', Integer),
)

order = Table('order', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('table_number', Integer),
    Column('number_of_customers', Integer),
    Column('current_number_of_items', Integer),
    Column('total_price', Integer),
    Column('currently_active', Boolean),
    Column('staggered_service', Boolean),
    Column('paid', Boolean),
    Column('time_arrived', DateTime),
    Column('time_finished', DateTime),
    Column('time_elapsed', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['order_item'].drop()
    post_meta.tables['menuitem_to_orderitem'].create()
    post_meta.tables['orderitem'].create()
    post_meta.tables['menusection'].columns['staggered_service_order'].create()
    post_meta.tables['order'].columns['staggered_service'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['order_item'].create()
    post_meta.tables['menuitem_to_orderitem'].drop()
    post_meta.tables['orderitem'].drop()
    post_meta.tables['menusection'].columns['staggered_service_order'].drop()
    post_meta.tables['order'].columns['staggered_service'].drop()
