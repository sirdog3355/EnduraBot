This class is named `DBBlacklist` and is stored at `classes/db_blacklist_handler.py`.

When initiated a connection to the `endurabot.db` database is made and, if the table does not already exist, the `blacklist` table is created.

### check_status()
This method accepts the following arguements:

- `target_id`: The Discord ID of a member.

The method will return the `bool` value `True` if the member is blacklisted and `False` if they are not.

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