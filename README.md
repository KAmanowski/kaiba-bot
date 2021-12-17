# Kaiba Bot

The bot to rule them all.

# Commands
All commands start with a prefix of `£`. Supported commands:

## Ping
`ping` makes the server reply with 'pong'.

## Rand
`rand` returns a random number.

### Arguments
All arguments given must be whole numbers.

- `£rand`: returns a decimal between `0` and `1`.
- `£rand <arg 1>`: returns a number between `0` and `<arg 1>`.
- `£rand <arg 1> <arg 2>`: returns a number between `<arg 1>` and `<arg 2>`.
  
  ![Capture](https://user-images.githubusercontent.com/18753120/141537045-2df44ab3-36da-4991-a9d8-71dae5073bf6.PNG)

## Server
`server` allow you to control a dedicated server for a specific game. 

List of currently supported servers:
- `valheim`

### Server Commands
There are 3 available server commands:

- `£server start <server>` starts a server.
- `£server kill <server>` kills a server.
- `£server restart <server>` restarts a server.

![Capture](https://user-images.githubusercontent.com/18753120/141541057-091db6a4-5cea-4348-98eb-8543fb52fbd3.PNG)

You can't start a new server command when there is one in progress. Also, you can be soft-banned for being an asshole with the commands.

## Announce
`announce` allows you to send a message as the bot to a specific channel on a server. The support server/channel pairs include:
-  `kaiba` (the Kaiba Corp. server):
	- `bantercave`
	- `servers`
	- `ttr`  (thingies-to-remember)
	- `hearties` (arrrr-me-hearties)
	- `valheim`
	- `dealhunters`
	- `bot`
	- `jukebox`

### Usage
Usage of the command is simple: `£announce <server> <channel> "<message in quotes>"`

Example: `£server kaiba bantercave "This is the bot speaking. Beep boop."`

## Parrot
`parrot` makes the bot parrot what you just wrote.

### Usage
`£parrot "<message>"` will make the bot delete your message, and say what you just said in the same channel.

Example: `£parrot "Shut up."`

# Requests
If you have an idea for what you want the bot to be able to do, raise an issue for it or tell me and I'll do it.

# Install
- Install Python 3.10+
	- Make sure to tick the 'Add to PATH' checkmark when intalling.
- Navigate to /scripts/install.bat and run it.
- Get your bot API key from discord and slap it into auth.json in /src/config.
- That should be it.