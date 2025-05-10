import logging

from fastapi import FastAPI

from .routes import api_router
from .config.logger import configure_logging


configure_logging()

logger = logging.getLogger(__name__)

api_server = FastAPI(
    description='Proyecto Fast-Movies.. solo con fines educativos',
    version='0.0.0',
    title='Fast-Movies',
)

api_server.include_router(api_router)
logger.info('Inicio de la API')
