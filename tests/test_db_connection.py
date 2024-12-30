import pytest
from core.database import mongo_client, async_client, db, get_collection

TEST_COLLECTION_NAME = "Doctors"


# Synchronous MongoDB Connection Test
def test_sync_db_connection():
    try:
        mongo_client.admin.command('ping')
        print("[PASS] Synchronous MongoDB connection successful")
    except Exception as e:
        pytest.fail(f"[FAIL] Synchronous MongoDB connection test failed: {e}")


# Asynchronous MongoDB Connection Test
@pytest.mark.asyncio
async def test_async_db_connection():
    try:
        await db.command('ping')
        print("[PASS] Asynchronous MongoDB connection successful")
    except Exception as e:
        pytest.fail(f"[FAIL] Asynchronous MongoDB connection test failed: {e}")


# Synchronous MongoDB Insertion Test
def test_sync_insert_record():
    collection = get_collection(TEST_COLLECTION_NAME)
    record = {"name": "Test User", "email": "testuser@example.com"}
    try:
        result = collection.insert_one(record)
        assert result.inserted_id is not None, "[FAIL] Record insertion failed in synchronous test"
        print("[PASS] Synchronous record insertion test passed")
    except Exception as e:
        pytest.fail(f"[FAIL] Synchronous record insertion test failed: {e}")
    finally:
        collection.delete_one({"_id": result.inserted_id})


# Asynchronous MongoDB Insertion Test
@pytest.mark.asyncio
async def test_async_insert_record():
    collection = db[TEST_COLLECTION_NAME]
    record = {"name": "Async Test User", "email": "asynctestuser@example.com"}
    try:
        result = await collection.insert_one(record)
        assert result.inserted_id is not None, "[FAIL] Record insertion failed in asynchronous test"
        print("[PASS] Asynchronous record insertion test passed")
    except Exception as e:
        pytest.fail(f"[FAIL] Asynchronous record insertion test failed: {e}")
    finally:
        await collection.delete_one({"_id": result.inserted_id})
