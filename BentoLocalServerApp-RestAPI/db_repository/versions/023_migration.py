from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
menusection = Table('menusection', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('section_name', String(length=64)),
    Column('number_of_groups', Integer),
    Column('total_number_of_items', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menusection'].columns['number_of_groups'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menusection'].columns['number_of_groups'].drop()
