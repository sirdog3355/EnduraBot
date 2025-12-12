EnduraBot's code is organized as follows:

| Folder      | Purpose                          |
| ----------- | ------------------------------------ |
| `classes`       | Contains classes used by EnduraBot.  |
| `cogs` | Contains EnduraBot's commands. |
| `data` | Contains configuration files. |
| `listeners` | Contains files that perform actions based on "listening" to various Discord API triggers (e.g `on_message`). |
| `logs` | Contains EnduraBot's logs. |
| `mkdocs` | Contains the raw content of EnduraBot's documentation. |
| `tasks` | Contains files that perform actions at set times or in set intervals. |
| `utils` | Contains files that provide utilities to EnduraBot's functioning. |

## Classes
Each class is documented on it's own page. See the left sidebar. You may need to scroll down.

## Cogs
| File      | Purpose                          |
| ----------- | ------------------------------------ |
| `blacklist.py` | Houses the code for `/blacklist`. |
| `edit_role.py` | Houses the code for `/editrole`. |
| `game_cmd.py` | Houses the code for `/game`. |
| `monitor.py` | Houses the code for `/monitor`. |
| `rquote.py` | Houses the code for `/rquote` and `/rquote-debug`. |
| `temp_role.py` | Houses the code for `/trole`. |
| `user_cmds.py` | Houses the code for multiple commands; usually because their complexity is low and/or organizing the command into a seperate cog does not provide a benefit. |

## Data
See: [Configuration](configuration.md)

## Listeners
| File      | Purpose                          |
| ----------- | ------------------------------------ |
| `alert_detect.py` | Houses the code that listens for pings to systems operators and determines if the ping should be deleted and the user advised to use `/alert`. |
| `bot_insult.py` | Houses the code that listens for pings to EnduraBot and determines if the user should be insulted. |
| `invites_creation.py` | Houses the code that listens for and logs the creation of invites to the server. |
| `invites_use.py` | Houses the code that listens for, logs, and reports to a configurable channel when someone joins, with what invite, who created said invite, and when said invite was created. |
| `member_monitor.py` | Houses the code that listens for when a member joins and, if they are being monitored, either only sends an alert, or sends an alert and bans the person, whichever is applicable. |

## Logs
| File      | Purpose                          |
| ----------- | ------------------------------------ |
| `endurabot.log` | Houses the logs for EnduraBot. |
| `endurabot_debug.log` | Houses the logs with the `DEBUG` level; seperated from `endurabot.log` as they are quite verbose. |

## Mkdocs
Explaining these files is out of scope. See the documentation for [Mkdocs Material](https://squidfunk.github.io/mkdocs-material) if interested.

## Tasks
| File      | Purpose                          |
| ----------- | ------------------------------------ |
| `bible_daily.log` | Houses the code that sends the daily bible quote. |
| `log_daily_reset.log` | Houses the code that seperates the logs for each day with a date-header. |
| `temp_role_monitor.log` | Houses the code that checks every minute if a person given a temporary role should still have it or not. |

## Utils
| File      | Purpose                          |
| ----------- | ------------------------------------ |
| `config_loader.py` | When imported by `main.py` loads the configuration files. |
| `logging_setup.py` | When imported by `main.py` sets the custom logging levels and formatting. |
| `permissions_checker.py` | Used by all cogs as the global means of checking if a user has permission to use a command. |