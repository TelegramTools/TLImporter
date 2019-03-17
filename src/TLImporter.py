
import getpass
import logging
import shutil
import sqlite3
import sys
import progressbar  # progressbar2 module
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from telethon.crypto import AuthKey
from telethon.tl.functions.messages import *
from telethon.tl.types import *
from telethon.utils import *
from telethon.sessions import *
import pyAesCrypt
from src.common import *
from src.client import ChatClient
from src.DBManager import DBManager
from src.context import Context

client1 = ChatClient('UserOne')
#  client1 = TelegramClient('User1', api_id, api_hash, device_model=TLdevice_model, system_version=TLsystem_version,
# app_version=TLapp_version, lang_code=TLlang_code, system_lang_code=TLsystem_lang_code)
# TO USE FORWARD 1.0 TELETHON VERSION


def event_handler(event):
    global SecretMessage
    if getattr(event.original_message, 'media', None):
        if isinstance(event.original_message.media, (MessageMediaDocument, Document)):
            for attr in event.original_message.media.document.attributes:
                if isinstance(attr, DocumentAttributeFilename):
                    if attr.file_name == "DB.aes":
                        print("\nResponse received! Processing...")
                        try:
                            os.remove("DB.aes")
                        except Exception as ex:
                            print(str(ex))
                        client1.download_media(event.original_message)
                        SecretMessage = client1.send_message(ChosenChat, "WooHoo!")
                        client1.disconnect()
    return


def start_secret_mode():
    global dialogs, ChosenChat, password, bufferSize, client2, SecretMessage
    getpass.getpass("\n\nYou have chosen to use the Telegram Tool's secret mode for logging your partner "
                    "in Telegram.\nNow, it's time to choose your partner in your chat list. Press ENTER to continue: ")
    print("Gathering your chat list...")
    ChosenChat = client1.get_chat_list()
    dialogs.clear()
    print("\n\nWaiting for a response from your partner...")
    client1.add_event_handler(event_handler, events.NewMessage(chats=ChosenChat, incoming=True))
    # client1.run_until_disconnected() TO USE FORWARD 1.0 TELETHON VERSION
    client1.idle()  # TO USE PRIOR 1.0 TELETHON VERSION
    client1.connect()
    pyAesCrypt.decryptFile("DB.aes", "TempDB.session", password, bufferSize)
    old_db = sqlite3.connect('TempDB.session')
    db = old_db.cursor()
    db.execute('SELECT * FROM sessions')
    List = []
    for row in db:
        List.append(row[0])
        List.append(row[1])
        List.append(row[2])
        List.append(row[3])
    old_db.close()
    try:
        os.remove("DB.aes")
        os.remove("TempDB.session")
    except Exception as exepti:
        print(str(exepti))
    client2 = ChatClient('UserTwo')
    client2.session.set_dc(List[0], List[1], List[2])
    client2.session.auth_key = AuthKey(data=List[3])  # TO USE PRIOR 1.0 TELETHON VERSION
    # client2._sender.state.auth_key = AuthKey(data=List[3])TO USE FORWARD 1.0 TELETHON VERSION
    List.clear()
    client1.start_client()
    client1.remove_event_handler(event_handler, events.NewMessage(chats=ChosenChat, incoming=True))
    client1.delete_messages(ChosenChat, SecretMessage.id, revoke=True)
    client2.start_client()
    print("Secret Mode's Authentication done successfully!")





def commit_messages(database):
    global user1IDs
    global User2IDs
    global self_user1
    global self_user2
    try:
        database.commit()
    except:
        pass
    for id1 in user1IDs:
        reg5 = (id1, None)
        database.execute("INSERT INTO SentMessagesIDs VALUES(?,?)", reg5)
    database.commit()
    looping_count = 0
    for id1 in user1IDs:
        if len(User2IDs) != 0:
            database.execute("UPDATE SentMessagesIDs SET User2={id} WHERE User1={user1id}". \
                             format(user1id=id1, id=User2IDs.pop(0)))
            looping_count = looping_count + 1
        else:
            break
    if len(User2IDs) != 0:
        for id2 in User2IDs:
            reg5 = (None, id2)
            database.execute("INSERT INTO SentMessagesIDs VALUES(?,?)", reg5)
    database.commit()
    return


def check_messages():
    global solo_importing
    global NameUser1
    global NameUser2
    global self_user1
    global self_user2
    global incorrectname
    global LineCount
    global User1Count
    global User2Count
    global ValidFile
    global TotalCount
    print()
    if solo_importing is True:
        NameUser1 = input("Who is one of the partners?: ")
    else:
        NameUser1 = input("Who will be you (+" + self_user1.phone + ") in this chat?: ")
    while True:
        if NameUser1 is None:
            NameUser1 = input(incorrectname)
        if NameUser1 is not None:
            NameUser1 = NameUser1.replace(":", "")
            break
    print()
    if solo_importing is True:
        NameUser2 = input("Who is the other partner?: ")
    else:
        NameUser2 = input("Who will be " + self_user2.first_name + " (+" + self_user2.phone + ") in this chat?: ")
    while True:
        if NameUser2 is None:
            NameUser2 = input(incorrectname)
        if NameUser2 is not None:
            NameUser2 = NameUser2.replace(":", "")
            break
    if solo_importing is True:
        print("\nOne of the partners is " + NameUser1 + " and the other one is " + NameUser2 +
              ". Checking if the file is valid to be imported...\n")
    else:
        print("\nYou are " + NameUser1 + " and your partner (+" + self_user2.phone + ") is " + NameUser2
              + ". Checking if the file is valid to be imported...\n")
        print()
    with open(FilePath, mode="r", encoding="utf-8") as f:
        user1_found = False
        user2_found = False
        for line in f:
            TotalCount = TotalCount + 1
            if line.find(NameUser1 + ":") != -1:
                user1_found = True
                User1Count = User1Count + 1
            elif line.find(NameUser2 + ":") != -1:
                user2_found = True
                User2Count = User2Count + 1
        if TotalCount != (User1Count + User2Count):
            TotalCount = User1Count + User2Count
        if user1_found and user2_found:
            ValidFile = True
        else:
            ValidFile = False
            return


def export_messages():
    global NoTimestamps
    global EndDate
    global self_user2
    global self_user1
    global User2IDs
    global user1IDs
    global TotalCount
    global NameUser2
    global NameUser1
    global RawLoopCount
    global user1
    global user2
    global Filename
    global FilePath
    print("\nYou can cancel at any time pressing CTRL+C keyboard combination.")
    print("\nINFORMATION: Each 2000 messages, a pause of around 7 minutes will be done for reducing Telegram's "
          "flood limits.\nBe patient, the process will be still going on.\n")
    try:
        if solo_importing:
            user1 = self_user1
        else:
            try:
                user2 = client1.get_input_entity(self_user2.phone)
            except:
                client1.get_dialogs(limit=None)
                user2 = client1.get_input_entity(self_user2.id)
            try:
                user1 = client2.get_input_entity(self_user1.phone)
            except:
                client2.get_dialogs(limit=None)
                user1 = client2.get_input_entity(self_user1.id)

        bar = progressbar.ProgressBar(max_value=TotalCount)
        bar.start()
        completed = 0
        database = DBManager.connect()
        if not solo_importing:
            reg1 = (self_user1.id, self_user2.id, self_user1.first_name + " (+" + self_user1.phone + ")", self_user2.first_name + " (+" + self_user2.phone + ")", client1.get_messages(user2, 0).total, client2.get_messages(user1, 0).total, TotalCount, solo_importing)
            welcmsg = client1.send_message(user2, "📲`IMPORTING THE CHAT WITH` __" + NameUser1 + "__ and __" + NameUser2 + "__ using `" + Filename + "` as source file. __'" + NameUser2 + "'__ is **" + self_user2.first_name + "** now.")
        else:
            reg1 = (self_user1.id, None, self_user1.first_name + " (+" + self_user1.phone + ")", None, client1.get_messages(user1, 0).total, None, TotalCount, solo_importing)
            welcmsg = client1.send_message(user2, "📲`IMPORTING THE CHAT WITH` __" + NameUser1 + "__ and __" + NameUser2 + "__ using `" + Filename + "` as source file.")
        reg2 = (NameUser1, NameUser2, Filename, FilePath, solo_importing)
        database.execute("INSERT INTO Statistics VALUES(?,?,?,?,?,?,?,?)", reg1)
        database.execute("INSERT INTO Settings VALUES(?,?,?,?,?)", reg2)
        database.commit()
        user1IDs.append(welcmsg.id)
        if not solo_importing:
            client2.get_incoming_id(user1, 1)
        db = database.cursor()
        db.execute('SELECT * FROM ImportedMessages')
        for row in db:
            out = None
            date = None
            message = None
            sender = None
            my_list = None
            long_message = False
            if row[0] == 0:
                out = False
            else:
                out = True

            if NoTimestamps:
                if solo_importing:
                    sender = "`" + row[1] + ":`\n"
                else:
                    date = None
                    sender = None
            else:
                if solo_importing and EndDate:
                    sender = "`" + row[1] + ":`\n"
                else:
                    sender = None
                if EndDate:
                    date = "`[" + row[2] + "]`"
                elif solo_importing:
                    date = "`[" + row[2] + "] " + row[1] + ":`\n"
                else:
                    date = "`[" + row[2] + "]`\n"
            message = row[3]

            if NoTimestamps:
                if len(message) > 4096:
                    if not solo_importing:
                        n = 4096
                    else:
                        n = 4096 - len(sender)
                    my_list = [message[i:i + n] for i in range(0, len(message), n)]
                elif solo_importing and len(message + sender) > 4096:
                    long_message = True
            else:
                if len(message) > 4096:
                    if not solo_importing:
                        n = 4096 - len(date)
                    else:
                        n = 4096 - len(date) - len(sender)
                    my_list = [message[i:i + n] for i in range(0, len(message), n)]
                elif not solo_importing and len(message + date) > 4096:
                    long_message = True
                elif solo_importing and len(message + date + sender) > 4096:
                    long_message = True

            if my_list is None:
                if long_message:
                    if solo_importing:
                        if NoTimestamps:
                            msg = client1.send_message(user1, sender)
                            msg2 = client1.send_message(user1, message, reply_to=msg.id)
                            user1IDs.append(msg.id)
                            user1IDs.append(msg2.id)
                        else:
                            msg = client1.send_message(user1, date)
                            msg2 = client1.send_message(user1, message, reply_to=msg.id)
                            user1IDs.append(msg.id)
                            user1IDs.append(msg2.id)
                    else:
                        if out:
                            msg = client1.send_message(user2, date)
                            msg2 = client1.send_message(user2, message, reply_to=msg.id)
                            user1IDs.append(msg.id)
                            user1IDs.append(msg2.id)
                        else:
                            msg = client2.send_message(user1, date)
                            msg2 = client2.send_message(user1, message, reply_to=msg.id)
                            User2IDs.append(msg.id)
                            User2IDs.append(msg2.id)
                else:
                    if solo_importing:
                        if NoTimestamps:
                            msg = client1.send_message(user1, sender+message)
                        elif EndDate:
                            msg = client1.send_message(user1, sender + message + date)
                        else:
                            msg = client1.send_message(user1, date + sender + message)
                        user1IDs.append(msg.id)
                    else:
                        if out:
                            if NoTimestamps:
                                msg = client1.send_message(user2, message)
                            elif EndDate:
                                msg = client1.send_message(user2, message + date)
                            else:
                                msg = client1.send_message(user2, date + message)
                            user1IDs.append(msg.id)
                        else:
                            if NoTimestamps:
                                msg = client2.send_message(user1, message)
                            elif EndDate:
                                msg = client2.send_message(user1, message + date)
                            else:
                                msg = client2.send_message(user1, date + message)
                            User2IDs.append(msg.id)
            else:
                loop_count = 0
                IDs = []
                if solo_importing:
                    if NoTimestamps:
                        for m in my_list:
                            if loop_count == 0:
                                msg = client1.send_message(user1, sender + m)
                            else:
                                msg = client1.send_message(user1, sender + m, reply_to=IDs[loop_count - 1])
                            loop_count = loop_count + 1
                            IDs.append(msg.id)
                            user1IDs.append(msg.id)
                    elif EndDate:
                        for m in my_list:
                            if loop_count == 0:
                                msg = client1.send_message(user1, sender + m + date)
                            else:
                                msg = client1.send_message(user1, sender + m + date, reply_to=IDs[loop_count - 1])
                            loop_count = loop_count + 1
                            IDs.append(msg.id)
                            user1IDs.append(msg.id)
                    else:
                        for m in my_list:
                            if loop_count == 0:
                                msg = client1.send_message(user1, date + m)
                            else:
                                msg = client1.send_message(user1, date + m, reply_to=IDs[loop_count - 1])
                            loop_count = loop_count + 1
                            IDs.append(msg.id)
                            user1IDs.append(msg.id)
                else:
                    if out:
                        if NoTimestamps:
                            for m in my_list:
                                if loop_count == 0:
                                    msg = client1.send_message(user2, m)
                                else:
                                    msg = client1.send_message(user2, m, reply_to=IDs[loop_count - 1])
                                loop_count = loop_count + 1
                                IDs.append(msg.id)
                                user1IDs.append(msg.id)
                        elif EndDate:
                            for m in my_list:
                                if loop_count == 0:
                                    msg = client1.send_message(user2, m + date)
                                else:
                                    msg = client1.send_message(user2, m + date, reply_to=IDs[loop_count - 1])
                                loop_count = loop_count + 1
                                IDs.append(msg.id)
                                user1IDs.append(msg.id)
                        else:
                            for m in my_list:
                                if loop_count == 0:
                                    msg = client1.send_message(user2, date + m)
                                else:
                                    msg = client1.send_message(user2, date + m, reply_to=IDs[loop_count - 1])
                                loop_count = loop_count + 1
                                IDs.append(msg.id)
                                user1IDs.append(msg.id)
                    else:
                        if NoTimestamps:
                            for m in my_list:
                                if loop_count == 0:
                                    msg = client2.send_message(user1, m)
                                else:
                                    msg = client2.send_message(user1, m, reply_to=IDs[loop_count - 1])
                                loop_count = loop_count + 1
                                IDs.append(msg.id)
                                User2IDs.append(msg.id)
                        elif EndDate:
                            for m in my_list:
                                if loop_count == 0:
                                    msg = client2.send_message(user1, m + date)
                                else:
                                    msg = client2.send_message(user1, m + date, reply_to=IDs[loop_count - 1])
                                loop_count = loop_count + 1
                                IDs.append(msg.id)
                                User2IDs.append(msg.id)
                        else:
                            for m in my_list:
                                if loop_count == 0:
                                    msg = client2.send_message(user1, date + m)
                                else:
                                    msg = client2.send_message(user1, date + m, reply_to=IDs[loop_count - 1])
                                loop_count = loop_count + 1
                                IDs.append(msg.id)
                                User2IDs.append(msg.id)
                IDs.clear()
                loop_count = 0

            RawLoopCount = RawLoopCount + 1
            completed = completed + 1
            bar.update(completed)
            # For avoiding some flood limits, it seems better to me to also gather the ids of 
            # the messages in the other account
            # instead of doing it when all it's finished.
            if not solo_importing and RawLoopCount == 2000:
                client1.get_incoming_id(user2, 2000)
                client2.get_incoming_id(user1, 2000)
                RawLoopCount = 0
                time.sleep(420)
            elif RawLoopCount == 2000 and solo_importing:
                RawLoopCount = 0
                time.sleep(420)
        if RawLoopCount != 0 and not solo_importing:
            client1.get_incoming_id(user2, RawLoopCount)
            client2.get_incoming_id(user1, RawLoopCount)
            RawLoopCount = 0
        client1.send_read_acknowledge(user2, max_id=0)
        client2.send_read_acknowledge(user1, max_id=0)
        if solo_importing:
            confirm = client1.send_message(user1, "✅ **SUCCESS!!**\nSuccessfully imported **" + str(TotalCount) 
                                           + "** messages. **" + str(User1Count) + "** messages were from `" 
                                           + NameUser1 + "` and **" + str(User2Count) + "** messages were from `" 
                                           + NameUser2 + "`.\nThis chat now contains **" 
                                           + str(client1.get_messages(user1, 0).total) 
                                           + "** messages.\n\nThank you very much for using"
                                             " TLImporter!\n\n**--ferferga** ✅")
            user1IDs.append(confirm.id)
        else:
            confirm = client1.send_message(user2, "✅ **SUCCESS!!**\nSuccessfully imported **" + str(
                TotalCount) + "** messages. **" + str(
                User1Count) + "** messages were from `" + NameUser1 + "` and **" + str(
                User2Count) + "** messages were from `" + NameUser2 + "`.\nThis chat now contains **" +
                                           str(client1.get_messages(user2, 0).total) + "** messages.\n\nThank "
                                                                                       "you very much for using "
                                                                                       "TLImporter!\n\n**--ferferga"
                                                                                       "** ✅")
            user1IDs.append(confirm.id)
            client2.get_incoming_id(user1, 1)
        commit_messages(database)
        bar.finish()
        print("\n\nThe process has been finished correctly!")

    except KeyboardInterrupt:
        print("\nThe process has been cancelled. Saving changes in the database...")
        if RawLoopCount != 0 and not solo_importing:
            client1.get_incoming_id(user2, RawLoopCount)
            client2.get_incoming_id(user1, RawLoopCount)
            RawLoopCount = 0
        commit_messages(database)
        DBManager.connect()
        print(
            "Changes saved! You will be able to use TLRevert to revert the changes made by TLImporter in the "
            "future, and remove all the messages sent by the application.\nYou will need to start from scratch "
            "if you want to continue the merging process later.")
        if SendDatabase is True:
            print("You have chosen to make a copy of your database in your 'Saved Messages' inside Telegram."
                  "\nBacking up database...")
            databasecopy = client1.send_file(self_user1, file="TLImporter-DB.db",
                                             caption="This is the TLImporter's database between " + NameUser1 + " and " + NameUser2)
            client1.send_message(self_user1, "💾 You can read this database using programs like https://github.com"
                                           "/sqlitebrowser/sqlitebrowser/releases. This database is **mandatory**"
                                           " if you want to use [TLRevert](https://github.com/TelegramTools/TLRevert)"
                                           " in order to revert all the changes made by TLImporter. Read the manuals"
                                           " of both programs if you have any doubt about them. **Thank you very much"
                                           " for using** [TLImporter](https://github.com/TelegramTools/TLImporter)"
                                           "**!**\n\n**--ferferga**",
                                 reply_to=databasecopy.id)
        else:
            return
    except Exception as e:
        logging.exception("TLIMPORTER EXCEPTION IN EXPORTINGMESSAGES: " + str(e))
        bar.finish()
        print("Something went wrong in our side. This is the full exception:\n\n"  + str(e))
        print("\nSaving changes in the database, so you can use TLRevert to revert the changes made by TLImporter "
              "and remove all the messages sent by the application...")
        if RawLoopCount != 0 and not solo_importing:
            client1.get_incoming_id(user2, RawLoopCount)
            client2.get_incoming_id(user1, RawLoopCount)
            RawLoopCount = 0
        commit_messages(database)
        DBManager.connect()
        if SendDatabase is True:
            print("You have chosen to make a copy of your database in your 'Saved Messages' inside Telegram."
                  "\nBacking up database...")
            if solo_importing:
                databasecopy = client1.send_file(self_user1, file="TLImporter-DB.db",
                                                 caption="This is the TLImporter's database between " + NameUser1 +
                                                       " and " + NameUser2)
            else:
                databasecopy = client1.send_file(self_user1, file="TLImporter-DB.db",
                                                 caption="This is the TLImporter's database with your partner " +
                                                         self_user2.first_name + "(+" + self_user2.phone + ")")
            client1.send_message(self_user1, "💾 You can read this database using programs like https://github.com"
                                           "/sqlitebrowser/sqlitebrowser/releases. This database is **mandatory** "
                                           "if you want to use [TLRevert](https://github.com/TelegramTools/TLRevert)"
                                            " in order to revert all the changes made by TLImporter. Read the manuals "
                                           "of both programs if you have any doubt about them. **Thank you very much "
                                           "for using** [TLImporter](https://github.com/TelegramTools/TLImporter)"
                                           "**!**\n\n**--ferferga**", reply_to=databasecopy.id)
        getpass.getpass("This part of the process can't be recovered. Press ENTER to close the app...")
        sys.exit(0)

#  ENTRY POINT OF THE CODE


try:
    os.remove("TLImporter-log.log")
except Exception as ex:
    print(str(ex))
logging.basicConfig(filename="TLImporter-log.log", level=logging.DEBUG, format='%(asctime)s %(message)s')
getpass.getpass("HELLO! WELCOME TO TELEGRAM CHAT IMPORTER!\n\nThis app will import your TXT conversations from "
                "third-party apps (like WhatsApp) into your existing Telegram Chat with your partner. \nRead all "
                "the documentation on the GitHub page (https://github.com/TelegramTools/TLImporter/wiki) for all "
                "the important information.\n\nPress ENTER to continue")
getpass.getpass("\n\nWARNING: Telegram allows only a specific and unknown amount of messages within a specific "
                "timeframe for security reasons. You might not be able to message friends for a small period of time."
                "\nThis is known as a 'flood limitation'.\n\nThus, I suggest you to do this at night or in a period "
                "of time that you do not need to use Telegram. Check https://github.com/TelegramTools/TLImporter/wiki"
                "/Before-starting for more information. Press ENTER to continue.")

print("\n\nLogging you into Telegram...")
client1.start_client()
print("\n\nYou are logged in as " + self_user1.first_name + "!")
try:
    os.remove("TLImporter-DB.db")
except Exception as ex:
    print(str(ex))
print("\nCreating database...")
DBManager.connect()
DBManager.create_tables()
while True:
    answer = None
    answer = input("Do you want to import a conversation using two users, in a 1:1 format? Otherwise, the chat "
                   "will be imported inside your 'Saved Messages'. [y/n]: ")
    answer = answer.replace(" ", "")
    answer = answer.upper()
    if not (answer == 'Y' or answer == 'N'):
        while True:
            print()
            answer = input("The command you entered was not valid. Please, enter a valid one: ")
            answer = answer.replace(" ", "")
            answer = answer.upper()
            if (answer == "Y") or (answer == "N"):
                break
    if answer == "Y":
        solo_importing = False
        break
    if answer == "N":
        solo_importing = True
        break
if solo_importing is False:
    print("\n\nNow, you have to log in your partner in Telegram...\n")
    while True:
        answer = None
        answer = input(
            "\nDo you want to log in your partner using the 'Secret Mode'? Refer to the documentation in GitHub "
            "(check https://github.com/TelegramTools/TLSecret as well) for more information. [y/n]: ")
        answer = answer.replace(" ", "")
        answer = answer.upper()
        if not (answer == 'Y' or answer == 'N'):
            while True:
                print()
                answer = input("The command you entered was not valid. Please, enter a valid one: ")
                answer = answer.replace(" ", "")
                answer = answer.upper()
                if (answer == "Y") or (answer == "N"):
                    break
        if answer == "Y":
            SecretMode = True
            break
        if answer == "N":
            SecretMode = False
            break
    if SecretMode:
        start_secret_mode()
    else:
        client2 = ChatClient('UserTwo')
        print("")
        client2.start_client()
    print ("\n\nYour partner is logged in as " + self_user2.first_name + " (+" + self_user2.phone + ")")
    print('\n\nYou are going to copy a conversation from ' + self_user1.first_name + ' (+' + self_user1.phone + ') to '
          + self_user2.first_name + ' (+' + self_user2.phone + ')')
else:
    print("\n\nYou are going to import the conversation in your Telegram's 'Saved Messages' section.")
while True:
    FilePath = input("""\nIt's time to type the path of the file to import. You can also drag and drop it here to 
    get the full path easily.\n\nPath of the file: """)
    if FilePath is None:
        print("You have entered a invalid path. Try again.")
        continue
    else:
        try:
            FilePath = FilePath.replace('"', "")
        except:
            pass
    if not os.path.isfile(FilePath):
        print("You have entered a wrong path, no file could be found. Try again.")
        continue
    else:
        check_messages()
        if ValidFile is True:
            break
        else:
            print(NameUser1 + " and " + NameUser2 + " couldn't be found in " + FilePath + ".\n")
            print("This file is not valid. I'm going to ask you again the filepath and the name of the users."
                  "\nMake sure that you set up everything accordingly. Read the FAQ (https://github.com"
                  "/TelegramTools/TLImporter/wiki/Importing-chats) for more information.")
print("This file is valid to be imported. It has " + str(TotalCount) + " lines in total.")
print("\n" + NameUser1 + " has " + str(User1Count) + " messages. " + NameUser2 + " has " + str(User2Count) 
      + " messages.")
print("\nProcessing and saving messages in the database...")
DBManager.dump()
print("\nSuccessfully completed!")
print("\n\nNow, before importing the chat, we will set up a few settings:\n")
print()
while True:
    print("Here are your current settings:\n")
    if NoTimestamps is True:
        print("> 1. Timestamps settings: Don't add timestamps")
    else:
        print("> 1. Timestamps settings: Add Timestamps")
    if EndDate is True:
        print(">     - Position: End of the message")
    else:
        print(">     - Position: Beginning of the message")
    if AppendHashtag is True:
        print("> 2. Add hashtags to each message: Yes")
    else:
        print("> 2. Add hashtags to each message: No")
    if SendDatabase is True:
        print("> 4. Backup of the database in 'Saved Messages': Yes")
    else:
        print("> 4. Backup of the database in 'Saved Messages': No")
    print()
    print("> Available commands: ")
    print("  !C: Confirm these settings and start the import of the chat")
    print("  !1: See a description and change timestamps settings")
    print("  !2: See a description and change hashtags settings")
    print("  !3: See a description and change Database settings")
    print()
    answer = str(input("Enter a command: "))
    answer = answer.replace(" ", "")
    answer = answer.upper()
    if not (answer == '!C' or answer == '!1' or answer == '!2' or answer == '!3'):
        while True:
            print()
            answer = input("The command you entered was not valid. Please, enter a valid one: ")
            answer = answer.replace(" ", "")
            answer = answer.upper()
            if (answer == "!C") or (answer == "!1") or (answer == "!2") or (answer == "!3"):
                break
    if answer == "!C":
        break
    if answer == "!1":
        Context.append_timestamp(True)
    if answer == "!2":
        Context.append_hashtag(True)
    if answer == "!3":
        Context.send_me_db(True)
print("STARTED! Importing the conversation in Telegram...")
print()
export_messages()
print("\n")
getpass.getpass("Press ENTER to log out: ")
print('Logging ' + self_user1.first_name + ' (+' + self_user1.phone + ') and ' + self_user2.first_name
      + ' (+' + self_user2.phone + ') out of Telegram...')
client1.log_out()
client2.log_out()
print("Thank you very much for using the app!\n\n--ferferga\n\nGOODBYE!")
print()
getpass.getpass("Press ENTER to close the app: ")
sys.exit(0)
