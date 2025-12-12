!!! info
    `Output Type` means whether the command causes a message to appear that anyone can see (i.e `Static`) or only the executor can see (i.e `Ephemeral`).

| Command | Who Can Use | Output Type | Description |
| :--- | :--- |  :--- |  :--- |
| `/about` | Anyone | Static | Get general infromation about EnduraBot. |
| `/alert` | Full Member | Static |  Send an alert to EDC systems operators. |
| `/blacklist` | Moderators | Static |  Blacklist a member from using EnduraBot at all. |
| `/echo` | Moderators | Static  | Make EnduraBot say something. |
| `/editrole` | Moderators | Static | Add or remove configurable roles from a member. |
| `/estop` | Moderators and Systems Operators | Static | Shutdown EnduraBot as an emergency measure. |
| `/user` | Anyone | Ephemeral | Get generic information about a server member. |
| `/info` | Anyone | Static | Get various information relevant to EDC by selecting one of the available options. |
| `/reboot` | Systems Operators | Ephemeral | Reboot EnduraBot. |
| `/rgit-deals` | Full Member | Static | Get a list of upto 25 deals for games submitted as options for RGIT. |
| `/rgit-edit` | Moderators |  Ephemeral | Add or remove games from the RGIT table used by `/rgit-deals`. |
| `/rgit-list` | Anyone | Ephemeral | Get a raw list of every game on the RGIT table. |
| `/rquote` | Anyone | Static | Take a quote from `#out-of-cotext` and present it with a comedic, fictionalized context. |
| `/rquote-debug` | Systems Operators | Ephemeral | Run the `/rquote` code on a specific message to see how it would be treated. |