# Temporary Role (/trole) Breakdown

`/trole` is a command that gives a role to a user for a specified duration.

## Command logic breakdown
!!! info
    Astute readers may notice that `#!python int()` and `#!python str()` are used more frequently than should be necessary. 
    
    This is because SQLITE columns with the `int` or `numeric` data type round up automatically if the number is too large. *All* Discord IDs are too large. This obviously causes issues. To get around this, relevant columns are passed the IDs as strings. `#!python int()` and `#!python str()` are used in situations where the relevant function requires said data type.

Below is an abbreviated breakdown of how `/trole` works programmatically.

At the top of the file we import the [`DBTempRole`](trole-handler-class.md) class and set it to variable `db_temp_role`.

```py title="temp_role.py"
from classes.db_trole_handler import DBTempRole

# ...

db_temp_role = DBTempRole()
```

Then, we use a `for` loop to dynamically generate the list of roles that can be selected. This is sourced from the `mod_editable_roles` variable of [`data/variables.json`](configuration.md#variables).

```py title="temp_role.py"
role_list = SETTINGS_DATA["mod_editable_roles"]
    options_list = []
    for role_name, role_id in role_list.items():
        #Because role ID numbers are so long, it's interpreted as being too big an integer and causes Discord to crash spectacularly.
        #So need to make it a string using an f-string.
        options_list.append(app_commands.Choice(name=role_name,value=f"{role_id}"))
```

We then register the command.
```py title="temp_role.py"
@app_commands.command(name="trole", description="Give a user a role temporarily.")
@app_commands.check(check_permissions)
@app_commands.guilds(GUILD_ID)
@app_commands.choices(roles=options_list)
@app_commands.describe(
    target = "Who is the target?",
    length = "Length, in hours, the role should last for. (default: 24)",
    roles = f"Which role should be given to the target? (default: {options_list[0].name})",
    disconnect = "Should the target be disconnected from VC? (default: True)",
    check = "If true, will ONLY be told if there's an active timer for the target.",
    remove = "If true, will ONLY remove the temp role and delete timer for target."
)
async def trole(self, interaction: discord.Interaction, target: discord.Member, roles: str = options_list[0].value, length: int = 24, check: bool = False, remove: bool = False, disconnect: bool = True):
```
`#!python @app_commands.check(check_permissions)` runs a custom function defined at `utils/permissions_checker.py` to ensure a person using the command is allowed to do so. This is added to *every* command in EnduraBot.

`#!python  @app_commands.choices(roles=options_list)` is what actually registers the options for the `roles` argument.

`#!python  @app_commands.describe()` is what sets the descriptions for all the command arguements.

Then, the command immediately defers the output:

```py title="temp_role.py"
await interaction.response.defer(ephemeral=True)
```

By default, Discord demands a bot respond to a query sent to it within 3 seconds. Deferring is what generates the `<bot> is thinking...` text and allows the bot to take *minutes* to respond. This is done because in certain situations EnduraBot needs more than 3 seconds to get it's ducklings in a row.

We then set a lot of variables for use in the lines to come.

```py title="temp_role.py"
role = interaction.guild.get_role(int(roles))
general_chat = self.bot.get_channel(SETTINGS_DATA["based_chat_channel_id"])
timestamp_equation = datetime.datetime.now() + timedelta(hours=length)
timestamp = timestamp_equation.replace(microsecond=0)
timestamp_fancy = timestamp.strftime("%B %d, %Y %H:%M")
epoch = round(timestamp_equation.timestamp())
```

Moving on: the bot then checks if the boolean arguements of `check` or `remove` are set to `True`.

If `check` is set to `True`, the command just echoes if the target has a temporary role and, if so, provides all relevant information. The command then stops there.

```py title="temp_role.py" linenums="1"
if check == True:
    if db_temp_role.check_status(str(target.id)) == False:
        await interaction.followup.send(f"<@{target.id}> does not have a temporary role.", ephemeral=True)
        logger.info(f"{interaction.user.name} ({interaction.user.id}) checked if {target.name} ({target.id}) has a temporary role. [FALSE]")
        return
    else:
        timestamp = db_temp_role.check_time(str(target.id))
        mod_id =  db_temp_role.get_mod(str(target.id))
        role_id = db_temp_role.get_role(str(target.id))
        role_name = interaction.guild.get_role(int(role_id)).name
        await interaction.followup.send(f"<@{mod_id}> gave <@&{role_id}> to <@{target.id}>. It is set to be removed <t:{timestamp}:f> (<t:{timestamp}:R>)", ephemeral=True)
        logger.info(f"{interaction.user.name} ({interaction.user.id}) checked if {target.name} ({target.id}) has a temporary role. [TRUE] [@{role_name}]")
        return
```

If `remove` is set to `True`, the command removes the temporary role entry from the SQLITE database and removes the relevant temporary role. The command then stops there.

```py title="temp_role.py"
if remove == True:
    if db_temp_role.check_status(str(target.id)) == False:
        await interaction.followup.send(f"<@{target.id}> does not have a temporary role.", ephemeral=True)
        logger.info(f"{interaction.user.name} ({interaction.user.id}) attempted to remove a temporary role from {target.name} ({target.id}) when they did not have one.")
        return
    else:
        role_to_remove = interaction.guild.get_role(int(db_temp_role.get_role(str(target.id))))
        role_name = role_to_remove.name
        await target.remove_roles(role_to_remove)
        await interaction.followup.send(f"<@{target.id}>'s temporary role successfully removed.", ephemeral=True)
        logger.info(f"{interaction.user.name} ({interaction.user.id}) removed the temporary role [@{role_name}] for {target.name} ({target.id}) early.")
        db_temp_role.remove_user_by_id(str(target.id))
        return
```

Following the above, 2 quick checks are performed to rule out edge cases. In this case, first, because it's unnecessary and can cause confusion, `/trole` stops itself from targetting bots. Second, if the `length` provided is equal to or less than `0`, the bot echoes a sarcastic message.

```py title="temp_role.py"
if target.bot:
    await interaction.followup.send("Bots may not be given a temporary role.", ephemeral=True)
    logger.log(UNAUTHORIZED, f"{interaction.user.name} ({interaction.user.id}) tried to give a temporary role to bot {target.name} ({target.id}).")
    return

if length <= 0:
    await interaction.followup.send("Hilarious.", ephemeral=True)
    return
```

Because the bot needs to be able to handle being ran multiple times on the same user, even if they have an existing temporary role, the bot checks to see if the target has an entry in the database.

If true, the bot replaces the role they were given previously with the role selected by the user. 

If false, the bot tries to add the role selected by the user. If the target already has it for some reason (e.g `/editrole` was used, which is permanent, or a user with native permissions did so manually), Discord gracefully does nothing.

```py title="temp_role.py"
if db_temp_role.check_status(str(target.id)) == True:

    db_role = interaction.guild.get_role(int(db_temp_role.get_role(str(target.id))))
    new_role = role

    if not new_role in target.roles:
        await target.remove_roles(db_role)
        await target.add_roles(new_role)

else:

    await target.add_roles(role)
```

We now add the target to the SQLITE database table. The [`add_user()`](trole-handler-class.md#add_user) method already handles checking if the target has an existing entry, so a check *here* is unnecessary.

```py title="temp_role.py"
db_temp_role.add_user(target.id, target.name, interaction.user.id, interaction.user.name, roles, timestamp)
```

The bot then checks if the target is in a VC at the time the command is ran. If so, *and* the `disconnect` arguement is set to `True`, they are disconnected.

```py title="temp_role.py"
if target.voice and disconnect == True:
    await target.move_to(None)
```

The embeds are now constructed; one for the person who ran the command (`embed_executor`) and the public one being sent to the configured channel (`embed_notification_public`).

```py title="temp_role.py"
embed_executor = discord.Embed(
    title="Action successful.",
    description=f"<@{target.id}> given <@&{roles}>.\n\n If you would like to remove the role early use the remove argument in `/trole`.\n\n Running the command again will result in resetting the timer and replacing the temporary role with whatever the new selection is.",
    color=3800852)

embed_notification_public = discord.Embed(
title=f"You have been given a temporary role.",
description=f"<@{interaction.user.id}> has given you the role `@{role.name}`.\n\n The date and time below is when the role will be removed automatically. Note that the removal time may be off by upto 2-5 minutes.",
color=15277667)
embed_notification_public.add_field(name="Automatic Removal Time", value=f"<t:{epoch}:f> (<t:{epoch}:R>)", inline=False)
```

The embeds are then sent and the command execution is logged.

```py title="temp_role.py"
await general_chat.send(embed=embed_notification_public, content=f"<@{target.id}>", allowed_mentions=self.default_allowed_mentions)

logger.info(f"{interaction.user.name} ({interaction.user.id}) gave [@{role.name}] to {target.name} ({target.id}) for {length} hour(s). Removal scheduled for {timestamp_fancy}.")
await interaction.followup.send(embed=embed_executor, ephemeral=True)
```

## Task breakdown
The task `tasks/temp_role_monitor.py` works in conjunction with `/trole` to ensure that temporary roles are removed on time. The following is a brief breakdown of the task itself.

So, first, like with the command, we import the [`DBTempRole`](trole-handler-class.md) class and set it to variable `temp_role`.

```py title="temp_role_monitor.py"
from classes.db_trole_handler import DBTempRole

# ...

temp_role = DBTempRole()
```

We then use a decorator to register the code about to be described as needing to run every minute.

```py title="temp_role_monitor.py"
@tasks.loop(minutes=1)
```

Following that, we assign variable `timestamps` as a Python list of timestamps representing still active temporary role entries. This is derived from method [`get_timestamps()`](trole-handler-class.md#get_timestamps) which returns a Python list.

```py title="temp_role_monitor.py"
timestamps = temp_role.get_timestamps()
```

A `for` loop is now initiated which runs for each timestamp. We begin by checking to see if the timestamp is *older* than whatever the time is *now*.

```py title="temp_role_monitor.py"
for timestamp in timestamps:
    if datetime.now() > timestamp:
```

If so, we assign some necessary variables. Because we don't have an `interaction` object to easily derive user and role information from, we have to instead derive them by passing various information stored in the database to methods in `self.guild`.

```py title="temp_role_monitor.py"
user = self.guild.get_member(
    int(temp_role.get_user_id_by_timestamp(timestamp))
)
role = self.guild.get_role(int(temp_role.get_role_by_timestamp(timestamp)))
```

Finally, if they still have their temporary role, it is removed, their entry in the database is removed, and then a log is made of the action. If they *don't* have the temporary role anymore, we still delete their entry in the database, and the log transparently reports that the role was removed abnormally.

```py title="temp_role_monitor.py"
if role in user.roles:
    await user.remove_roles(role)
    logger.info(
        f"{temp_role.get_user_name_by_timestamp(timestamp)} ({temp_role.get_user_id_by_timestamp(timestamp)}) was given [@{role.name}] temporarily and the duration has ended. Role removed and status removed from database."
    )
    temp_role.remove_user_by_timestamp(timestamp)
else:
    logger.info(
        f"{temp_role.get_user_name_by_timestamp(timestamp)} ({temp_role.get_user_id_by_timestamp(timestamp)}) was given [@{role.name}] temporarily and the duration has ended. Role detected to have been removed early. Removed status from database."
    )
    temp_role.remove_user_by_timestamp(timestamp)
```


