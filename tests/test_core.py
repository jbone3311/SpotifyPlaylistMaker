from unittest.mock import MagicMock
import core


def test_fetch_user_playlists_paging():
    client = MagicMock()
    client.current_user_playlists.side_effect = [
        {
            "items": [
                {"id": "1", "name": "A", "tracks": {"total": 10}},
            ],
            "next": "next",
        },
        {
            "items": [
                {"id": "2", "name": "B", "tracks": {"total": 20}},
            ],
            "next": None,
        },
    ]

    playlists = core.fetch_user_playlists(client)
    assert playlists == [
        {"id": "1", "name": "A", "track_total": 10},
        {"id": "2", "name": "B", "track_total": 20},
    ]
