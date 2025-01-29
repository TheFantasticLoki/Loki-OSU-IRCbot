from src.bot.command import Command
from ..utils import log

class CustomCommandHandler:
    VALID_COMMANDS = ['socials', 'collections', 'skin', 'about']  # List of registered custom commands
    
    @staticmethod
    async def handle_custom_command(ctx, command_name: str, *args):
        """Template handler for all custom commands"""
        target_user = args[0] if args else ctx.author.name

        # Check for default request
        if args and args[0].lower() in ['loki', 'fantastic_loki']:
            query = """
            SELECT message_content, message_index 
            FROM custom_commands 
            WHERE command_name = ? AND is_default = 1 
            ORDER BY message_index
            """
            params = (command_name,)
        else:
            query = """
            SELECT message_content, message_index 
            FROM custom_commands 
            WHERE user_id = ? AND command_name = ? 
            ORDER BY message_index
            """
            params = (target_user, command_name)

        results = await ctx.database.fetch_all(query, *params)

        if not results:
            return [f"No {command_name} configured for this user."], []

        # Separate immediate and delayed messages
        messages = []
        timeout_messages = []

        for row in results:
            # Access tuple elements by index instead of string keys
            message_index = row[1]  # message_index is second column
            message_content = row[0]  # message_content is first column

            if message_index <= 5:
                messages.append(message_content)
            else:
                delay = 5 + (5 * ((message_index - 6) // 5))
                timeout_messages.append((message_content, delay))
        return messages, timeout_messages

# Register all custom commands
for cmd in CustomCommandHandler.VALID_COMMANDS:
    @Command.register(cmd)
    async def custom_command(ctx, *args, cmd=cmd):
        return await CustomCommandHandler.handle_custom_command(ctx, cmd, *args)
