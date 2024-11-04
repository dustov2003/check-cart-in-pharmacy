from logging import getLogger

from fastapi import FastAPI
from uvicorn import run

from pharmacy_cart_checker.config import get_settings
from pharmacy_cart_checker.endpoints import list_of_routes
from pharmacy_cart_checker.utils import get_hostname


logger = getLogger(__name__)


def bind_routes(application: FastAPI) -> None:
    """
    Bind all routes to application.
    """

    for route in list_of_routes:
        application.include_router(route)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Микросервис, реализующий возможность укорачивать ссылки."

    tags_metadata = [
        {
            "name": "Check",
        },
    ]

    application = FastAPI(
        title="Pharmacy's cart checker",
        description=description,
        tags_metadata=tags_metadata,
        openapi_url="/openapi",
        version="1.0.0",
    )

    bind_routes(application)

    return application


app = get_app()

if __name__ == "__main__":
    settings_for_application = get_settings()
    run(
        "pharmacy_cart_checker.__main__:app",
        host=get_hostname(settings_for_application.APP_HOST),
        port=settings_for_application.APP_PORT,
        reload=True,
        reload_dirs=["./pharmacy_cart_checker"],
        log_level="debug",
    )
