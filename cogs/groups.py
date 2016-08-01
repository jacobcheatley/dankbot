import discord
from discord.ext import commands
from typing import Iterable
from .utils import database, functions, checks
import re


class Groups:
    """The group system is very dank. Because of how stuff works, !help group might be more useful."""

    def __init__(self, bot):
        self.bot = bot
        self.db = database.Database('groups.json')
        self.notify_regex = re.compile('@!(\S+)')

    @commands.group()
    async def group(self):
        """Allows you to create, manage and notify groups of people."""
        pass

    def get_group(self, group_name):
        entry = self.db.get(group_name, None)
        return entry

    async def modify_test(self, lookup, group, ctx):
        if group is None:
            await self.bot.say('You wot. Group {} doesn\'t exist.'.format(lookup))
            return False
        if not (group['owner'] == ctx.message.author.id or checks.is_owner_check(ctx.message)):
            await self.bot.say('You do not have permissions to modify this group.')
            return False
        return True

    async def _notify(self, channel: discord.Channel, group_name: str):
        lookup = functions.strip_white(group_name)
        group = self.get_group(lookup)
        if group is None:
            await self.bot.send_message(channel, 'Group {} not found'.format(lookup))
            return

        await self.bot.send_message(channel, ' '.join(functions.id_to_mention(member_id) for member_id in group['members']))

    @group.command(pass_context=True)
    async def notify(self, ctx, *, group_name: str):
        """Notifies the members of a group. Can also use @!group_name anywhere in a message."""

        await self._notify(ctx.message.channel, group_name)

    @group.command(pass_context=True, aliases=['add'])
    async def create(self, ctx: commands.Context, group_name: str, *members: discord.Member):
        """Creates a new group controlled by you."""

        lookup = functions.strip_white(group_name)
        if self.get_group(lookup) is not None:
            await self.bot.say('Group {} already exists.'.format(lookup))
            return
        if len(lookup) < 3:
            await self.bot.say('That group name is too short.')
            return

        await self.db.put(lookup,
                          {
                              'owner': ctx.message.author.id,
                              'members': list(set([member.id for member in members]))
                          })
        await self.bot.say('Successfully created group.')

    @group.command(pass_context=True, aliases=['delete'])
    async def remove(self, ctx: commands.Context, *, group_name: str):
        """Removes a group that you control."""

        lookup = functions.strip_white(group_name)
        can_modify = await self.modify_test(lookup, self.get_group(lookup), ctx)

        if can_modify:
            await self.db.remove(lookup)
            await self.bot.say('Removed group.')

    @group.command(pass_context=True, name='list')
    async def _list(self, ctx: commands.Context, member: discord.Member = None):
        """Lists groups with a member in them. If no member is given, lists all groups."""

        if member is None:
            reply = 'All groups: {}'.format(', '.join(sorted(self.db.all())))
        else:
            valid_groups = [group_name for group_name, group_info in self.db.all().items() if
                            member.id in group_info['members']]
            if len(valid_groups) != 0:
                reply = 'Groups {} is in: {}'.format(member.name, ', '.join(sorted(valid_groups)))
            else:
                reply = '{} is in no groups.'.format(member.name)

        await functions.send_long(self.bot, ctx.message.channel, reply)

    @group.command(pass_context=True)
    async def add_member(self, ctx: commands.Context, member: discord.Member, group_name: str):
        """Adds a member to a group that you control."""

        lookup = functions.strip_white(group_name)
        group = self.get_group(lookup)
        can_modify = await self.modify_test(lookup, group, ctx)

        if can_modify:
            await self.db.put(lookup,
                              {
                                  'owner': group['owner'],
                                  'members': list(set(group['members']) | {member.id})
                              })
            await self.bot.say('Added {} to group {}.'.format(member.name, lookup))

    @group.command(pass_context=True, aliases=['delete_member'])
    async def remove_member(self, ctx: commands.Context, member: discord.Member, group_name: str):
        """Removes a member from a group that you control."""

        lookup = functions.strip_white(group_name)
        group = self.get_group(lookup)
        can_modify = await self.modify_test(lookup, group, ctx)

        if can_modify:
            new_members = list(set(group['members']) - {member.id})
            if len(new_members) == 0:
                await self.db.remove(lookup)
                await self.bot.say('No more members left in group. Group deleted.')
            else:
                await self.db.put(lookup,
                                  {
                                      'owner': group['owner'],
                                      'members': new_members
                                  })
                await self.bot.say('Removed {} from group {}.'.format(member.name, lookup))

    @group.command()
    async def info(self, group_name: str):
        """Displays information about a group."""

        lookup = functions.strip_white(group_name)
        group = self.get_group(lookup)
        if group is None:
            await self.bot.say('Group {} not found'.format(lookup))
            return

        await self.bot.say('Group {} is owned by {} and has the members: {}'.format(
            lookup,
            functions.id_to_name(group['owner'], self.bot),
            ', '.join([functions.id_to_name(member_id, self.bot) for member_id in group['members']])
        ))

    @group.command(pass_context=True)
    async def search(self, ctx, query: str):
        """Searches for a group. Query length must be at least 2 characters."""

        query = functions.strip_white(query)
        if len(query) < 2:
            await self.bot.say('Query length must be at least two characters.')
            return

        results = [group_name for group_name in self.db.all() if query in group_name]
        if results:
            await functions.send_long(self.bot, ctx.message.channel, '{} groups found:\n{}'.format(len(results), ', '.join(results)))
        else:
            await self.bot.say('No groups found.')

    async def on_message(self, message: discord.Message):
        if message.content.startswith(self.bot.command_prefix) or message.author.id == self.bot.user.id:
            return

        match = self.notify_regex.search(message.content)
        if match:
            await self._notify(message.channel, match.group(1))


def setup(bot):
    bot.add_cog(Groups(bot))

