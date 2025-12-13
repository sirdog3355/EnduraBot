The following will explain how to set up an environment to locally host an instance of EnduraBot.

## Requirements
You will need the following before you begin.

- [Python 3.13](https://www.python.org/) or greater installed on your machine.
- [Git](https://git-scm.com/install/) installed on your machine.
- A [Discord bot token](#bot-setup-and-invitation).
- An [IsThereAnyDeal API](#isthereanydeal-api-token) token.
- Have sufficient permissions to invite a bot to a Discord server. It's suggested to make a dedicated one to tinker with EnduraBot.

## On Discord IDs
Configuration will be dependent on IDs for various Discord-objects being obtained.

To get an ID for things you must enable Discord developer mode. This is done by going to the `User Settings` cog, scrolling down to `Advanced`, then ticking `Developer Mode`.

To get the ID for something you will typically right-click on it and select the option that appears called `Copy ID`. It will be copied to your clipboard.

## Bot setup and invitation
!!! warning
    It is best practice to *not* give bots the `Administrator` permission unless it is *needed* and you trust the bot. Strictly speaking, EnduraBot should not *need* it, but because EnduraBot is developed for a specific single low-traffic Discord server, effort was not put into responsibly limiting it's required permissions.

Before we do anything with EnduraBot's code you'll need a bot application through the [Discord developer portal](https://discord.com/developers/applications) in order to allow the bot to join a server.

Once at the portal click `New Application`, give the bot a name (presumably you'll name it `EnduraBot`), agree to the *Developer Terms of Service* and *Developer Policy*, then click `Create`. On the new screen retype the bot's name and optionally provide an avatar.

Now, navigate to the `Bot` tab located on the left of the screen. Scroll down and enable the `Presence Intent`, `Server Members Intent`, and `Message Content Intent`. Then, scroll back up and click `Reset Token`.

Once you confirm you wish to reset the token[^1] you should see a long string of letters and numbers appear. This is the bot token mentioned in the [requirements](#requirements) section. Hold onto it and store it in a secure place on your computer (such as a dedicated [password manager](https://en.wikipedia.org/wiki/Password_manager)).

Next, go to the `OAuth2` tab located on the left of the screen. Scroll down to the `OAuth2 URL Generator` box and select the following:

- `bot`
- `applications.commands`

When you select `bot` a new sub-box should appear below called `BOT PERMISSIONS`. Select `Administrator`.

At the very bottom you will have a `Generated URL`. Ensure the option above it is set to `Guild Install` and not `User Install`. Then paste that into a browser and Discord will guide you through inviting the bot.

## IsThereAnyDeal API token
!!! warning
    Per the MIT license it is *your* responsibility to ensure that your use of the IsThereAnyDeal API is in-line with their [API terms of service](https://docs.isthereanydeal.com/#section/Terms-of-Service).

In order to access the IsThereAnyDeal API an access token needs to be obtained. This is quite simple.

1. Navigate to [https://isthereanydeal.com/apps/](https://isthereanydeal.com/apps/).
2. Click `Sign in to register an app`.
3. Create an account or sign in through STEAM.
4. Click `Register App` and give your application a unique name.
5. Click the green box underneath the `API Keys` header.

Like with the Discord bot token, hold onto this and store it securely on your computer.

## Cloning the repository
Navigate in a terminal to the directory you desire to house EnduraBot's code. It's advised to use an IDE which has a terminal built in, such as [Visual Studio Code](https://code.visualstudio.com/). Then, run the following command:
``` sh
git clone https://github.com/sirdog3355/EnduraBot.git
```

## Local setup

### Environment variables
!!! danger
    The purpose of a `.env` file is to safely store and access sensitive credentials rather than hard code them. This file should never be committed to any kind of repository. It should only ever be on your own machine and on the machine hosting the bot.

Take `.env-example`, copy it into the directory that houses `main.py`, then rename it to `.env`. This expects a couple of variables:

```dotenv title=".env"
guild=
token=
itad-token=
```

The `guild` is the Discord server ID for the server that you want EnduraBot to join. EnduraBot will leave any server that does not match this ID.

The `token` is the bot token you got from the Discord developer portal.

The `itad-token` is the token you got from ITAD.

When done you should see the following structure:
``` hl_lines="9"
.
|── classes/
|── cogs/
|── data/
|── listeners/
|── tasks/
|── utils/
|── zensical/
|── .env
|── .env-example
|── .gitignore
|── docker-compose.yml
|── Dockerfile
|── LICENSE.md
|── main.py
|── README.md
└── requirements.txt
```

### Configuration
Navigate to `data` and notice that 3 JSON files exist here.

```
|──data /
|   |── misc_text_example.json
|   |── permissions_example.json
|   └── variables_example.json
```

Copy and paste them all into `data` and rename them to remove the `_example`. This should result in the following structure:

``` hl_lines="3 5 7"
|──data /
|   |── misc_text_example.json
|   |── misc_text.json
|   |── permissions_example.json
|   |── permissions.json
|   |── variables_example.json
|   └── variables.json
```

Due to the `.gitignore` that comes with the repository they should automatically not be tracked once renamed.

`misc_text.json` may be left alone. If you have the `Adminsitrator` permission on the server that will host EnduraBot you may also do this with `permissions.json`. An alternative is to blank the file and replace it with `{}`, though be warned that this means *anyone* on the server can use *any* command.

If neither option is viable review the documentation on [permissions](configuration.md#permissions).

For EnduraBot to function properly the following variables in `variables.json` need proper IDs added. Click the :material-plus-circle-outline: for an explanation of each item.

``` json title="variables.json"
{
    "out_of_context_channel_id": 1426036432195289160, //(1)!
    "alert_channel_id": 1426036519692669042, //(2)!
    "based_chat_channel_id": 1426036403506118656, //(3)!
    "sysop_role_id": 1426035389214232656, //(4)!
    "mod_role_id": 1426035365671731292, //(5)!
    "cooldown_exempt_roles": [ //(6)!
        1426035365671731292,
        1426035308297715742
    ]
}
```

1. Channel with out of context messages; used by the `/rquote` and the daily bible quote task.
2. Channel where EDC systems operators chat; used primarily by `/alert` and `/estop`.
3. Channel where daily bible quotes and temporary role notifications are sent.
4. Role that represents a member that runs technical stuff for the community. It's the role pinged by `/alert` and is used as an exemption criteria for the `alert_detection.py` listener.
5. Role that represents a server moderator.
6. List of role IDs that bypass the `/rquote` cooldown.

!!! note
    The command `/trole` will default to using the *first* role in `mod_editables_roles` if the user does not select one themselves.

There is also a list of key value pairs at variable `mod_editable_roles`.

```json title="variables.json"
"mod_editable_roles": {
        "dummy_role_a": 1122334455667788990,
        "dummy_role_b": 2233445566778899001,
        "dummy_role_c": 3344556677889900112
    }
```

The keys (e.g `dummy_role_a`) are what is shown to a user running `/trole` or `/editrole` as the roles which can be manipulated. While not required, the live bot running for EDC has them formatted as `@` followed by the fancy role name (e.g `@L`). 

The IDs should be the associated role ID.

It is advised to edit the other variables to your liking. All variables are documented at the [page on configuration](configuration.md#variables).

### Logs folder
EnduraBot does all logging to files. While it will automatically create the relevant files on startup it will *not* create the *directory* it expects them in.

Simply create a directory called `logs` in the same directory as `main.py`. This should result in the following structure:

``` hl_lines="6"
.
|── classes/
|── cogs/
|── data/
|── listeners/
|── logs/
|── tasks/
|── utils/
|── zensical/
|── .env
|── .env-example
|── .gitignore
|── docker-compose.yml
|── Dockerfile
|── LICENSE.md
|── main.py
|── README.md
└── requirements.txt
```

## Python dependencies
!!! info
    It is best practice in Python development to install dependencies in a [virtualized environment](https://docs.python.org/3/library/venv.html) rather than your global environment. If you choose to do this, and you have not already, it may be worth adding `venv` to your global Git ignore file.

There are Python specific dependencies required for EnduraBot to run. You may install them by running the following from within the directory housing `requirements.txt`:
``` sh
pip install -r requirements.txt
```

## Running the bot
By this point everything should be set for the bot to run properly. To run it, navigate in a terminal to the directory that houses `main.py` and run the following command:

```sh
python main.py
```

You should see something like this:
``` py hl_lines="7"
[20XX-XX-XX XX:XX:XX]:INFO:endurabot: Loaded cogs.bible_daily
[20XX-XX-XX XX:XX:XX]:INFO:endurabot: Loaded cogs.bot_react
[20XX-XX-XX XX:XX:XX]:INFO:endurabot: Loaded cogs.user_cmds
[20XX-XX-XX XX:XX:XX]:INFO:endurabot.cogs.bible_daily: Waiting for bot to be ready before starting daily bible quote loop...
[20XX-XX-XX XX:XX:XX]:INFO:endurabot.cogs.bible_daily: Bot ready, starting daily bible quote loop.
[20XX-XX-XX XX:XX:XX]:INFO:endurabot: Synced X commands.
[20XX-XX-XX XX:XX:XX]:INFO:endurabot: Hello, world! I am awake and ready to work!
```

Once you see the highlighted line the bot is functioning and ready to go. It may sometimes take awhile for commands to sync; they will typically still work before the highlighted line appears but unexpected behavior may occur.

## SQLITE
EnduraBot utilizes a SQLITE database to hold persistent information. This will be created automatically once the bot runs for the first time. As a result, the *final* directory structure after a successful boot up of the bot will be the following:

``` hl_lines="15"
.
|── classes/
|── cogs/
|── data/
|── listeners/
|── logs/
|── tasks/
|── utils/
|── zensical/
|── .env
|── .env-example
|── .gitignore
|── docker-compose.yml
|── Dockerfile
|── endurabot.db
|── LICENSE.md
|── main.py
|── README.md
└── requirements.txt
```

## About Docker
The live bot that runs for EDC is hosted in a Docker container on the community's infrastructure. `docker-compose.yml` and `Dockerfile` are used for this purpose. You are, per the license, free to use these files to do this yourself. You will need to adjust them, though.  

I do not feel confident documenting how to do so (nor am I interested in maintaining such documentation).


[^1]: Resetting the bot token on a new application is standard practice. Discord, as as a security measure, does not allow reviewing active tokens; you can only generate new ones. Thus, since the initial one is not provided, you have to reset it. This has no bearing on anything given the initially created token is never used.


*[SaaS]: Software as a service
