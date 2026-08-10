from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

# Configure standard industry logging
logger = logging.getLogger(__name__)

class DatabaseService:
    @staticmethod
    def check_connection(db: Session) -> int:
        """
        Attempts to run a lightweight query to verify database connectivity.
        Fails fast and raises an exception if the DB is unreachable.
        """
        try:
            result = db.execute(text("SELECT 1")).fetchone()
            if not result:
                raise ValueError("Database returned an empty result set.")
            return result[0]
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            raise e