As of version `2.1` EnduraBot centralized it's permissions checking to the contents of `data/permissions.json`.


``` json title="permissions.json"
{
    "editrole": [
        1426035365671731292
    ],
    "alert": [
        3456789012345678901
    ]
}
```

The keys (e.g `editrole`) are the programmatic function names of registered commands. The value of the key, being a JSON list, are role IDs authorized to use the command.

If a registered command does not have an entry in `permissions.json` EnduraBot will presume that anyone in the server may use it. Furthermore, any member on a server with the `Administrator` permission automatically passes all permissions checks.

To find the programmatic name for a command one may search the files in the `cogs` folder. Unless the entire file is dedicated to one command, generally, comments precede the code that registers a command.

Lets take a look at the `/about` command.

``` py title="user_cmds.py" hl_lines="6" linenums="90"
# --- COMMAND: /about ---

    @app_commands.command(name="about", description="Get information about EnduraBot.")
    @app_commands.check(check_permissions)
    @app_commands.guilds(GUILD_ID)
    async def about(self, interaction: discord.Interaction):
```

In the above case the programmatic name for the command is `about`. It is the name of the declared asynchronus function (`#!python async def`) following the decorator registering a Discord application command (`#!python @app_commands.command()`).

