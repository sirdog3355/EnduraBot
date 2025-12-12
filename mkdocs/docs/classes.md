EnduraBot uses various custom-made classes to enhance it's functionality. These are stored in `classes/`.

## DBBlacklist
This class is stored at `classes/db_blacklist_handler.py`.

When initiated a connection to the `endurabot.db` database is made and, if the table does not already exist, the `blacklist` table is created.

### check_status()
This method accepts the following arguements:

- `target_id`: The Discord ID of a member.

The method will return `True` if the member is blacklisted and `False` if they are not.

### add_user()
This method accepts the following arguements:

- `target_id`: The Discord ID of the member to blacklist.
- `mod_id`: The Discord ID of the member who performed the blacklisting.

The method will check if the `target_id` is in the blacklist and, if so, will raise a `ValueError`.

If no errors are raised the `target_id` will be blacklisted with the `mod_id` stored as the moderator who blacklisted them.

### remove_user()
This method accepts the following arguements:

- `target_id`: The Discord ID of a member.

The method will check if the `target_id` is in the blacklist and, if not, will raise a `ValueError`.

If no errors are raised the `target_id` will be removed from the blacklist.

## DBRGITGames
This class is stored at `classes/db_rgit_games_handler.py`.

When initiated a connection to the `endurabot.db` database is made and, if the table does not already exist, the `rgit_games` table is created.

### check_if_exists()
This method accepts the following arguements:

- `id`: The ITAD UUID of a game.

This method will return `not None` if the UUID is in the RGIT table and `False` if it is not.

### add_game()
!!! info
    The 150 row limit is due to the Discord embed 4096 character limit. Roughly more than 150 games may cause this to be exceeded when running `/rgit-list` due to the lack of pagination.

This method accepts the following arguements:

- `title`: The fancy title of a game.
- `game_id`: The ITAD UUID of a game.
- `user_id`: The Discord ID of a member.

This method will check if the `game_id` is already in the RGIT table and, if so, will raise a `ValueError`. It will also check if more than 150 rows exist in the table and, if so, raise a `RuntimeError`.

If no errors are raised the method will add the `title` and `game_id` to the RGIT table with the `user_id` set as the member who added the game.

### remove_game()
This method accepts the following arguements:

- `id`: The ITAD UUID of a game.

This method will check if the `game_id` is already in the table and, if not, will raise a `ValueError`.

If no errors are raised the method will remove the game by it's `game_id`.

### list_games()
This method accepts no arguements.

This method returns a Python list of all the fancy game titles in the RGIT table.

### get_ids()
This method accepts no arguements.

This method returns a Python list of all ITAD UUIDs in the RGIT table.

### get_ids_and_names()
This method accepts no arguements.

This method returns a Python list of dictionaries where the `key` is an ITAD UUID and the `value` is the fancy game title associated with the UUID.

## ItadGameSearchHandler
This class is stored at `classes/itad_get_games_handler.py`.

This class accepts the following arguements:

- `title`: A fancy game title.

When initiated the `title` is sent to the ITAD API to see if an associated game and it's UUID can be found. If the API token is not accepted it will raise a `TypeError`.

If the API does not return expected data, or indicates the game could not be found, the class will raise a `ValueError`.

If a found game's boxart or release date is not found the relevant attributes will be set to generic values.

When initialization completes the following class attributes are made available:

- `self.title`: The fancy title of the game found by the API.
- `self.id`: The ITAD UUID of the game found by the API.
- `self.boxart`: The URL to the boxart of the game found by the API.
- `self.release_date`: The release date in ISO format for the game found by the API.
- `self.publishers`: A Python list of the publishers of the game found by the API.
- `self.tags`: A Python list of the game tags for the game found by the API.

### check_connection()
This method accepts no arguements.

This method checks if a connection to the API can be successfully made. If the API returns back a `status_code` JSON object the method will raise a `KeyError`.

### get_title()
This method accepts no arguements.

This method returns the `self.title` attribute.

### get_boxart()
This method accepts no arguements.

This method returns the `self.boxart` attribute.

### get_id()
This method accepts no arguements.

This method returns the `self.id` attribute.

### get_release_data()
This method accepts no arguements.

This method returns the `self.release_date` attribute.

### get_publishers()
This method accepts no arguements.

This method returns the `self.publishers` attribute.

### get_tags()
This method accepts no arguements.

This method returns the `self.tags` attribute.

## ItadGameDealsHandler
This class is stored at `classes/itad_get_deals_handler.py`.

This class accepts the following arguements:

- `deals_list`: A Python list of ITAD UUIDs. Designed to accept the method [`get_ids()`](#get_ids) from [`DBRGITGames`](#dbrgitgames).

When initiated the `deals_list` is sent to the ITAD API. The API *should* send back a list of JSON objects which represent the games in the `deals_list` that have deals. If the API token is not accepted the class will raise a `TypeError`.

The API is instructed in the URL parameters to *only* return deals and *only* return a single `shop`[^1] object per deal.

When initialization completes the following class attributes are made available:

- `self.deals`: The JSON returned by the ITAD API of games with deals.
- `self.list_of_ids`: The `deals_list` argument received by the class.

### get_deals_by_cut()
This method accepts no arguement.

This method returns the first 25 JSON objects given by `self.deals` sorted in order from games with the highest percentage off to lowest percentage off.

### get_deals_by_price()
This method accepts no arguement.

This method returns the first 25 JSON objects given by `self.deals` sorted in order from lowest deal price to highest deal price.


[^1]: The IsThereAnyDeal API calls a `shop` a provider of the game. Ergo, one shop might be `Steam`, another `GOG`, and so on.