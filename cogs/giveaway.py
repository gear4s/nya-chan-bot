import discord
from discord.ext import commands
from nyalib.NyaBot import ThrowawayException
from database import Methods as db_util
from cogs.base_cog import BaseCog
import random


class Cog(BaseCog, name="Giveaway"):
    giveaways = {}

    async def cog_before_invoke(self, ctx):
        if ctx.invoked_subcommand.name != "list":
            giveaway_name = ctx.kwargs.get("giveaway_name")
            with self.cursor_context() as cursor:
                db_util.select("giveaway").items("giveaway_id").where(
                    server_id=ctx.guild.id, giveaway_name=giveaway_name
                ).run(cursor)
                row = cursor.fetchone()

            message = None
            if ctx.invoked_subcommand.name == "start" and row:
                message = 'The giveaway "{}" already exists.'
            elif ctx.invoked_subcommand.name != "start" and not row:
                message = 'The giveaway "{}" doesn\'t exist.'

            if message:
                await ctx.channel.send(message.format(giveaway_name))
                raise ThrowawayException

            if ctx.invoked_subcommand.name != "start":
                with self.cursor_context() as cursor:
                    db_util.select("giveaway_roles").items("role_id").where(
                        giveaway_id=row[0]
                    ).run(cursor)
                    row = cursor.fetchone()

                ctx.custom["ga_role"] = discord.utils.get(ctx.guild.roles, id=row[0])

                if not ctx.custom.ga_role:
                    await ctx.channel.send("The giveaway exists but the role does not. This should not happen.")
                    raise ThrowawayException

    @commands.group(invoke_without_command=True)
    async def ga(self, ctx):
        """Giveaway commands."""
        await ctx.send_help("ga")

    @ga.command(description='Starts a giveaway.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors',  'Moderators')
    async def start(self, ctx, *, giveaway_name: str):
        """Starts a giveaway"""
        role = await ctx.guild.create_role(
            name=f"Giveaway: {giveaway_name}", mentionable=True,
            reason=f"Giveaway started by {ctx.author.name}"
        )

        with self.cursor_context(commit=True) as cursor:
            db_util.insert("giveaway").items(
                server_id=ctx.guild.id, giveaway_name=giveaway_name
            ).run(cursor)
            db_util.select("giveaway").items("giveaway_id").where(
                server_id=ctx.guild.id, giveaway_name=giveaway_name
            ).limit(1).run(cursor)
            row = cursor.fetchone()

            db_util.insert("giveaway_roles").items(
                giveaway_id=row[0], role_id=role.id
            ).run(cursor)

        await ctx.channel.send(
            '**A new giveaway has started !**\n'
            'Please use the following commands to enter or leave this giveaway\n'
            f'```!n.ga enter {giveaway_name}\n!n.ga leave {giveaway_name}```')

    @ga.command(description='Stop a giveaway.')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators')
    async def stop(self, ctx, *, giveaway_name: str):
        """Stop a giveaway"""
        # Remove the role from server
        await ctx.custom.ga_role.delete()
        with self.cursor_context(commit=True) as cursor:
            db_util.delete("giveaway").where(
                server_id=ctx.guild.id, giveaway_name=giveaway_name
            ).run(cursor)
        await ctx.channel.send(
            f'**The giveaway "{giveaway_name}" has now ended, thank you all for your participation !**')

    @ga.command(description='List giveaways.')
    @commands.guild_only()
    async def list(self, ctx):
        """List giveaways"""
        with self.cursor_context() as cursor:
            db_util.select("giveaway").items("giveaway_name").where(
                server_id=ctx.guild.id
            ).run(cursor)
            rows = cursor.fetchall()

        if not rows:
            await ctx.reply('There are no active giveaways.')
            return

        ga_roles = [
            x[0] for x in rows
        ]
        await ctx.reply(f'Here is the list of the active giveaways ({len(ga_roles)}) :\n```{", ".join(ga_roles)}```')

    @ga.command(description='Enters a giveaway.')
    @commands.guild_only()
    async def enter(self, ctx, *, giveaway_name: str):
        """Enters a giveaway"""
        roles = ctx.author.roles
        has_role = discord.utils.get(roles, id=ctx.custom.ga_role.id) is not None
        if has_role is not False:
            await ctx.reply(f'You already are in the giveaway "{giveaway_name}"')
            return

        await ctx.author.add_roles(ctx.custom.ga_role)
        await ctx.reply(f'You just entered the giveaway "{giveaway_name}"')

    @ga.command(description='Leaves a giveaway.')
    @commands.guild_only()
    async def leave(self, ctx, *, giveaway_name: str):
        """Leaves a giveaway"""
        roles = ctx.author.roles
        has_role = discord.utils.get(roles, id=ctx.custom.ga_role.id) is not None
        if has_role is False:
            await ctx.reply(f'You are not in the giveaway "{giveaway_name}"')
            return

        await ctx.author.remove_roles(ctx.custom.ga_role)
        await ctx.reply(f'You just left the giveaway "{giveaway_name}"')

    @ga.command(description='Pick a winner from the people who entered the giveaway')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators')
    async def pick(self, ctx, *, giveaway_name: str):
        """Pick a winner"""
        participants = ctx.custom.ga_role.members
        if not participants:
            await ctx.reply(f'Nobody entered the giveaway "{giveaway_name}"')
            return

        if giveaway_name not in self.giveaways:
            self.giveaways[giveaway_name] = []

        updated_participants = [
            participant
            for participant in participants
            if participant.id not in self.giveaways[giveaway_name]
        ]
        if not updated_participants:
            await ctx.reply(f'All participants have already won the giveaway "{giveaway_name}"')
            return

        winner = random.choice(updated_participants)
        self.giveaways[giveaway_name].append(winner.id)
        await ctx.channel.send(f'**Congratulation, {winner.mention}, you just won in the giveaway "{giveaway_name}"!')

    @ga.command(description='List winners ID')
    @commands.guild_only()
    @commands.has_any_role('Nixie', 'Supervisors', 'Moderators')
    async def winners(self, ctx, *, giveaway_name: str):
        """List winners ID"""
        winners = []
        for winner_id in self.giveaways[giveaway_name]:
            winner = self.bot.get_user(winner_id)
            if winner is not None:
                winners.append(winner.mention)

        if not winners:
            await ctx.reply(f'There are no winners for the giveaway "{giveaway_name}" yet')
            return
        await ctx.reply('List of winners:\n- {}'.format("\n- ".join(winners)))
