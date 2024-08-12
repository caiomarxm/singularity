import logging
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from singularity.database.engine import get_session

from singularity.database.bootstrap_db import bootstrap_db_defaults


if __name__ == "__main__":
    logging.info("Creating initial data")
    session = next(get_session())
    bootstrap_db_defaults(session=session)
    logging.info("Initial data created")
