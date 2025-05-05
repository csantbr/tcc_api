from mongodb_migrations.base import BaseMigration
from pymongo import ASCENDING


class Migration(BaseMigration):
    @property
    def problems(self):
        return self.db['problems']

    def upgrade(self):
        if 'users' not in self.db.list_collection_names():
            self.db.create_collection('users')

        if 'problems' not in self.db.list_collection_names():
            self.db.create_collection('problems')

        if 'submissions' not in self.db.list_collection_names():
            self.db.create_collection('submissions')

        self.problems.create_index(
            [
                ('name', ASCENDING),
                ('created_at', ASCENDING),
            ],
            name='ix_name_1_created_at_1',
        )

    def downgrade(self):
        self.db.drop_collection('users')
        self.db.drop_collection('problems')
        self.problems.drop_index('ix_name_1_created_at_1')
        self.db.drop_collection('submissions')
