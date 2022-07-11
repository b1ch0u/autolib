"""Insert 10 cars

Revision ID: ac457cf86898
Revises: 5c7b1266a316
Create Date: 2022-07-10 21:14:32.395931

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import select


# revision identifiers, used by Alembic.
revision = 'ac457cf86898'
down_revision = '5c7b1266a316'
branch_labels = None
depends_on = None


car_models = sa.table(
    'car_models',
    sa.Column('id', sa.Integer),
    sa.Column('name', sa.String),
    sa.Column('seats', sa.Integer),
)


cars = sa.table(
    'cars',
    sa.Column('id', sa.Integer),
    sa.Column('x', sa.Integer),
    sa.Column('y', sa.Integer),
    sa.Column('model_id', sa.Integer),
)


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(car_models.insert().values(
        [
            {'name': 'Renaul Clio 5', 'seats': 5}
        ]
    ))
    model_id = conn.execute('select id from car_models').first()[0]
    op.bulk_insert(
        cars,
        [
            {'x': 0, 'y': 0, 'model_id': model_id}
        ] * 10
    )


def downgrade() -> None:
    op.execute('delete from cars')
    op.execute('delete from car_models')
