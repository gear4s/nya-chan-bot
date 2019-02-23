import discord
from discord.ext import commands
from discord.ext.commands import group
from cogs.base_cog import BaseCog
from nyalib.NyaBot import ThrowawayException
from types import SimpleNamespace


class Moderation(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.roles = {
            "set": {
                "Mods": SimpleNamespace(name="mod_role", checked=True),
                "Moderators": SimpleNamespace(name="moderator_role", checked=False),
                "Mod Trainees": SimpleNamespace(name="trainee_role", checked=True)
            },
            "remove": {
                "Mods": SimpleNamespace(name="mod_role", checked=True),
                "Moderators": SimpleNamespace(name="moderator_role", checked=True)
            },
            "set_trainee": {
                "Mods": SimpleNamespace(name="mod_role", checked=True),
                "Moderators": SimpleNamespace(name="moderator_role", checked=False),
                "Mod Trainees": SimpleNamespace(name="trainee_role", checked=True)
            },
            "remove_trainee": {
                "Mods": SimpleNamespace(name="mod_role", checked=False),
                "Moderators": SimpleNamespace(name="moderator_role", checked=False),
                "Mod Trainees": SimpleNamespace(name="trainee_role", checked=True)
            }
        }

    async def _Moderation__before_invoke(self, ctx):
        if ctx.invoked_subcommand is not None:
            username = ctx.kwargs.get("username")

            converter = commands.converter.MemberConverter()
            user = await converter.convert(ctx, username)
            if user is None:
                await ctx.reply('The user **{}** cannot be found'.format(username))
                raise ThrowawayException

            command_name = ctx.invoked_subcommand.name

            missing = []
            roles = SimpleNamespace()
            has_roles = SimpleNamespace()
            for role_name, attribute in self.roles[command_name].items():
                role = discord.utils.get(ctx.guild.roles, name=role_name)
                if not role:
                    missing.append(role_name)
                    continue

                if attribute.checked:
                    setattr(has_roles, attribute.name, discord.utils.get(user.roles, name=role_name) is not None)
                setattr(roles, attribute.name, role)

            if missing:
                await ctx.reply('These roles cannot be found: {}'.format(", ".join(missing)))
                raise ThrowawayException

            user.has = has_roles

            ctx.user = user
            ctx.roles = roles

    @group()
    async def mod(self, ctx):
        """Mod commands."""
        if ctx.invoked_subcommand is None:
            await ctx.reply('Invalid mod command passed')

    @mod.command(description='Promotes an user to be a Mod')
    @commands.has_any_role('Nixie', 'Supervisors')
    async def set(self, ctx, *, username: str):
        """Promotes an user to be a Mod"""
        if ctx.user.has.mod_role is True:
            await ctx.reply('{} is a Mod already'.format(username))
            return False

        if ctx.user.has.trainee_role is True:
            await ctx.user.add_roles(ctx.roles.mod_role, reason="Promoted to Mods")
            await ctx.user.remove_roles(ctx.roles.trainee_role, reason="Promoted to Mods")
        else:
            await ctx.user.add_roles(ctx.roles.mod_role, ctx.roles.moderator_role, reason="Promoted to Mods")
        await ctx.reply('{} is now a Mod'.format(ctx.user.name))

    @mod.command(description='Removes an user Mod status')
    @commands.has_any_role('Nixie', 'Supervisors')
    async def remove(self, ctx, *, username: str):
        """Removes an user Mod status"""
        if ctx.user.has.mod_role is False:
            await ctx.reply('{} is a not a Mod'.format(username))
            return

        await ctx.user.remove_roles(ctx.roles.mod_role, ctx.roles.moderator_role, reason="User demoted from Mods")
        await ctx.reply('{} is not a Mod anymore'.format(ctx.user.name))

    @mod.command(description='Promotes an user to be a Mod Trainee')
    @commands.has_any_role('Nixie', 'Supervisors')
    async def set_trainee(self, ctx, *, username: str):
        """Promotes an user to be a Mod Trainee"""
        if ctx.user.has.trainee_role is True:
            await ctx.reply('{} is a Mod Trainee already'.format(username))
            return

        if ctx.user.has.mod_role is True:
            await ctx.user.add_roles(ctx.roles.trainee_role, reason="Promoted to Mod Trainees")
            await ctx.user.remove_roles(ctx.roles.mod_role, reason="Promoted to Mod Trainees")
        else:
            await ctx.user.add_roles(ctx.roles.trainee_role, ctx.roles.moderator_role, reason="Promoted to Mod Trainees")
        await ctx.reply('{} is now a Mod Trainee'.format(ctx.user.name))

    @mod.command(description='Removes an user Mod Trainee status')
    @commands.has_any_role('Nixie', 'Supervisors')
    async def remove_trainee(self, ctx, *, username: str):
        """Removes an user Mod Trainee status"""
        if ctx.user.has.trainee_role is False:
            await ctx.reply('{} is a not a Mod Trainee'.format(username))
            return

        await ctx.user.remove_roles(ctx.roles.trainee_role, ctx.roles.moderator_role, reason="User demoted from Mod Trainees")
        await ctx.reply('{} is not a Mod Trainee anymore'.format(ctx.user.name))


def setup(bot):
    cog = Moderation(bot)
    bot.add_cog(cog)
