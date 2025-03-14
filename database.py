import pymongo
import logging
from config import Config
from pymongo.errors import OperationFailure

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(Config.DATABASE_URL)
        self.db = self.client["FileIndexer"]
        self.files = self.db["files"]
        self._create_indexes()

    def _create_indexes(self):
        try:
            self.files.create_index(
                [("file_name", "text"), ("caption", "text")],
                name="search_index",
                weights={"file_name": 2, "caption": 1}
            )
        except OperationFailure as e:
            logger.error(f"Index creation error: {e}")

    def save_file(self, file_data):
        try:
            self.files.update_one(
                {'file_id': file_data['file_id']},
                {'$set': file_data},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Save file error: {e}")
            return False

    def search_files(self, query, page=1):
        try:
            skip = (page - 1) * Config.RESULTS_PER_PAGE
            return list(self.files.find(
                {'$text': {'$search': query}},
                {'score': {'$meta': 'textScore'}}
            ).sort([('score', {'$meta': 'textScore'})])
            .skip(skip)
            .limit(Config.RESULTS_PER_PAGE))
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []

    def get_total_results(self, query):
        try:
            return self.files.count_documents(
                {'$text': {'$search': query}}
            )
        except Exception as e:
            logger.error(f"Count error: {e}")
            return 0

db = Database()
