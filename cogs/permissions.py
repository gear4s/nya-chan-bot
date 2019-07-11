from bot.cog_base import Base, commands
from bot.checks import is_admin, is_owner, CHECK_FAIL
from bot.command import NyaCommand, NyaGroup
from discord import Role as DiscordRole, utils as DiscordUtils


class setup(Base, name="Permissions"):
    def __init__(self):
        self.db = self.bot.database.collection("ServersJoined")
        self.unconfigured = []

    def execution_allowed(self, ctx):
        def bw_checker():
            for f in ctx.command.bitwise_checks:
                if f(ctx) & CHECK_FAIL:
                    return False

            return True

        if (isinstance(ctx.command.cog, setup) and bw_checker()) or ctx.command.name == "help":
            return True

        if ctx.guild.id in self.unconfigured:
            return False

        if not bw_checker():
            return False

        return True

    def check_has_permission(self, ctx, of):
        guild = self.db.find(guild_id=str(ctx.guild.id))
        if not guild:
            return False

        if f'{of}_role_ids' not in guild.getStore():
            return False

        for role_id in guild[f"{of}_role_ids"]:
            if DiscordUtils.get(ctx.author.roles, id=int(role_id)):
                return True
        return False

    def check_is_admin(self, ctx):
        return self.check_has_permission(ctx, "admin")

    def check_is_moderator(self, ctx):
        return self.check_has_permission(ctx, "mod")

    @commands.group("config", cls=NyaGroup, invoke_without_command=True)
    @is_admin()
    async def configure(self, ctx):
        await ctx.send_help(ctx.invoked_with)

    @configure.command("set_moderators", cls=NyaCommand)
    @is_admin()
    async def configure_set_moderator_roles(self, ctx, roles: commands.Greedy[DiscordRole]):
        entry = self.db.find(guild_id=str(ctx.guild.id))
        entry["mod_role_ids"] = [str(role.id) for role in roles]
        entry["configured"] = True
        entry.save()
        await ctx.message.add_reaction('👍')

    @configure.command("set_admins", cls=NyaCommand)
    @is_owner()
    async def configure_set_admin_roles(self, ctx, roles: commands.Greedy[DiscordRole]):
        entry = self.db.find(guild_id=str(ctx.guild.id))
        entry["admin_role_ids"] = [str(role.id) for role in roles]
        entry["configured"] = True
        entry.save()
        await ctx.message.add_reaction('👍')

    @Base.listener()
    async def on_ready(self):
        guilds = [guild.id for guild in self.bot.guilds]
        differences = set(guilds) ^ set(int(guild["guild_id"]) for guild in self.db.entries)
        for guild_id in differences:
            if guild_id not in guilds:
                self.db.find(guild_id=str(guild_id)).delete()
            else:
                self.unconfigured.append(guild_id)
                self.db.enter(
                    dict(
                        guild_id=str(guild_id)
                    )
                )

    @Base.listener()
    async def on_guild_join(self, guild):
        self.db.enter(
            dict(
                guild_id=str(guild.id)
            )
        )

    @Base.listener()
    async def on_guild_remove(self, guild):
        self.db.find(guild_id=str(guild.id)).delete()

