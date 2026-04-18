"""Integration tests for API endpoints"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import create_app
from src.database import Base, Database
from src.config import get_settings


@pytest.fixture(scope="module")
def app():
    """Create a test FastAPI app."""
    return create_app()


@pytest.fixture(scope="module")
def client(app):
    """Create a test client."""
    with TestClient(app) as c:
        yield c


class TestHealthEndpoint:
    """Test GET /health endpoint"""

    def test_health_check(self, client):
        """Test that health check returns 200 with status healthy"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"

    def test_root_endpoint(self, client):
        """Test that root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data


class TestShortenEndpoint:
    """Test POST /api/shorten endpoint"""

    def test_shorten_valid_url(self, client):
        """Test shortening a valid URL returns 201 with short code"""
        response = client.post(
            "/api/shorten",
            json={"long_url": "https://www.example.com/very/long/path"},
        )
        assert response.status_code == 201
        data = response.json()
        assert "short_code" in data
        assert "short_url" in data
        assert "created_at" in data
        assert len(data["short_code"]) > 0

    def test_shorten_returns_different_codes(self, client):
        """Test that two different URLs get different short codes"""
        response1 = client.post(
            "/api/shorten",
            json={"long_url": "https://www.example.com/page1"},
        )
        response2 = client.post(
            "/api/shorten",
            json={"long_url": "https://www.example.com/page2"},
        )
        assert response1.status_code == 201
        assert response2.status_code == 201
        assert response1.json()["short_code"] != response2.json()["short_code"]

    def test_shorten_invalid_url(self, client):
        """Test that an invalid URL returns 400"""
        response = client.post(
            "/api/shorten",
            json={"long_url": "not a valid url"},
        )
        assert response.status_code == 400

    def test_shorten_ftp_url(self, client):
        """Test that FTP URLs are rejected"""
        response = client.post(
            "/api/shorten",
            json={"long_url": "ftp://example.com/file"},
        )
        assert response.status_code == 400

    def test_shorten_empty_url(self, client):
        """Test that empty URL returns 422 (Pydantic validation)"""
        response = client.post(
            "/api/shorten",
            json={"long_url": ""},
        )
        assert response.status_code == 422

    def test_shorten_missing_body(self, client):
        """Test that missing body returns 422"""
        response = client.post("/api/shorten")
        assert response.status_code == 422


class TestRedirectEndpoint:
    """Test GET /api/{short_code} endpoint"""

    def test_redirect_valid_code(self, client):
        """Test that a valid short code redirects to the original URL"""
        # Create a short URL
        original_url = "https://www.example.com/redirect-test"
        create_response = client.post(
            "/api/shorten",
            json={"long_url": original_url},
        )
        short_code = create_response.json()["short_code"]

        # Follow the redirect
        response = client.get(f"/api/{short_code}", follow_redirects=False)
        assert response.status_code == 302
        assert response.headers["location"] == original_url

    def test_redirect_increments_click_count(self, client):
        """Test that each redirect increments the click count"""
        # Create a short URL
        original_url = "https://www.example.com/click-test"
        create_response = client.post(
            "/api/shorten",
            json={"long_url": original_url},
        )
        short_code = create_response.json()["short_code"]

        # Redirect 3 times
        for _ in range(3):
            client.get(f"/api/{short_code}", follow_redirects=False)

        # Check stats
        stats_response = client.get(f"/api/stats/{short_code}")
        assert stats_response.status_code == 200
        assert stats_response.json()["click_count"] == 3

    def test_redirect_nonexistent_code(self, client):
        """Test that a nonexistent short code returns 404"""
        response = client.get("/api/nonexistent123", follow_redirects=False)
        assert response.status_code == 404


class TestStatsEndpoint:
    """Test GET /api/stats/{short_code} endpoint"""

    def test_stats_valid_code(self, client):
        """Test that stats for a valid code returns 200 with correct data"""
        # Create a short URL
        original_url = "https://www.example.com/stats-test"
        create_response = client.post(
            "/api/shorten",
            json={"long_url": original_url},
        )
        short_code = create_response.json()["short_code"]

        # Get stats
        response = client.get(f"/api/stats/{short_code}")
        assert response.status_code == 200
        data = response.json()
        assert data["short_code"] == short_code
        assert data["long_url"] == original_url
        assert data["click_count"] == 0
        assert "created_at" in data

    def test_stats_after_redirects(self, client):
        """Test that click count updates after redirects"""
        # Create a short URL
        original_url = "https://www.example.com/stats-clicks-test"
        create_response = client.post(
            "/api/shorten",
            json={"long_url": original_url},
        )
        short_code = create_response.json()["short_code"]

        # Redirect 5 times
        for _ in range(5):
            client.get(f"/api/{short_code}", follow_redirects=False)

        # Check stats
        response = client.get(f"/api/stats/{short_code}")
        assert response.status_code == 200
        assert response.json()["click_count"] == 5

    def test_stats_nonexistent_code(self, client):
        """Test that stats for a nonexistent code returns 404"""
        response = client.get("/api/stats/nonexistent123")
        assert response.status_code == 404


class TestDeleteEndpoint:
    """Test DELETE /api/{short_code} endpoint"""

    def test_delete_valid_code(self, client):
        """Test that deleting a valid short code returns 204"""
        # Create a short URL
        create_response = client.post(
            "/api/shorten",
            json={"long_url": "https://www.example.com/delete-test"},
        )
        short_code = create_response.json()["short_code"]

        # Delete it
        response = client.delete(f"/api/{short_code}")
        assert response.status_code == 204

        # Verify it's gone
        stats_response = client.get(f"/api/stats/{short_code}")
        assert stats_response.status_code == 404

    def test_delete_nonexistent_code(self, client):
        """Test that deleting a nonexistent code returns 404"""
        response = client.delete("/api/nonexistent123")
        assert response.status_code == 404
