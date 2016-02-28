import discord
from discord.ext import commands
from .utils import database, checks


def verify_lookup(lookup):
    if '@everyone' in lookup:
        raise RuntimeError('That tag is using blocked words.')
    if not lookup:
        raise RuntimeError('You need to actually pass in a tag name.')
    if len(lookup) > 100:
        raise RuntimeError('Tag name is a maximum of 100 characters.')


class Tags:
    def __init__(self, bot):
        self.bot = bot
        self.db = database.Database('tags.json')

    def get_tag(self, name):
        entry = self.db.get(name, None)
        return entry

    @commands.group(pass_context=True, invoke_without_command=True)
    async def tag(self, ctx, *, name: str):
        """Allows you to tag text for later retrieval.
        If a subcommand is not called, then this will search the tag database
        for the tag requested.
        """

        lookup = name.lower()
        tag = self.get_tag(lookup)
        if tag is None:
            await self.bot.say('Tag "{}" not found.'.format(name))
            return

        await self.bot.say(tag['content'])

    @tag.error
    async def tag_error(self, error, ctx):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.bot.say('You need to give a tag name.')

    @tag.command(pass_context=True, aliases=['add'])
    async def create(self, ctx, name: str, *, content: str):
        """Creates a new tag owned by you."""

        content = content.replace('@everyone', '@\u200beveryone')
        lookup = name.lower().strip()
        try:
            verify_lookup(lookup)
        except RuntimeError as e:
            await self.bot.say(e)
            return

        if lookup in self.db:
            await self.bot.say('A tag with the name of "{}" already exists.'.format(name))
            return

        await self.db.put(lookup, {'owner': ctx.message.author.id, 'content': content})
        await self.bot.say('Tag "{}" successfully created.'.format(lookup))

    @tag.command(pass_context=True)
    async def edit(self, ctx, name: str, *, content: str):
        """Modifies an existing tag you own. Replaces original text."""

        content = content.replace('@everyone', '@\u200beveryone')
        lookup = name.lower().strip()
        tag = self.get_tag(lookup)

        if tag is None:
            await self.bot.say('The tag does not exist.')
            return
        if not (tag['owner'] == ctx.message.author.id or checks.is_owner_check(ctx.message)):
            await self.bot.say('Only the tag or bot owner can edit this tag.')
            return

        await self.db.put(lookup, {'owner': ctx.message.author.id, 'content': content})
        await self.bot.say('Tag successfully edited.')

    @tag.command(pass_context=True, aliases=['delete'])
    async def remove(self, ctx, *, name: str):
        """Removes a tag that you own."""

        lookup = name.lower().strip()
        tag = self.get_tag(lookup)

        if tag is None:
            await self.bot.say('Tag not found.')
            return
        if not (tag['owner'] == ctx.message.author.id or checks.is_owner_check(ctx.message)):
            await self.bot.say('You do not have permissions to delete this tag.')
            return

        await self.db.remove(lookup)
        await self.bot.say('Tag successfully removed.')

    @tag.command(name='list', pass_context=True)
    async def _list(self, ctx):
        """Lists all the tags that belong to you."""

        owner = ctx.message.author.id
        tags = [tag_name for tag_name, tag_info in self.db.all().items() if tag_info['owner'] == owner]

        if tags:
            await self.bot.say('You have the following tags:\n{}'.format(', '.join(tags)))
        else:
            await self.bot.say('You have no tags.')


def setup(bot):
    bot.add_cog(Tags(bot))
