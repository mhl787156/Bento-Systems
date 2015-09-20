from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
orderitem = Table('orderitem', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('item_id', String(length=64)),
    Column('quantity', Integer),
    Column('sub_price', Numeric(precision=2)),
    Column('order', Integer),
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
    Column('order_counter', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['orderitem'].columns['order'].create()
    post_meta.tables['order'].columns['order_counter'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['orderitem'].columns['order'].drop()
    post_meta.tables['order'].columns['order_counter'].drop()
