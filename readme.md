# Idea
I want to use a DS18S20 wired to a raspberry pi to alert me, when I leave the freezer door open by accident again (this has been happening way to often lately)

I imagene it like this:

* The pi watches the temprature and emits and optical and audible signal when the temperature drops under a certain threshold
* The pi watches the door and also alerts me audible when it is open an extended amount of time
* The Pi operates a telegram bot who would send messages to a group in the above events
 * This way I can easily add users to the bot, without hardcoding any numbers
* the alerts can be silenced via sending a message in the telegram group
