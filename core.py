import logging
import os
from typing import Dict, List

import spotipy
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger(__name__)


def init_spotify_client() -> spotipy.Spotify:
    """Initialize and return an authenticated Spotify client.

    The client is authorized using credentials provided via environment variables:
    ``SPOTIFY_CLIENT_ID`` and ``SPOTIFY_CLIENT_SECRET`` must be set. The optional
    ``SPOTIFY_REDIRECT_URI`` variable may override the default local callback.
    
    Returns
    -------
    spotipy.Spotify
        Authenticated Spotify client instance.
    """
    scopes = [
        "playlist-read-private",
        "playlist-read-collaborative",
        "user-library-read",
    ]
    auth_manager = SpotifyOAuth(
        scope=scopes,
        client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
        client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.environ.get(
            "SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback"
        ),
        open_browser=False,
    )
    logger.debug("Spotify auth scopes: %s", scopes)
    client = spotipy.Spotify(auth_manager=auth_manager)
    logger.info("Spotify client initialised")
    return client


def fetch_user_playlists(sp: spotipy.Spotify) -> List[Dict[str, object]]:
    """Fetch all playlists for the current user.

    Parameters
    ----------
    sp:
        Authenticated Spotipy client.

    Returns
    -------
    list[dict[str, object]]
        Each playlist entry contains ``id``, ``name`` and ``track_total`` keys.
    """
    playlists: List[Dict[str, object]] = []
    offset = 0
    while True:
        response = sp.current_user_playlists(limit=50, offset=offset)
        logger.debug(
            "Fetched %d playlists at offset %d", len(response.get("items", [])), offset
        )
        for item in response.get("items", []):
            playlists.append(
                {
                    "id": item["id"],
                    "name": item["name"],
                    "track_total": item["tracks"]["total"],
                }
            )
        if response.get("next"):
            offset += len(response.get("items", []))
        else:
            break
    logger.info("Total playlists fetched: %d", len(playlists))
    return playlists
