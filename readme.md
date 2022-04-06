# Idea
I want to use a DS18S20 wired to a raspberry pi to alert me, when I leave the freezer door open by accident again (this has been happening way to often lately)

I imagine it like this:

* The pi watches the temprature and emits an optical and audible signal when the temperature drops under a certain threshold
* The pi watches the door and also alerts me audible when it is open an extended amount of time
* The pi operates a telegram bot who would send messages to a group in the above events
 * This way I can easily add users to the bot, without hardcoding any numbers
* The alerts can be silenced via sending a message in the telegram group
* The bot maintaines a pinned message with the current temperature in the group
** unpin all messages
** send new message with current temerature
** save of that id persistently (in file)
** from now on, update the message when a new temperature is read

# How to use
Check `/sys/bus/w1/devices/`directory. Every sensor that the sytems sees will be listed here as subdirectory.
There naming will be a component family code follow by `_` and an unique identifier.
The DS18S20's familiy code will be `28`
Grab the name of the directory.

Run temp-alarm.py `temp-alarm.py <target_temperature> <sensor_dir>`

The script will loop until exited via KeyboardInterrupt

# To Dos
See issue tracker
