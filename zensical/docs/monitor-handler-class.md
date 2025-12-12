This class is named `DBMonitor` and is stored at `classes/db_monitor_handler.py`.

When initiated a connection to the `endurabot.db` database is made and, if the table does not already exist, the `member_monitor` table is created.

### check_status()
This method accepts the following arguements:

- `target_id`: The Discord ID of a member.

The method will return the `bool` value `True` if the member is being monitored and `False` if they are not.

### add_user()
!!! info
    EnduraBot expects `level` to either be `alert` or `ban`. If any other value is passed EnduraBot will treat the target as being level `alert`.

This method accepts the following arguements:

- `target_name`: The name of the person to be monitored.
- `target_disc_id`: The Discord ID of the person to be monitored.
- `target_steam_id`: The Steam ID x64[^1] of the person to be monitored.
- `mod_name`: The name of the person adding the target.
- `mod_disc_id`: The Discord ID of the person adding the target.
- `reason`: The reason why the target is being monitored.
- `level`: Whether EnduraBot should react to target joining by only alerting (`alert`) or alerting and banning (`ban`).

The method does not return data.

### remove_user()
This method accepts the following arguements:

- `target_id`: The Discord ID of a member.

This method does not return data.

### get_steamid()
This method accepts the following arguements:

- `target_id`: The Discord ID of a member.

This method returns the Steam ID of the target as a string.

### get_mod_name()
This method accepts the following arguements:

- `target_id`: The Discord ID of a member.

This method returns the name of the person who added the target for monitoring as a string.

### get_mod_id()
This method accepts the following arguements:

- `target_id`: The Discord ID of a member.

This method returns the Discord ID of the person who added the target for monitoring as a string.

### get_reason()
This method accepts the following arguements:

- `target_id`: The Discord ID of a member.

This method returns the reason for why the target was monitored as a string.

### get_timestamp()
This method accepts the following arguements:

- `target_id`: The Discord ID of a member.

This method returns the timestamp of when the target was set for monitoring as a string.

[^1]: Should look like `76561198055926520` and not `STEAM_0:0:47830396`.