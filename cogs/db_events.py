from .base_cog import BaseCog
import discord
from discord.ext import commands
from database import Methods as db_util
from database import DBFunction


class Cog(BaseCog, name="DBEvent"):
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        with self.cursor_context(commit=True) as cursor:
            member_count = len(guild.members)
            humans = member_count - len([m for m in guild.members if m.bot])
            db_util.insert("server_list").items(
                server_id=guild.id, name=guild.name, members=member_count,
                human_members=humans, bot_members=member_count - humans
            ).run(cursor)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with self.cursor_context(commit=True) as cursor:
            db_util.delete("server_list").where(
                server_id=guild.id
            ).run(cursor)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.content.startswith(self.bot.command_prefix) and not message.author.bot:
            guild = message.guild
            author = message.author
            channel = message.channel
            if guild is not None:
                with self.cursor_context(commit=True) as cursor:
                    db_util.insert("server_user_stats").items(
                        server_id=guild.id, channel_id=channel.id,
                        user_id=author.id, msg_count=1
                    ).append_sql("ON DUPLICATE KEY UPDATE msg_count = msg_count + 1").run(cursor)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with self.cursor_context(commit=True) as cursor:
            db_util.insert("server_event_logs").items(
                server_id=member.guild.id, user_id=member.id,
                event_type="joined"
            ).run(cursor)

            update = db_util.update("server_list").where(
                server_id=member.guild.id
            )
            if member.bot:
                update.items(bot_members=DBFunction("bot_members + 1")).run(cursor)
            else:
                update.items(human_members=DBFunction("human_members + 1")).run(cursor)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with self.cursor_context(commit=True) as cursor:
            db_util.insert("server_event_logs").items(
                server_id=member.guild.id, user_id=member.id,
                date_utc=DBFunction("NOW()"), event_type="left"
            ).run(cursor)

            update = db_util.update("server_list").where(
                server_id=member.guild.id
            )
            if member.bot:
                update.items(bot_members=DBFunction("bot_members - 1")).run(cursor)
            else:
                update.items(human_members=DBFunction("human_members - 1")).run(cursor)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        with self.cursor_context(commit=True) as cursor:
            db_util.insert("server_event_logs").items(
                server_id=guild.id, user_id=user.id,
                event_type="banned"
            ).run(cursor)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        with self.cursor_context(commit=True) as cursor:
            db_util.insert("server_event_logs").items(
                server_id=guild.id, user_id=user.id,
                event_type="unbanned"
            ).run(cursor)
