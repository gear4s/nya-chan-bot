from discord.ext import commands
import discord

from cogs.base_cog import BaseCog
from database import Methods as db_util


class Cog(BaseCog, name="Welcome"):
    """Welcomes new members to the server via private message"""
    def get_message(self, guild):
        with self.cursor_context() as cursor:
            db_util.select("server_base_config").items("welcome_message").where(server_id=guild.id).run(cursor)
            row = cursor.fetchone()

        return row[0] if row else None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        user_role = discord.utils.get(member.guild.roles, name="Users")
        if user_role is not None:
            await member.add_roles(user_role, reason="Safeguard against pruning.")
        text = self.get_message(member.guild)
        if text:
            try:
                await member.send(text.format(member, member.guild))
            except discord.Forbidden:
                pass

    @commands.command(description='Send the welcome message via private message again.')
    @commands.guild_only()
    async def welcome(self, ctx):
        """Resend welcome message"""
        text = self.get_message(ctx.guild)
        if text:
            try:
                await ctx.author.send(text.format(ctx.author, ctx.guild))
            except discord.Forbidden:
                pass
