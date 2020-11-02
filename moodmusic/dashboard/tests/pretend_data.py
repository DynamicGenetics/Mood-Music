import json

INVALID_DATA = json.dumps(
    {
        "playlists": [
            {
                "name": "Test Data",
                "lastModifiedDate": "2020-01-18",
                "items": [
                    {
                        "track": {
                            "trackName": '"The Take Over, The Breaks Over"',
                            "artistName": "Fall Out Boy",
                            "albumName": "Infinity On High",
                        },
                        "episode": "null",
                        "localTrack": "null",
                    }
                ],
                "description": "null",
                "numberOfFollowers": 0,
            }
        ]
    }
)

VALID_DATA = json.dumps(
    [
        {
            "endTime": "2019-01-19 17:01",
            "artistName": "David Bowie",
            "trackName": "Heroes - 2017 Remaster",
            "msPlayed": 18982,
        },
        {
            "endTime": "2019-01-20 11:15",
            "artistName": "Fleetwood Mac",
            "trackName": "Landslide",
            "msPlayed": 199493,
        },
    ]
)
