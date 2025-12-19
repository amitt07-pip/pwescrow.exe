#!/usr/bin/env python3
"""
Telethon Session String Generator
This script helps you generate a string session for the escrow bot.
Run this in the Shell (not the workflow) to avoid conflicts.
"""

import os
from telethon import TelegramClient
from telethon.sessions import StringSession

# Get credentials from environment or prompt
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

if not API_ID or not API_HASH:
    print("❌ Error: TELEGRAM_API_ID and TELEGRAM_API_HASH must be set in Secrets")
    print("Please add these secrets first, then run this script again.")
    exit(1)

print("=" * 60)
print("TELETHON SESSION STRING GENERATOR")
print("=" * 60)
print()
print("This script will:")
print("1. Connect to Telegram using your phone number")
print("2. Send a verification code to your Telegram app")
print("3. Generate a STRING SESSION for the bot")
print()
print("⚠️  IMPORTANT:")
print("   - You will receive a code in your Telegram app")
print("   - If you have 2FA, you'll need your password")
print("   - The session string is VERY LONG - copy it completely")
print()

async def main():
    # Create client with StringSession
    client = TelegramClient(StringSession(), int(API_ID), API_HASH)
    
    await client.start()
    
    # Get the session string
    session_string = client.session.save()
    
    print()
    print("=" * 60)
    print("✅ SUCCESS! Your Telethon session string is:")
    print("=" * 60)
    print()
    print(session_string)
    print()
    print("=" * 60)
    print()
    print("NEXT STEPS:")
    print("1. COPY the entire session string above (it's very long!)")
    print("2. Go to Replit Secrets (🔒 icon in left sidebar)")
    print("3. DELETE the old 'TELEGRAM_SESSION_STRING' if it exists")
    print("4. CREATE NEW secret:")
    print("   - Key: TELEGRAM_SESSION_STRING")
    print("   - Value: (paste the session string)")
    print("5. Restart the bot workflow")
    print()
    print("=" * 60)
    
    await client.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
