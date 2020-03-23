# DiscordHeadlessClient

Small headless client for discord using their hidden api.

## To use

You'll need to retrieve your discord token to do this you can open discord in chrome and login then go to chrome developr tools > application > Local storage and in the local storage you'll find dict of information and in the dict will be a key called token the value is your token.

To get serverIDs and channelIDs you'll need to go to discord settings and enable developer mode. Then when you right click on a server or channel there'll be an option to copy id. That's what you pass to the respective command.

Commands:
- js --[serverID] - Changes you to the server you input as the arg
- cc --[channelID] - Changes you to the channel you input as the arg
- exit - Closes the program
- help - lists all commands
