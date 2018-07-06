<p align="center">
  <img src="https://github.com/TelegramTools/TLImporter/raw/python/images/Intro.png">
 </p>

# Version 2.5.4

- Added Solo Importing: Now you can import your chats inside the "Saved Messages" section of your Telegram account.
- Now the file that is being imported will be locked while the app is working with it, so you don't accidentally delete it or remove it, crashing the app.
- Fixed typos
- Improved overall performance.
- Fancy colors that make the app beautiful and friendlier :)
- An even fancier progress bar that will keep you updated of the progress
- Added an "--advanced" command line parameter that will display detailed output while importing into Telegram, confirming you every time that a message has been sent.
- Better error handling.

# Version 3.0

- The app is now written in Python! This means that it is cross-platform now and can be used in other systems, like Mac and Linux
- That means that it is a completely new app, and all the bugs that the old version might had are now gone. But perhaps some new ones appeared, but I don't hope so :(
- Now, you have settings to do before importing the chat: You can choose to add a hashtag to each message sent in your chat by TLImporter (so you can easily search them on),
also, you can choose between adding timestamps or not, and it's position.
- Now, the app stores the messages and their data in a database. That enables you to remove the messages created by TLImporter or other Telegram Tools apps using
[TLRevert](https://github.com/TelegramTools/TLRevert), whenever you can.
- That database is also a great copy of your imported chat, so you can remove the original txt file and keep the database :)
- You can also backup that database, using the app, inside your "Saved Messages" section of your Telegram's account :). You will never lose a thing.
- The app doesn't use colors now (for the sake of accesibility), but now the progress bars are much cooler and work much better.
- In general, this can be considered as the final version of TLImporter, as it's really stable.
- Much faster at sending messages. Also, it should raise less FloodWaits, as it will pause for 7 minutes to make sure Telegram doesn't warn us so frequently.
([Read this](https://github.com/TelegramTools/TLImporter/wiki/FAQ) for more information)
- Oh, and talking about Flood Limits! Now, there is a fancy countdown that tells you how much you have to wait when you are flood limited :).
- Removed the --advanced parameter.
- Added the new Telegram Tools' "Secret Mode"!: In old versions of TLImporter, you must ask your partner his phone number, his code and his password, and he need to trust you,
because after giving that data away to you, you could do with it whatever you want. Now, with Telegram Tool's Secret Mode, your partner has the complete control of the login and authentication process.