import os
import sys
import pytest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.youtube import get_youtube_url

@pytest.mark.parametrize(
    "track,expected_in_url",
    [
        ({"artist": "Aphex Twin", "title": "Avril 14th"}, "youtube.com"),
        ({"artist": "Radiohead", "title": "Karma Police"}, "youtube.com"),
        ({"artist": "Daft Punk", "title": "Harder Better Faster Stronger"}, "youtube.com"),
    ]
)
def test_get_youtube_url_valid(track, expected_in_url):
    url = get_youtube_url(track)
    assert isinstance(url, str)
    assert expected_in_url in url
    assert url.startswith("http")

def test_get_youtube_url_missing_artist():
    track = {"title": "Imagine"}
    url = get_youtube_url(track)
    assert isinstance(url, str)
    assert "youtube.com" in url

def test_get_youtube_url_missing_title():
    track = {"artist": "John Lennon"}
    url = get_youtube_url(track)
    assert isinstance(url, str)
    assert "youtube.com" in url

def test_get_youtube_url_empty_track():
    track = {}
    url = get_youtube_url(track)
    assert isinstance(url, str)
    assert "youtube.com" in url

def test_get_youtube_url_none_track():
    with pytest.raises(Exception):
        get_youtube_url(None)