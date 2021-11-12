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

`£rand`: returns a decimal between `0` and `1`.

`£rand <arg 1>`: returns a number between `0` and `<arg 1>`.

`£rand <arg 1> <arg 2>`: returns a number between `<arg 1>` and `<arg 2>`.
  
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

You can't start a new server command when there is one in progress

# Requests
If you have an idea for what you want the bot to be able to do, raise an issue for it.
