from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.routers.routes import router as main_route
from app.db.session import engine
from app.db.base import Base


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_application() -> FastAPI:
    ''' Configure, start and return the application '''

    ## Start FastApi App
    application = FastAPI(
        title="Vehicle locator",
        summary="A FastAPI backend service that tracks vehicles in real-time using the gpslogger application",
        version="0.0.1",
        contact={
            "name": "Usman Fawad",
            "email": "ufawad0@gmail.com",
        }
    )

    Instrumentator().instrument(application).expose(application)
    # Creating all database tables
    create_tables()
    ## Mapping api routes
    application.include_router(main_route, prefix="/app")


    ## Allow cors
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


app = get_application()
