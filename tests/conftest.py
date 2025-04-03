import pytest
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from main import app
from src.models import Base
from src.database_manager import DatabaseManager
from src.logger import setup_logger
from src.settings import LOG_FILE_TEST

# Logger configuration
logger = setup_logger("testing")

@pytest.fixture(scope="module")
def postgres_container():
    container = PostgresContainer("postgres:17.4")
    container.start()
    yield container
    try:
        container.stop()
    except Exception as e:
        logger.info(f"Error stopping container: {e}")
        # Try force removal if needed
        try:
            container.get_wrapped_container().remove(force=True)
        except Exception as e:
            logger.error(f"Error forcing removal: {e}")

@pytest.fixture(scope="module")
def test_db(postgres_container):
    test_db_url = postgres_container.get_connection_url()
    engine = create_engine(test_db_url)
    Base.metadata.create_all(bind=engine)
    
    # Insert basic test data
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO pricing_data (sku, product_family) 
            VALUES ('KDWMVZSTP4QSAE5G', 'test_family'),
                   ('TEST-SKU-DELETE', 'delete_family')
            ON CONFLICT DO NOTHING
        """))
        conn.commit()
    
    return engine

@pytest.fixture(scope="module")
def test_client(test_db):
    TestingSessionLocal = sessionmaker(bind=test_db)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[DatabaseManager().get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()