from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create FastAPI application."""

    auto_scraper = FastAPI(
        title="Auto Scraper API",
        description="Auto Scraper internal API",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
    )

    return auto_scraper


app = create_app()
