from discord.ext import commands
from .utils import checks
import asyncio
import traceback
import discord


# Shameless lifted from Robo Danny
class REPL:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def cleanup_code(content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @staticmethod
    def get_syntax_error(e):
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def repl(self, ctx: commands.Context):
        """Starts a Python repl session."""
        msg = ctx.message

        repl_locals = {}
        repl_globals = {
            'ctx': ctx,
            'bot': self.bot,
            'message': msg,
            'last': None
        }

        await self.bot.say('Enter code to execute or evaluate. `exit()` or `quit` to exit.')
        while True:
            response = await self.bot.wait_for_message(author=msg.author, channel=msg.channel,
                                                       check=lambda m: m.content.startswith('`'))

            cleaned = self.cleanup_code(response.content)

            if cleaned in ('quit', 'exit', 'exit()'):
                await self.bot.say('Exiting.')
                return

            executor = exec
            if cleaned.count('\n') == 0:
                # single statement, potentially 'eval'
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await self.bot.say(self.get_syntax_error(e))
                    continue

            repl_globals['message'] = response

            fmt = None

            try:
                result = executor(code, repl_globals, repl_locals)
                if asyncio.iscoroutine(result):
                    result = await result
            except Exception as e:
                fmt = '```py\n{}\n```'.format(traceback.format_exc())
            else:
                if result is not None:
                    fmt = '```py\n{}\n```'.format(result)
                    repl_globals['last'] = result

            try:
                await self.bot.send_message(msg.channel, fmt)
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await self.bot.send_message(msg.channel, 'Unexpected error: `{}`'.format(e))


def setup(bot):
    bot.add_cog(REPL(bot))
