EnduraBot has Python files colloquially called "listeners" located at `listeners/`; files with code that primarily react to events provided by the Discord API.

## Alert detection
One of EnduraBot's commands is `/alert`; a command which sends a structured ping to technical staff regarding an issue with services they oversee.

Given the low-population of the server this bot was created to monitor, simply advising members the command exists (even though that was also done) made no gaurantee it would be used.

To enforce use, `listeners/alert_detect.py` was made with a function that listens to all messages submitted on the server. It looks for 3 criteria:

1. Is the message pinging the role defined at `data/variables.json` as the `sysop_role_id`?
2. Does the message contain atleast 1 word defined at `data/misc_text.json` under the `server_identifiers` key?
3. Does the message contain atleast 1 word defined at `data/misc_text.json` under the `issue_identifiers` key?

If *all 3* criteria are true EnduraBot will delete the relevant message and replace it with an embed advising the user to use `/alert`.

Messages that ping the `sysop_role_id` by someone who *has* the `sysop_role_id` do not trigger the listener.

## Bot insults
As a funny feature `listeners/bot_insult.py` was made to listen for any time a person pings the bot.

If someone pings the bot it will generate a random float between `0` and `1`. If the generated float is less than or equal to the value set at `data/variables.json` as `bot_insult_chance` the bot will insult the user. Insults are held at `data/misc_text.json` under the `bot_insults` key.

## Invite tracking
As administrative utilities `listeners/invites_creation.py` and `listeners/invites_use.py` were made.

`invites_creation.py` simply listens to new `on_invite_create` events and logs to `logs/endurabot.log` everytime an invite is made, the code generated, and who made it.

`invites_use` is a more sophisticated listener which monitors all the invites and their use-count. It then listens to new `on_member_join` events.

When it detects that someone joins it looks to see which invite's use count increased. It then determines that such an invite was the one the new member just used. With this information it logs to `logs/endurabot.log` that a person joined the server, that the new person used the detected invite code, then it logs the original creator of the invite and when the invite was originally made.
