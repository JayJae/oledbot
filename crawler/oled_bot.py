import telegram

class OledBot() :
    bot = None
    users = []

    def __init__(self) :
        self.bot = telegram.Bot(token='384108295:AAFtxAAVhdFtLTWXWyHvukeQcT2yurZtV9E')

    def get_users(self) :
        updates = self.bot.getUpdates()
        """
        for update in updates :
            print(update.message.chat.id)
            self.users.append(update.message.chat.id)
        """
        self.users = ['410160924', '169412234', '422922822']

    def send_message(self, msg) :
        for user in self.users :
            self.bot.sendMessage(chat_id=user, text=msg)
