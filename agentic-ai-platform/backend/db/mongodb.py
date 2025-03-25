"""
MongoDB connection and database access for the Agentic AI Platform.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class MongoDB:
    client: AsyncIOMotorClient = None
    db = None


mongodb = MongoDB()


async def connect_to_mongo():
    """Create database connection."""
    logger.info("Connecting to MongoDB...")

    try:
        mongodb.client = AsyncIOMotorClient(settings.MONGODB_URL)
        mongodb.db = mongodb.client[settings.MONGODB_DB_NAME]

        # Ping the database to verify connection
        await mongodb.client.admin.command("ping")

        logger.info("Connected to MongoDB")
    except ConnectionFailure as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close database connection."""
    if mongodb.client:
        logger.info("Closing MongoDB connection...")
        mongodb.client.close()
        logger.info("MongoDB connection closed")


def get_database():
    """Get MongoDB database instance."""
    return mongodb.db
