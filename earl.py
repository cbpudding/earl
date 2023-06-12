#!/usr/bin/python
import discord
import hashlib
import random
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
                # Arrays mean we have multiple options. We'll either pick one at
                # random or use the first capture group as the hash input for
                # reproducable results. ~Alex
                if type(response) is list:
                    selector = 0
                    if len(groups) > 0:
                        victim = groups[0].lower().encode(encoding="utf8")
                        selector = hashlib.sha1(victim).digest()[0]
                        selector = selector % len(response)
                    else:
                        selector = random.randint(0, len(response) - 1)
                    formatted = response[selector].format(*groups)
                    await message.channel.send(formatted, mention_author=False, reference=message)
                # If the response starts with a plus sign, then we're reacting
                # with an emoji. ~Alex
                elif response.startswith("+"):
                    id = response[1:]
                    if id.isnumeric():
                        emoji = None
                        try:
                            emoji = await message.guild.fetch_emoji(id)
                            await message.add_reaction(emoji)
                        except:
                            print("Failed to fetch emoji: " + id)
                    else:
                        await message.add_reaction(id)
                # Otherwise, it's a plain ol' response. Format and go. ~Alex
                else:
                    formatted = response.format(*groups)
                    await message.channel.send(formatted, mention_author=False, reference=message)
                return

intents = discord.Intents.default()
intents.message_content = True

earl = Earl(intents=intents)

with open("token.txt", "r") as secret:
    earl.run(secret.read())