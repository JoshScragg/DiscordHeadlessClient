from pprint import pprint
import time
import json
import requests
import os 

userToken = input('> User Token: ')

def sendMessage(channelID, serverID, userToken):
    baseURL = "https://discordapp.com/api/channels/{}/messages".format(channelID)
    headers = { "Authorization":"{}".format(userToken),
                "User-Agent":"myBotThing (http://some.url, v0.1)",
                "Content-Type":"application/json", }
    message = input('-> ')
    if message == '--leave':
        return main(serverID)
    else: 
        POSTedJSON =  json.dumps ( {"content":message} )
        r = requests.post(baseURL, headers = headers, data = POSTedJSON)
        sendMessage(channelID, serverID, userToken)



################
# CLI COMMANDS #
################

def joinServer(serverID, userToken):
    try:
        serverInfo = []
        baseURL = "https://discordapp.com/api/v6/guilds/{}".format(serverID)
        headers = { "Authorization":"{}".format(userToken),
                    "User-Agent":"myBotThing (http://some.url, v0.1)",
                    "Content-Type":"application/json", }
        r  = requests.get(baseURL, headers = headers).text
        server = json.loads(r)
        serverName = server['name']
        region = server['region']
        owner = server['owner_id']
        ownerInfo = getUserInfo(owner, userToken)
        serverInfo.append(serverName)
        serverInfo.append(region)
        serverInfo.append(ownerInfo)
        print('Welcome to {} the server owner is {}#{}'.format(serverInfo[0], serverInfo[2][0], serverInfo[2][1]))
        print('Do cc --[channelNum] to select your text channel')
        return main(serverID)
    except TypeError:
        print('Invalid Server ID')
        return main()




def getUserInfo(userID, userToken):
    infoList = []
    baseURL = "https://discordapp.com/api/v6/users/{}".format(userID)
    headers = { "Authorization":"{}".format(userToken),
                "User-Agent":"myBotThing (http://some.url, v0.1)",
                "Content-Type":"application/json", }
    r  = requests.get(baseURL, headers = headers).text
    user = json.loads(r)
    username = user['username']
    discriminator = user['discriminator']
    avatar = user['avatar']
    infoList.append(username)
    infoList.append(discriminator)
    infoList.append(avatar)
    return infoList
    


def textChannel(channelID, serverID, userToken):
    channelNamesList = []
    channelIDList = []
    baseURL = "https://discordapp.com/api/v6/guilds/{}/channels".format(serverID)
    headers = { "Authorization":"{}".format(userToken),
                "User-Agent":"myBotThing (http://some.url, v0.1)",
                "Content-Type":"application/json", }
    r  = requests.get(baseURL, headers = headers).text
    channel = json.loads(r)

    for channels in channel:
        channelType = channels['type']
        if channelType == 0:
            textChannels = channels['name']
            textChannelID = channels['id']
            channelNamesList.append(textChannels)
            channelIDList.append(textChannelID)
    
    for i in range(len(channelIDList)):
        channelIDListInt = int(channelIDList[i])
        channelIDInt = int(channelID)
        if channelIDListInt == channelIDInt:      
            print(f'You are in the {channelNamesList[i]} channel you may now send messages')
            print('To exit type --leave')
            return sendMessage(channelIDInt, serverID, userToken)
        #else:
    print('Invalid Channel ID')
    main()


def helpFunc(userToken):
    print("""

Commands:
> js --[serverID] - Changes you to the server you input as the arg
> cc --[channelNum] - Changes you to the channel you input as the arg
> exit - Closes the program
> help - lists all commands

    """)
    return main()

def exitFunc(userToken):
    exit()


#################
# MAIN FUNCTION #
#################

def main(serverID=000):
    commands = {
        "js" : joinServer,
        "cc" : textChannel,
        "exit" : exitFunc,
        "help" : helpFunc
    }
    command = input('> ')
    if '--' in command:
        argument = command.split(' --')
        command = argument[0]
        argument = argument[1]  
        try:
            if command == 'cc':
                commands[command](argument, serverID, userToken)
            else:
                commands[command](argument, userToken)
        except TypeError as error:
            print('> {}: command not found | {}'.format(command, error))
            return main()
    else:
        try:
            commands[command](userToken)
        except (KeyError, TypeError) as error:
            print('> {}: command not found | {}'.format(command, error))
            return main()

main()
