import discord
import requests

TOKEN = ''

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)


    if message.content.startswith('!temperature'):
        url = requests.get('https://www.yr.no/place/Antarctica/Other/Amundsen-Scott_South_Pole_Station/')
        start = url.text.find('temperature minus') + 39
        stop = start + 4
        temp = url.text[start:stop]
        msg = '{0.author.mention} Here is ' + temp + ' degrees ' + 'in Antarctica'
        await message.channel.send(msg.format(message))


    if message.content.startswith('!kills'):
        site = requests.get('https://zkillboard.com/').text

        def findkill():
            start_kill = site.text.find("killListRow")
            return start_kill

        def find_next_kill_value(page):
            start_link = page.find("killListRow")
            if start_link == -1:
                return None, 0
            start_quote = page.find('/">', start_link) + 2
            end_quote = page.find('</a>', start_quote)
            url = page[start_quote + 1:end_quote]
            return url, end_quote

        def find_next_kill_link(page):
            start_link = page.find("killListRow")
            if start_link == -1:
                return None, 0
            start_quote = page.find('<a href="/kill/', start_link) + 9
            end_quote = page.find('">', start_quote + 1)
            url = page[start_quote + 1:end_quote]
            return url, end_quote

        def find_all_kills_values(page):
            values = []
            while True:
                url, endpos = find_next_kill_value(page)
                if url:
                    values.append(url)
                    page = page[endpos:]
                else:
                    break
            return values

        def find_all_kills_links(page):
            links = []
            while True:
                url, endpos = find_next_kill_link(page)
                if url:
                    links.append(url)
                    page = page[endpos:]
                else:
                    break
            return links

        database = []

        values_list = find_all_kills_values(site)
        links_list = find_all_kills_links(site)

        i = 0

        for i in range(0, 50):
            database.append([values_list[i], "https://zkillboard.com/" + links_list[i]])
            i += 1

        i = 0
        preresult = []

        while i <= len(database) - 1:
            if database[i][0][-1] == "k":
                del database[i]
            else:
                preresult.append(database[i])
            i += 1

        print(len(database))
        i = 0
        result = []
        print(preresult)

        while i <= len(preresult) - 1:
            var = preresult[i][0][0:-1]
            varstrip = var.replace(",", "")
            if preresult[i][0][-1] == "b":
                print(preresult[i][0])
                result.append(preresult[i])
            if int(float(varstrip)) < 100:
                del preresult[i]
            else:
                result.append(preresult[i])
                print(varstrip)
            i += 1
        msg = '{0.author.mention} Last valuable kills ' + str(result)
        await message.channel.send(msg.format(message))
        print(result)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)

