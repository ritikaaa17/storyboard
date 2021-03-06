# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

"""task-links

Revision ID: 052
Revises: 051
Create Date: 2016-02-08 15:58:59.451550

"""

# revision identifiers, used by Alembic.
revision = '052'
down_revision = '051'


from alembic import op
import sqlalchemy as sa


def upgrade(active_plugins=None, options=None):

    op.add_column('tasks', sa.Column('link', sa.UnicodeText(), nullable=True))


def downgrade(active_plugins=None, options=None):

    op.drop_column('tasks', 'link')
