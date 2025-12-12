This class is named `DBTempRole` and is stored at `classes/db_trole_handler.py`.

When initiated a connection to the `endurabot.db` database is made and, if the table does not already exist, the `temp_roles` table is created.

### check_status()
This method accepts the following arguements:

- `target_id`: The Discord ID of the target.

The method will return the `bool` value `True` if the member has a temporary role and `False` if they don't.

### add_user()
This method accepts the following arguements:

- `target_id`: The Discord ID of the target.
- `target_name`: The name of the target.
- `mod_id`: The Discord ID of the person giving the temporary role.
- `mod_name`: The name of the person giving the temporary role.
- `role_id`: The ID of the role given to the target.
- `timestamp`: The timestamp for when the temporary role should be removed.

This method will add an entry of the target being given a temporary role.

### remove_user_by_timestamp()
This method accepts the following arguements:

- `timestamp`: The timestamp for when the temporary role should be removed.

This method will delete a row in `temp_roles` by the `timestamp`; used by `tasks/temp_role_monitor.py`.

### remove_user_by_id()
This method accepts the following arguements:

- `target_id`: The Discord ID of the target.

This method will delete a row in `temp_roles` by the `target_id`.

### get_user_name_by_timestamp()
This method accepts the following arguements:

- `timestamp`: The timestamp for when the temporary role should be removed.

This method will return the name of the target by the `timestamp` as a string; used by `tasks/temp_role_monitor.py`.

### get_mod()
This method accepts the following arguements:

- `target_id`: The Discord ID of the target.

This method will return the Discord ID of the person who gave the `target_id` a temporary role.

### get_role()
This method accepts the following arguements:

- `target_id`: The Discord ID of the target.

This method will return the role ID of the role that `target_id` was given.

### get_role_by_timestamp()
This method is identical to [`get_role()`](#get_role) but accepts a `timestamp` instead of `target_id`; used by `tasks/temp_role_monitor.py`.

### check_time()
This method accepts the following arguements:

- `target_id`: The Discord ID of the target.

This method will return the timestamp for when the temporary role should be removed in [Unix time](https://en.wikipedia.org/wiki/Unix_time).

### get_timestamps()
This method accepts no arguments.

This method will return a Python list of all timestamps in `temp_roles`.