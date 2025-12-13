# IsThereAnyDeal game search handler class

This class is named `ItadGameSearchHandler` and is stored at `classes/itad_get_games_handler.py`.

The class object itself accepts an argument of `title`; a string value representing a title to query the IsThereAnyDeal API for.

When the class is initiated as an object an API chain is started. Endpoint `/games/lookup/v1` is sent the `title` and either reports that nothing is found *or* returns data, including the UUID of the `title`.

The UUID is then sent to endpoint `/games/info/v2` which either reports nothing was found *or* returns a variety of data that ITAD stores about the game. The data worthwhile to EnduraBot is then stored in class attributes.

### check_connection()
This method accepts no arguements.

This method sends a pre-defined payload to endpoint `/games/lookup/v1` to verify there is a valid connection to the API. It will return the `bool` value `False` if the connection failed and `True` if it succeeded.

### get_title()
This method accepts no arguements.

This method returns the title of the video game produced by the API.

### get_boxart()
This method accepts no arguements.

This method returns the URL to the boxart of the video game produced by the API.

### get_id()
This method accepts no arguements.

This method returns the internal ITAD UUID of the video game produced by the API.

### get_release_date()
This method accepts no arguements.

This method returns the release date produced by the ITAD API for the video game in `YYYY-MM-DD` format.

### get_publishers()
This method accepts no arguements.

This method returns a Python list of the publishers for the video game produced by the API.

### get_tags()
This method accepts no arguements.

This method returns a Python list of the video game genre and content tags produced by the API.