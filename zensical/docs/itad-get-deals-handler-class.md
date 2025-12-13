# IsThereAnyDeal game deals handler class

This class is named `ItadGameDealsHandler` and is stored at `classes/itad_get_deals_handler.py`.

The class object itself accepts an argument of `deals_list`; a Python list of internal ITAD game UUIDs to search for deals on.

When the class is initiated as an object an API call is made to endpoint `/games/prices/v3` with the `deals_list`. The deal data returned by the API, and the list of deals given to this class, are then stored in class attributes.

### check_connection()
This method accepts no arguements.

This method sends a pre-defined payload to endpoint `/games/prices/v3` to verify there is a valid connection to the API. It will return the `bool` value `False` if the connection failed and `True` if it succeeded.

### get_deals()
This method accepts no arguments.

This method processes the `deals_list` sent to the class and returns a new list of game objects. The method performs the following actions:

1.  It filters out any deals from blacklisted shops (per variable `blacklisted_itad_shops` at [`data/variables.json`](configuration.md#variables)).
2.  For each game, it sorts its remaining deals from the lowest price to the highest.
3.  It sorts the entire list of games based on the price of each game's new cheapest deal.

The returned list contains the full game objects, each with a filtered and sorted list of its available deals.