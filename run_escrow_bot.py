"""
Run PagaL Escrow Bot only
"""
import sys
import types
import os

if sys.version_info >= (3, 13):
    sys.modules["imghdr"] = types.ModuleType("imghdr")


def main():
    escrow_token = os.getenv("ESCROW_BOT_TOKEN")
    if not escrow_token:
        print("❌ ERROR: ESCROW_BOT_TOKEN not set!")
        sys.exit(1)

    print("✅ PagaL Escrow Bot (@PagaLEscrowBot) - Starting...")

    # Delegate to escrow_bot.main() so this entrypoint always has the full,
    # up-to-date handler set (e.g. /manual, response delay, service-message
    # cleanup). Registering handlers here separately caused them to drift.
    import escrow_bot
    escrow_bot.main()


if __name__ == "__main__":
    main()
