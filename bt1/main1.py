from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from student_Dung import Dung
from student_Long import Long

# Create instances of students
students = {
    "Dung": Dung(),
    "Long": Long()
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = """
🤖 **Welcome to the Student Info Bot!**

You can interact with the following commands:

/start - Display this help message.
/student <name> - Get details about a specific student. Example: `/student Dung`
/list_students - List all available students.

🔍 **Example Usage:**
- `/student Dung`
- `/student An`

Type a command to begin!
"""
    await update.message.reply_text(help_message, parse_mode="Markdown")


async def student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Please provide a student's name. Example: /student Dung")
        return

    student_name = context.args[0]
    if student_name in students:
        student = students[student_name]
        response = (
            f"👤 **Name:** {student.name()}\n"
            f"💬 **Speak:** {student.speak()}\n"
            f"🏠 **Address:** {student.address()}\n"
            f"📲 **Telegram ID:** {student.telegram_id()}"
        )
        await update.message.reply_text(response)
    else:
        await update.message.reply_text(f"No student found with the name '{student_name}'.")


# Main function to run the bot
# Done! Congratulations on your new bot. You will find it at t.me/K64_chuyende2_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.
#
# Use this token to access the HTTP API:
# 7718470610:AAFSLzaJjsLk5hgFkV86WX8MbhEcdiILtnY
# Keep your token secure and store it safely, it can be used by anyone to control your bot.
#
# For a description of the Bot API, see this page: https://core.telegram.org/bots/api
def main():
    bot_token = "7718470610:AAFSLzaJjsLk5hgFkV86WX8MbhEcdiILtnY"
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("student", student))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

