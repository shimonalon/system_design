"""FastAPI routes for URL Shortener API"""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from src.database import get_db
from src.cache import get_cache
from src.shortener import Base62Encoder, URLShortener
from src.models import URLRecord
from src.schemas import ShortenRequest, ShortenResponse, StatsResponse, ErrorResponse
from src.config import get_settings
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/api", tags=["urls"])


@router.post("/shorten", response_model=ShortenResponse, status_code=status.HTTP_201_CREATED)
async def shorten_url(
    request: ShortenRequest,
    session: Session = Depends(get_db().get_session),
):
    """
    Generate a short URL from a long URL.
    """
    # Validate long URL
    shortener = URLShortener(get_settings().BASE_URL)
    if not shortener.validate_long_url(request.long_url):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    # Insert into database (flush to get auto-incremented id)
    url_record = URLRecord(long_url=request.long_url, created_at=datetime.now(), short_code="temp")
    session.add(url_record)
    session.flush()

    # Generate short code from id
    short_code = Base62Encoder.encode(url_record.id)
    url_record.short_code = short_code
    session.commit()

    # Cache in Redis
    cache = get_cache(get_settings().REDIS_URL)
    await cache.set(short_code, request.long_url, ttl=get_settings().CACHE_TTL)

    # Return response
    return ShortenResponse(
        short_code=short_code,
        short_url=shortener.generate_short_url(short_code),
        created_at=url_record.created_at,
    )


@router.get("/{short_code}", status_code=status.HTTP_302_FOUND)
async def redirect_to_url(
    short_code: str,
    session: Session = Depends(get_db().get_session),
):
    """
    Redirect short code to original long URL.
    """
    cache = get_cache(get_settings().REDIS_URL)

    # Check Redis cache
    long_url = await cache.get(short_code)
    if long_url:
        # Increment click count in database
        url_record = session.query(URLRecord).filter_by(short_code=short_code).first()
        if url_record:
            url_record.click_count += 1
            session.commit()
        return RedirectResponse(url=long_url)

    # Query database
    url_record = session.query(URLRecord).filter_by(short_code=short_code).first()
    if not url_record:
        raise HTTPException(status_code=404, detail="Short code not found")

    # Check expiration
    if url_record.expires_at and url_record.expires_at < datetime.now():
        raise HTTPException(status_code=410, detail="URL expired")

    # Cache in Redis
    await cache.set(short_code, url_record.long_url, ttl=get_settings().CACHE_TTL)

    # Increment click count
    url_record.click_count += 1
    session.commit()

    # Redirect
    return RedirectResponse(url=url_record.long_url)


@router.get("/stats/{short_code}", response_model=StatsResponse)
async def get_stats(
    short_code: str,
    session: Session = Depends(get_db().get_session),
):
    """
    Get statistics for a short URL.
    """
    url_record = session.query(URLRecord).filter_by(short_code=short_code).first()
    if not url_record:
        raise HTTPException(status_code=404, detail="Short code not found")

    return StatsResponse(
        short_code=url_record.short_code,
        long_url=url_record.long_url,
        created_at=url_record.created_at,
        click_count=url_record.click_count,
    )


@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_url(
    short_code: str,
    session: Session = Depends(get_db().get_session),
):
    """
    Delete a shortened URL.
    """
    url_record = session.query(URLRecord).filter_by(short_code=short_code).first()
    if not url_record:
        raise HTTPException(status_code=404, detail="Short code not found")

    session.delete(url_record)
    session.commit()

    cache = get_cache(get_settings().REDIS_URL)
    await cache.delete(short_code)

    return
