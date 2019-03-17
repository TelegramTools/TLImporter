from telethon import TelegramClient
from telethon.errors import FloodWaitError
from src.common import *
import getpass, logging


class ChatClient(TelegramClient):

    def __init__(self, client_name):
        TelegramClient.__init__(client_name, api_id, api_hash, device_model=TLdevice_model,
                                system_version=TLsystem_version, app_version=TLapp_version, lang_code=TLlang_code,
                                system_lang_code=TLsystem_lang_code, spawn_read_thread=False, update_workers=1)
        self.client_instance = None
        self.messages_IDs = []
        self.name = client_name

    def add_message_id(self, msg_id):
        self.messages_IDs.append(msg_id)

    def start_client(self):
        while self.is_connected() is not True:
            try:
                self.connect()
                if not self.is_user_authorized():
                    self.start(force_sms=False)
            except Exception as ex:
                print(ex)
                getpass.getpass(
                    "You are not connected to the internet or the phone was given in the incorrect format. \n"
                    "Check your connection and press ENTER to try again: ")

    def send_message(self, *args, **kwargs):
        send = False
        while send is False:
            try:
                self.send_message(*args, **kwargs)
                send = True
            except FloodWaitError as e:
                logging.exception("TLImporter FLOODEXCEPTION IN SendMessageClient1: " + str(e))
                countdown(e.seconds)
            except Exception as e:
                logging.exception("TLImporter TELEGRAMEXCEPTION IN SendMessageClient1: " + str(e))
                print("\nSomething went wrong in Telegram's side. This is the full exception:\n\n" + str(e))

    def send_file(self, *args, **kwargs):
        send = False
        while send is False:
            try:
                self.send_file(*args, **kwargs, allow_cache=False)
                send = True
            except FloodWaitError as e:
                logging.exception("TLImporter FLOODEXCEPTION IN SendMessageClient1: " + str(e))
                countdown(e.seconds)
            except Exception as e:
                logging.exception("TLImporter TELEGRAMEXCEPTION IN SendMessageClient1: " + str(e))
                print("\nSomething went wrong in Telegram's side. This is the full exception:\n\n" + str(e))

    def get_incoming_id(self, user, limit):
        messages = self.get_messages(user, limit=limit)
        for msg in messages:
            if msg.id not in self.messages_IDs:
                try:
                    self.messages_IDs.append(msg.id)
                except FloodWaitError as e:
                    logging.exception("TLImporter FLOODEXCEPTION IN get_incoming_ID: " + str(e))
                    countdown(e.seconds)
        messages.clear()

    def get_chat_list(self):
        while True:
            dialogs = self.get_dialogs(limit=None)
            i = None
            while i is None:
                print("This is your chat list:\n\n")
                for i, dialog in enumerate(dialogs, start=1):
                    if get_display_name(dialog.entity) is "":
                        name = "Deleted Account"
                    elif isinstance(dialog.entity, InputPeerSelf):
                        name = "Chat with yourself (Saved Messages)"
                    else:
                        name = get_display_name(dialog.entity)
                    sprint('{}. {}'.format(i, name))

                print()
                print('> Who is your partner?')
                print('> Available commands:')
                print('  !q: Quits the dialogs window and exits.')
                print('  !l: Logs out, terminating this session.')
                print()
                i = input('Enter dialog ID or a command to continue: ')
                if i is None:
                    continue
                if i == '!q':
                    sys.exit()
                if i == '!l':
                    client1.log_out()
                    sys.exit()
            try:
                i = int(i if i else 0) - 1
                # Ensure it is inside the bounds, otherwise retry
                dialog_count = dialogs.total
                if not 0 <= i < dialog_count:
                    i = None
            except Exception as ex:
                i = None
                print("That's not a valid Chat. Please, try again.")
                continue

                # Retrieve the selected user (or chat, or channel)
            return dialogs[i].entity