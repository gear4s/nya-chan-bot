import re

from discord import Message
from discord.ext.commands import Bot
from types import SimpleNamespace


# Add regex here, along with the response the bot should give if it finds a match.
# We're using {bot} and {user} to refer


class TriggerWords:
    """
    Trigger responses from certain regular expression triggers.
    """

    def __init__(self, bot: Bot):
        self.bot = bot
        self.triggers = None

    async def on_ready(self):
        """
        Generates the regex and responses once
        the bot has booted. This information is not
        available until runtime.
        """
        self.triggers = [
            SimpleNamespace(
                regex=re.compile("(:?i'?m|i am) (going|gonna go) to (:?bed|sleep)"),
                response="Good night {}!"
            ),
            SimpleNamespace(
                regex=re.compile(f"(:?hi|hello|hey there|sup) {self.bot.user.mention}!?"),
                response="Hey {}!"
            )
        ]

    async def on_message(self, message: Message):
        """
        This event triggers whenever someone sends a message into any channel.

        If the content of the message matches one of our triggers, we'll respond
        with the corresponding message.
        """
        if not self.triggers:
            return

        response = None
        for trigger in self.triggers.keys():
            if trigger.regex.search(message.content):
                response = trigger.response
                break

        if response:
            await message.channel.send(response.format(user=message.author.mention))


def setup(bot):
    bot.add_cog(TriggerWords(bot))
