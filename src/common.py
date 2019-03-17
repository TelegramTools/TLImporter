

try:
    import cryptg
    from cryptg import *
except:
    pass
import time, datetime


api_id = YOUR_API_ID_HERE
api_hash = 'YOUR_API_HASH_HERE'
TLdevice_model = 'Desktop device'
TLsystem_version = 'Console'
TLapp_version = '- TLImporter 3.0.2'
TLlang_code = 'en'
TLsystem_lang_code = 'en'
self_user1 = None
user1 = None
user2 = None
self_user2 = None
user1IDs = []
User2IDs = []
NoTimestamps = False
AppendHashtag = False
SendDatabase = True
SecretMode = False
EndDate = True
ExceptionReached = False
solo_importing = False
ValidFile = False
Hashtag = "\n#TLImporter"
FilePath = None
NameUser1 = None
NameUser2 = None
incorrectname = "This name is not valid. Please, try again, with a correct name: "
LineCount = 0
User1Count = 0
User2Count = 0
TotalCount = 0
RawLoopCount = 0
Filename = None
client2 = None
dialogs = None
ChosenChat = None
password = "PASSWORD_FOR_SECRET_MODE"
bufferSize = 64 * 1024
SecretMessage = None


def countdown(t):
    print("\n\n")
    print('--> We have reached a flood limitation. Waiting for: ' + str(datetime.timedelta(seconds=t)))
    time.sleep(t)


def sprint(string, *args, **kwargs):
    # Safe Print (handle UnicodeEncodeErrors on some terminals)
    try:
        print(string, *args, **kwargs)
    except UnicodeEncodeError:
        string = string.encode('utf-8', errors='ignore')\
                       .decode('ascii', errors='ignore')
        print(string, *args, **kwargs)
