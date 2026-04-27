"""
Run PagaL Escrow Bot only
"""
import asyncio
import sys
import types
import os

if sys.version_info >= (3, 13):
    sys.modules["imghdr"] = types.ModuleType("imghdr")

from telegram.ext import MessageHandler, filters

def main():
    escrow_token = os.getenv("ESCROW_BOT_TOKEN")
    if not escrow_token:
        print("❌ ERROR: ESCROW_BOT_TOKEN not set!")
        sys.exit(1)
    
    print("✅ PagaL Escrow Bot (@PagaLEscrowBot) - Starting...")
    
    import escrow_bot
    from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ChatMemberHandler
    
    # Load persistent data on startup
    escrow_bot.load_blacklist()
    escrow_bot.load_global_fee()
    escrow_bot.load_saved_addresses()
    
    app = ApplicationBuilder().token(escrow_token).build()
    
    app.add_handler(CommandHandler("start", escrow_bot.start_command))
    app.add_handler(CommandHandler("menu", escrow_bot.menu_command))
    app.add_handler(CommandHandler("escrow", escrow_bot.escrow_command))
    app.add_handler(CommandHandler("dispute", escrow_bot.dispute_command))
    app.add_handler(CommandHandler("dd", escrow_bot.dd_command))
    app.add_handler(CommandHandler("buyer", escrow_bot.buyer_command))
    app.add_handler(CommandHandler("seller", escrow_bot.seller_command))
    app.add_handler(CommandHandler("token", escrow_bot.token_command))
    app.add_handler(CommandHandler("deposit", escrow_bot.deposit_command))
    app.add_handler(CommandHandler("balance", escrow_bot.balance_command))
    app.add_handler(CommandHandler("addbalance", escrow_bot.addbalance_command))
    app.add_handler(CommandHandler("add", escrow_bot.add_command))
    app.add_handler(CommandHandler("fakedepo", escrow_bot.fakedepo_command))
    app.add_handler(CommandHandler("link", escrow_bot.link_command))
    app.add_handler(CommandHandler("ban", escrow_bot.ban_command))
    app.add_handler(CommandHandler("blacklist", escrow_bot.blacklist_command))
    app.add_handler(CommandHandler("whitelist", escrow_bot.whitelist_command))
    app.add_handler(CommandHandler("close", escrow_bot.close_command))
    app.add_handler(CommandHandler("verify", escrow_bot.verify_command))
    app.add_handler(CommandHandler("id", escrow_bot.id_command))
    app.add_handler(CommandHandler("release", escrow_bot.release_command))
    app.add_handler(CommandHandler("refund", escrow_bot.refund_command))
    app.add_handler(CommandHandler("globalfee", escrow_bot.globalfee_command))
    app.add_handler(CommandHandler("save", escrow_bot.save_command))
    app.add_handler(CommandHandler("empty", escrow_bot.empty_command))
    app.add_handler(CommandHandler("setaddy", escrow_bot.setaddy_command))
    app.add_handler(CallbackQueryHandler(escrow_bot.button_callback))
    app.add_handler(ChatMemberHandler(escrow_bot.track_chat_members, ChatMemberHandler.CHAT_MEMBER))
    # Message handler to capture deal details (Quantity/Amount) after /dd command
    app.add_handler(MessageHandler((filters.TEXT | filters.CAPTION) & ~filters.COMMAND & filters.ChatType.GROUPS, escrow_bot.handle_deal_details_message))
    
    async def post_init(application):
        # Use application.create_task so PTB tracks and cancels it on shutdown
        application.create_task(escrow_bot.monitor_deposits(application))
    
    # Properly stop Pyrogram client on shutdown
    async def post_shutdown(application):
        if escrow_bot.user_client and escrow_bot.user_client.is_connected:
            try:
                await escrow_bot.user_client.stop()
                print("✅ Pyrogram client stopped cleanly")
            except Exception as e:
                print(f"⚠️  Error stopping Pyrogram client: {e}")
    
    app.post_init = post_init
    app.post_shutdown = post_shutdown
    
    print("✅ PagaL Escrow Bot is running...")
    
    # Print configuration diagnostics
    bscscan_key = os.getenv("BSCSCAN_API_KEY", "")
    trongrid_key = os.getenv("TRONGRID_API_KEY", "")
    logs_channel_id = os.getenv("LOGS_CHANNEL_ID", "")
    
    if bscscan_key and trongrid_key:
        print("✅ Blockchain monitoring enabled (BSC & TRON)")
    else:
        print("⚠️  Blockchain monitoring disabled (API keys not configured)")
    
    if logs_channel_id:
        print(f"✅ Logs channel configured: {logs_channel_id}")
    else:
        print("⚠️  Logs channel not configured (LOGS_CHANNEL_ID not set)")
    
    print("✅ Bot is now polling for updates...")
    
    # Include chat_member in allowed_updates to receive member join events
    app.run_polling(allowed_updates=["message", "callback_query", "chat_member", "my_chat_member"])

if __name__ == "__main__":
    main()
