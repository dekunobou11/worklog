class Memo:
    def __init__(self, row):
        self.id = row['id']
        self.user_id = row['user_id']
        self.content = row['content']
        self.tag = row['tag']
        self.image = row['image']
        self.created_at = row['created_at']

    @staticmethod
    def from_db_row(row):
        return Memo(row) if row else None