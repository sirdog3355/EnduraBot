The following will explain how to set up an environment to locally host an instance of EnduraBot.

## Requirements
You will need the following before you begin.

- [Python 3.13](https://www.python.org/) or greater installed on your machine.
- [Git](https://git-scm.com/install/) installed on your machine.
- A [Discord bot token](#bot-setup-and-invitation).
- An [IsThereAnyDeal API](#isthereanydeal-api-token) token.
- Have sufficient permissions to invite a bot to a Discord server. It's suggested to make a dedicated one to tinker with EnduraBot.

## On Discord IDs
Configuration will be dependent on IDs for various Discord-related things being obtained.

To get an ID for things you must enable Discord developer mode. This is done by going to the `User Settings` cog, scrolling down to `Advanced`, then ticking `Developer Mode`.

To get the ID for something you will typically right-click on it and select the option that appears called `Copy ID`. It will be copied to your clipboard.

## Bot setup and invitation
!!! warning
    It is best practice to *not* give bots the `Administrator` permission unless you fully trust it and it *needs* it to function. Strictly speaking EnduraBot should not *need* it, but because EnduraBot primarily exists for a single non-public facing Discord server, effort was not put into responsibly limiting it's required permissions.

Before we do anything with EnduraBot's code you'll need a bot application through the [Discord developer portal](https://discord.com/developers/applications) in order to allow the bot to join a server.

Once at the portal click `New Application`, give the bot a name (presumably you'll name it `EnduraBot`), agree to the *Developer Terms of Service* and *Developer Policy*, then click `Create`. On the new screen retype the bot's name and optionally provide an avatar.[^1]

Now, navigate to the `Bot` tab located on the left of the screen. Scroll down and enable the `Presence Intent`, `Server Members Intent`, and `Message Content Intent`. Then, scroll back up and click `Reset Token`.

Once you confirm you wish to reset the token you should see a long string of letters and numbers appear. This is the bot token mentioned in the [requirements](#requirements) section. Hold onto it and store it in a secure place on your computer (such as a dedicated [password manager](https://en.wikipedia.org/wiki/Password_manager)).

Next, go to the `OAuth2` tab. Scroll down to the `OAuth2 URL Generator` box and select the following:

- `bot`
- `applications.commands`

When you select `bot` a new sub-box should appear below called `BOT PERMISSIONS`. Select `Administrator`.

At the very bottom you will have a `Generated URL`. Ensure the option above it is set to `Guild Install` and not `User Install`. Then paste that into a browser and Discord will guide you through inviting the bot.

[^1]: You can use the image located at `/mkdocs/docs/assets/EnduraBot_Logo.png` in the EnduraBot repository if you would like.

## IsThereAnyDeal API token
!!! warning
    Per the MIT license it is *your* responsibility to ensure that your use of the IsThereAnyDeal API is in-line with their [API terms of service](https://docs.isthereanydeal.com/#section/Terms-of-Service).

In order to access the IsThereAnyDeal API, which is what allows `/rgit-edit` and `/rgit-deals` to function, an API token needs to be obtained. This is quite simple.

1. Navigate to [https://isthereanydeal.com/apps/](https://isthereanydeal.com/apps/).
2. Click `Sign in to register an app`.
3. Create an account or sign in through STEAM.
4. Click `Register App` and give your application a unique name.
5. Click the green box underneath the `API Keys` header.

Like with the Discord bot token, hold onto this and store it securely on your computer.

## Cloning the repository
Navigate in a terminal to the directory you desire to house EnduraBot's code. It's advised to use an IDE which has a terminal built in, such as [Visual Studio Code](https://code.visualstudio.com/). Then, run the following command:
``` sh
git clone https://github.com/sirdog9001/EnduraBot.git
```
Note that this will create a directory called `EnduraBot` *inside* of the directory you run this in.

## Local setup

### Environment variables
!!! danger
    Your real `.env` file should *never* leave your machine and/or wherever EnduraBot is being hosted. It absolutely should *not* be committed to any Git repository; especially a remote one. It's highly advised you add this to your global Git ignore file.

Take `.env-example`, copy it into the directory that houses `main.py`, then rename it to `.env`. This expects a couple of variables:

```sh title=".env"
guild=
token=
itad-token=
```

The `guild` is the Discord server ID for the server that you want EnduraBot to join. EnduraBot will leave any server that does not match this ID.

The `token` is the bot token you got from the Discord developer portal.

The `itad-token` is the IsThereAnyDeal token you got from IsThereAnyDeal.

When done you should see the following structure:
``` hl_lines="9"
.
|── classes/
|── cogs/
|── data/
|── listeners/
|── mkdocs/
|── tasks/
|── utils
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

If neither option is viable review the documentation on [permissions](permissions.md).

For EnduraBot to work the following variables in `variables.json` need proper IDs added. Click the :material-plus-circle-outline: for an explanation of each item.

``` json title="variables.json"

{
    "out_of_context_channel_id": 1426036432195289160, //(1)!
    "alert_channel_id": 1426036519692669042, //(2)!
    "based_chat_channel_id": 1426036403506118656, //(3)!
    "sysop_role_id": 1426035389214232656, //(4)!
    "mod_role_id": 1426035365671731292, //(5)!
    "admin_role_id": 1426035308297715742, //(6)!
    "cooldown_exempt_roles": [ //(7)!
        1426035365671731292,
        1426035308297715742
    ]
}

```

1. Channel with messages placed in quotations that represent things people have said out of context; to be used by the `/rquote` and daily bible quote feature.
2. Channel where a message is sent when running `/alert`.
3. Channel where daily bible quotes should be sent.
4. Role that represents a member that runs technical stuff for the community. Used in `/info` to denote the person is a systems operator, is the role pinged by `/alert`, and is used as an exemption criteria for the `alert_detection.py` listener.
5. Role that represents a server moderator. Used by `/info` to determine if the member is a staff member.
6. Role that represents a server administrator. Used by `/info` to determine if the member is a staff member.
7. List of role IDs that bypass the `/rquote` cooldown.

There is also a list of key value pairs at variable `mod_editable_roles`.

```json title="variables.json"
"mod_editable_roles": {
        "dummy_role_a": 1122334455667788990,
        "dummy_role_b": 2233445566778899001,
        "dummy_role_c": 3344556677889900112
    }
```

The keys (e.g `dummy_role_a`) serve no programmatic purpose and are purely for readability. The IDs should be role IDs that you'd like `/editrole` to be able to manipulate, otherwise it will not function.

Other variables can be configured to your liking and are documented more properly at the [configuration page](configuration.md).

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
|── mkdocs/
|── tasks/
|── utils/
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
    You may wish to install these dependencies in a [virtualized environment](https://docs.python.org/3/library/venv.html) rather than your master Python environment. If you choose to do this, and you have not already, it may be worth adding `venv` to your global Git ignore file.

There are Python specific dependencies required for EnduraBot to run. You may install them by running the following from within the directory housing the text file:
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

## Considerations
If you have made it this far, congratulations, you now have your very own instance of EnduraBot. I hope you have fun with it.

There are some quirks to be made aware of, both because a) this bot isn't *designed* for public use and b) because I am not a professional software developer.

- You will really want to add atleast *one* game to your RGIT table by using `/rgit-edit` with the `Add Game` option as soon as possible. Otherwise, if you run `/rgit-deals`, you will get a cryptic message saying EnduraBot didn't respond. This is because EnduraBot doesn't know how to gracefully handle an empty RGIT table.
- If you haven't already, unless you are only ever going to tinker with EnduraBot privately, you probably want to get your [permissions](permissions.md) squared away.
- Those who are astute will notice that a `Dockerfile` and `docker-compose.yml` exist in this repository. You are more than welcome to use them to host EnduraBot in a Docker container. I just do not feel confident documenting those steps (nor am I interested in maintaining such documentation). Plenty of tutorials exist regarding Docker, though.
- In regards to `/rquote`:
    - Ensure everyone puts their out of context quotes in `""` or they won't be picked. If you want this to change you'll need to edit code at `cogs/rquote.py` (more details available at the [page dedicated to rquote](rquote.md)).
    - If you are starting from an empty channel please ensure atleast 1 quote is present before someone runs `/rquote`.
