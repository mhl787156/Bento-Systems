from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
section_to_subsection = Table('section_to_subsection', post_meta,
    Column('menusection_id', Integer),
    Column('menusubsection_id', Integer),
)

menusection = Table('menusection', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('section_name', String(length=64)),
    Column('number_of_groups', Integer),
    Column('total_number_of_items', Integer),
    Column('visibility', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['section_to_subsection'].create()
    post_meta.tables['menusection'].columns['visibility'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['section_to_subsection'].drop()
    post_meta.tables['menusection'].columns['visibility'].drop()
