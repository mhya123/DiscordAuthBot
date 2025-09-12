from discord import app_commands, Interaction

class BasicCommands(app_commands.Group, name="basic", description="Basic utility commands"):
    @app_commands.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message("Pong! 🏓", ephemeral=True)

    @app_commands.command(name="echo", description="Echo the provided text")
    @app_commands.describe(text="Text to echo back")
    async def echo(self, interaction: Interaction, text: str):
        if not text:
            await interaction.response.send_message("Please provide text to echo.", ephemeral=True)
            return
        await interaction.response.send_message(text)

    @app_commands.command(name="help", description="Show help information")
    async def help(self, interaction: Interaction):
        content = (
            "Available commands:\n"
            "- /basic ping — check bot\n"
            "- /basic echo <text> — echo back text\n"
            "- /basic help — this message"
        )
        await interaction.response.send_message(content, ephemeral=True)
