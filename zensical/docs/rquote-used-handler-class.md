This class is named `RquoteUsed` and is stored at `classes/db_rquote_used_handler.py`.

When initiated a connection to the `endurabot.db` database is made and, if the table does not already exist, the `rquote_used` table is created.

### check_status()
This method accepts the following arguements:

- `msg_id`: The message ID of a Discord message.

The method will return the `bool` value `True` if the message is in the table and `False` if it is not.

### get_row_count()
This method does not accept arguments.

The method will return the number of rows in the `rquote_used` table as an `int` value.

### delete_oldest_row()
This method does not accept arguments.

The method will delete the row in the `rquote_used` table with the smallest autoincrementing ID.

### add_msg()
This method accepts the following arguements:

- `msg_id`: The message ID of a Discord message.

The method will add the `msg_id` to the `rquote_used` table *and* if `get_row_count()` returns a value that meets or exceeds the [configuration variable](configuration.md#variables) `max_old_quotes` this method will run `delete_oldest_row()`.