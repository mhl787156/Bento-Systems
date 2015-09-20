from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
order = Table('order', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('table_number', Integer),
    Column('number_of_customers', Integer),
    Column('current_number_of_items', Integer),
    Column('total_price', Integer),
    Column('currently_active', Boolean),
    Column('paid', Boolean),
    Column('time_arrived', DateTime),
    Column('time_finished', DateTime),
    Column('time_elapsed', DateTime),
)

order_item = Table('order_item', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('item_number', Integer),
    Column('quantity', Integer),
    Column('sub_price', Integer),
    Column('menu_item', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['order'].create()
    post_meta.tables['order_item'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['order'].drop()
    post_meta.tables['order_item'].drop()
