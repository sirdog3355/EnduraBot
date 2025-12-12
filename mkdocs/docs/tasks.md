EnduraBot has Python files colloquially called "tasks" located at `tasks/`; files with code that perform pre-determined actions at pre-determined times.

## Daily bible quote
As a funny feature `tasks/bible_daily.py` was made.

At the hour and minute set by `data/variables.json` under the keys `bibleq_hour_of_day` and `bibleq_min_of_day`, respectively, an embed will be sent to the channel with the `variables.json` key `based_chat_channel_id`.

This will take a random quote out of the channel with `variables.json` key `out_of_context_channel_id` and present it like a preacher reading from a gospel of the Christian bible.

The opening dialogue for these quotes is held at `data/misc_text.json` under the `daily_bible_openers` key and the gospels it will "quote from" are under the `misc_text.json` key `bible_gospels`.