import discord

def get_bot_token():
    # Prompt the user for the bot token
    return input("Enter your bot token: ")

def main():
    # Get the bot token from the user
    token = get_bot_token()

    # Create a new instance of the Discord client
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user.name} ({client.user.id})')

    # Log in using the provided token
    client.run(token)

if __name__ == "__main__":
    main()

