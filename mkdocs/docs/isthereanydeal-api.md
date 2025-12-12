# IsThereAnyDeal
The API documentation is at [https://docs.isthereanydeal.com/](https://docs.isthereanydeal.com/).

EnduraBot uses the following IsThereAnyDeal endpoints:

- `/games/lookup/v1` ([ItadGameSearchHandler](classes.md#itadgamesearchhandler))
- `/games/info/v2` ([ItadGameSearchHandler](classes.md#itadgamesearchhandler))
- `/games/prices/v3` ([ItadGameDealsHandler](classes.md#itadgamedealshandler))

The base URL for API calls to ITAD is `https://api.isthereanydeal.com`

## /games/lookup/v1
This endpoint requires the following URL query parameters be sent via an HTTP `GET` header:
```json
{"key": key, "title": title}
```

Where `key` is the ITAD API key and `title` is a string for a game to search for.

This endpoint returns the following:
```json
{
  "found": true,
  "game": {
    "id": "018d937f-3062-71ad-8549-0a24362a14ec",
    "slug": "human-fall-flat",
    "title": "Human: Fall Flat",
    "type": "game",
    "mature": false,
    "assets": {
      "boxart": "https://assets.isthereanydeal.com/018d937f-3062-71ad-8549-0a24362a14ec/boxart.jpg?t=1761756326",
      "banner145": "https://assets.isthereanydeal.com/018d937f-3062-71ad-8549-0a24362a14ec/banner145.jpg?t=1761756326",
      "banner300": "https://assets.isthereanydeal.com/018d937f-3062-71ad-8549-0a24362a14ec/banner300.jpg?t=1761756326",
      "banner400": "https://assets.isthereanydeal.com/018d937f-3062-71ad-8549-0a24362a14ec/banner400.jpg?t=1761756326",
      "banner600": "https://assets.isthereanydeal.com/018d937f-3062-71ad-8549-0a24362a14ec/banner600.jpg?t=1761756327"
    }
  }
}
```

The following is returned if the API key is determined to not exist or be invalid:
```json
{
  "status_code": 403,
  "reason_phrase": "Invalid or expired api key"
}
```

The following is returned if the API cannot find a game by the title given:
```json
{
  "found": false
}
```

## /games/info/v2
This endpoint requires the following URL query parameters be sent via an HTTP `GET` header:
```json
{"key": key, "id": id}
```
Where `key` is the ITAD API key and `id` is the UUID for an ITAD game.

This endpoint returns the following:
```json
{
  "id": "018d937f-3062-71ad-8549-0a24362a14ec",
  "slug": "human-fall-flat",
  "title": "Human: Fall Flat",
  "type": "game",
  "mature": false,
  "assets": {
    "boxart": "https://assets.isthereanydeal.com/018d937f-3062-71ad-8549-0a24362a14ec/boxart.jpg?t=1761756326",
    "banner145": "https://assets.isthereanydeal.com/018d937f-3062-71ad-8549-0a24362a14ec/banner145.jpg?t=1761756326",
    "banner300": "https://assets.isthereanydeal.com/018d937f-3062-71ad-8549-0a24362a14ec/banner300.jpg?t=1761756326",
    "banner400": "https://assets.isthereanydeal.com/018d937f-3062-71ad-8549-0a24362a14ec/banner400.jpg?t=1761756326",
    "banner600": "https://assets.isthereanydeal.com/018d937f-3062-71ad-8549-0a24362a14ec/banner600.jpg?t=1761756327"
  },
  "earlyAccess": false,
  "achievements": true,
  "tradingCards": true,
  "appid": 477160,
  "tags": [
    "Co-op",
    "Funny",
    "Puzzle",
    "Adventure",
    "Physics"
  ],
  "releaseDate": "2016-07-21",
  "developers": [
    {
      "id": 1115,
      "name": "No Brakes Games"
    }
  ],
  "publishers": [
    {
      "id": 77,
      "name": "Curve Games"
    },
    {
      "id": 701,
      "name": "Curve Digital"
    }
  ],
  "reviews": [
    {
      "score": 94,
      "source": "Steam",
      "count": 167213,
      "url": "https://store.steampowered.com/app/477160/"
    },
    {
      "score": 70,
      "source": "Metascore",
      "count": 21,
      "url": "https://metacritic.com/game/human-fall-flat/critic-reviews/?platform=pc"
    },
    {
      "score": 72,
      "source": "Metacritic User Score",
      "count": 310,
      "url": "https://metacritic.com/game/human-fall-flat/user-reviews/?platform=pc"
    },
    {
      "score": 68,
      "source": "OpenCritic",
      "count": 61,
      "url": "https://opencritic.com/game/2906/human-fall-flat"
    }
  ],
  "stats": {
    "rank": 316,
    "waitlisted": 5143,
    "collected": 28328
  },
  "players": {
    "recent": 479,
    "day": 1944,
    "week": 3126,
    "peak": 113147
  },
  "urls": {
    "game": "https://isthereanydeal.com/game/human-fall-flat/"
  }
}
```

The following is returned if the UUID cannot be found or is not valid:
```json
{
  "status_code": 500,
  "reason_phrase": "Internal Server Error"
}
```

The following is returned if the API key is determined to not exist or be invalid:
```json
{
  "status_code": 403,
  "reason_phrase": "Invalid or expired api key"
}
```

## /games/prices/v3
This endpoint requires the following URL query parameters be sent via an HTTP `POST` header:
```json
{"key": key}
```

`key` is the ITAD API key. There are also 2 relevant and optional parameters that can be added to this header:

- `capacity`: An integer representing the number of shops[^1] that ITAD should provide for each game.
- `deals`: A boolean. `False` will return data for every game in the list regardless of if a deal for the game exists. `True` will only return data for games with deals.

This endpoint *also requires* that the request body be given a list of ITAD game UUIDs. This is done by passing them into the `json=` parameter of `#!python requests.post()`.

The endpoint returns JSON structured like the example below *for each game*. `capacity` was set to `1` in the example for brevity.
```json
[
  {
    "id": "018d937f-3062-71ad-8549-0a24362a14ec",
    "historyLow": {
      "all": {
        "amount": 1.99,
        "amountInt": 199,
        "currency": "USD"
      },
      "y1": {
        "amount": 2.1,
        "amountInt": 210,
        "currency": "USD"
      },
      "m3": {
        "amount": 2.1,
        "amountInt": 210,
        "currency": "USD"
      }
    },
    "deals": [
      {
        "shop": {
          "id": 2,
          "name": "AllYouPlay"
        },
        "price": {
          "amount": 2.1,
          "amountInt": 210,
          "currency": "USD"
        },
        "regular": {
          "amount": 19.99,
          "amountInt": 1999,
          "currency": "USD"
        },
        "cut": 89,
        "voucher": null,
        "storeLow": {
          "amount": 2.07,
          "amountInt": 207,
          "currency": "USD"
        },
        "flag": "S",
        "drm": [
          {
            "id": 61,
            "name": "Steam"
          }
        ],
        "platforms": [
          {
            "id": 1,
            "name": "Windows"
          },
          {
            "id": 2,
            "name": "Mac"
          }
        ],
        "timestamp": "2025-10-27T14:41:35+01:00",
        "expiry": null,
        "url": "https://itad.link/0190025c-aac3-7229-b8cd-6537cc082ca3/"
      }
    ]
  }
]
```

The following is returned if the API key is determined to not exist or be invalid:
```json
{
  "status_code": 403,
  "reason_phrase": "Invalid or expired api key"
}
```

The following is returned if `deals` is set to `True` and no game UUIDs have deals:
```json
[]
```

The following is returned if *none* of the submitted UUIDs are valid:
```json
[]
```

If *any* UUID is valid all invalid UUIDs are ignored and valid UUIDs are returned as normal.


[^1]: The IsThereAnyDeal API calls a `shop` a provider of the game. Ergo, one shop might be `Steam`, another `GOG`, and so on.