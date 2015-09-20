from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
    Column('orderitem_id', INTEGER),
)

menuitem_to_orderitem = Table('menuitem_to_orderitem', post_meta,
    Column('orderitem', Integer),
    Column('menuitem', Integer),
)

orderitem = Table('orderitem', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('quantity', INTEGER),
    Column('sub_price', NUMERIC(precision=2)),
    Column('order', INTEGER),
    Column('item_id', VARCHAR(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].drop()
    post_meta.tables['menuitem_to_orderitem'].create()
    pre_meta.tables['orderitem'].columns['item_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    post_meta.tables['menuitem_to_orderitem'].drop()
    pre_meta.tables['orderitem'].columns['item_id'].create()
