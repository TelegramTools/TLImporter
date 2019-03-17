import progressbar
from src.DBManager import DBManager
from src.context import Context
MAX_MSG_SIZE = 4096


class MessageDispatcher:

    def __init__(self, users, msg_count):
        self.msg_count = msg_count
        self.users = users

    def send_conversation(self, receiver):
        bar = progressbar.ProgressBar(max_value=self.msg_count)
        bar.start()
        completed = 0
        database = DBManager.connect()
        # Load messages from db
        db = database.cursor()
        db.execute('SELECT * FROM ImportedMessages')
        for row in db:
            for u in self.users:
                if row[1].find('] ' + u.name + ':') != -1:  # if one of the users is the sender
                    messages = MessageDispatcher.prepare_msg(row)  # it's a list
                    for msg in messages:
                        u.send_message(receiver, msg)
            completed += 1
            bar.update(completed)
        DBManager.commit()
        bar.finish()
        print("\n\nThe process has been finished correctly!")

    def check_messages(self):
        pass

    @staticmethod
    def prepare_msg(row):
        message = row[3]

        if Context.__append_timestamp__:    # Add timestamp if required
            message += "'[" + row[2] + "]'"

        if Context.__self_importing__:      # If solo mode, append sender's sign
            message += "'-" + row[1] + "'"

        if Context.__hashtag__ is not None:
            message += "'#" + Context.__hashtag__ + "'"

        message_list = []
        if len(message) > 4096:
            message_list = [message[i:i + MAX_MSG_SIZE] for i in range(0, len(message), MAX_MSG_SIZE)]
        else:
            message_list.append(message)
        return message_list
