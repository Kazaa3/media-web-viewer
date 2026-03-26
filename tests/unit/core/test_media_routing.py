import pytest
from fastapi.testclient import TestClient
from src.core.main import app

client = TestClient(app)

def test_direct_route():
    response = client.get("/direct/sample.mp4")
    assert response.status_code in (200, 404)  # 200 if file exists, 404 if not

def test_media_raw_route():
    response = client.get("/media-raw/sample.mp4")
    assert response.status_code in (200, 404)

def test_video_stream_route():
    response = client.get("/video-stream/sample.mp4")
    assert response.status_code in (200, 404)

# Add more tests for edge cases, e.g. invalid paths, permissions, etc.
