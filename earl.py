#!/usr/bin/python
import discord
import re
import yaml

patterns = yaml.safe_load(open("patterns.yml", "r"))

class Earl(discord.Client):
    async def on_message(self, message):
        # We don't want to have Earl respond to himself ~Alex
        if message.author == self.user:
            return
        # Search for any patterns in the message and send the first matching
        # response we find ~Alex
        for pattern, response in patterns.items():
            match = re.search(pattern, message.content)
            if bool(match):
                groups = []
                if match.lastindex != None:
                    for i in range(1, match.lastindex + 1):
                        groups.append(match.group(i))
                formatted = response.format(*groups)
                await message.channel.send(formatted, mention_author=False, reference=message)
                return

intents = discord.Intents.default()
intents.message_content = True

earl = Earl(intents=intents)

with open("token.txt", "r") as secret:
    earl.run(secret.read())