class User:
    def __init__(self, row):
        self.id = row['id']
        self.username = row['username']
        self.password = row['password']

    @staticmethod
    def from_db_row(row):
        return User(row) if row else None