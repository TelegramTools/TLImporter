<p align="center">
  <img src="https://github.com/TelegramTools/TLImporter/raw/python/images/Intro.png">
 </p>
<p align="center">
  <img src="https://github.com/TelegramTools/TLSecret/raw/master/images/SecretModeLabel.png">
 </p>

# TLImporter - Telegram Chat Importer

This app will import your conversations from WhatsApp or other services (using a _txt_ file obtained from the chat provider) into Telegram. With TLImporter you can import your messages into your "Saved Messages" section or do it in a 1:1 format. That means that you will need to log in your partner's Telegram's account inside TLImporter and it will automatically send the corresponding messages to each other, keeping the original structure.

Briefly, Telegram Chat Importer can turn your exported plaintext conversations into a 1:1 format like this:

![](/images/txt.PNG)

Into this:

![](/images/ImportedChat.PNG)

## How to use?

Easy! Start over [here](https://github.com/TelegramTools/TLImporter/wiki/Getting-your-chats-from-third-party-services) and follow the steps in the guide. You will be a master using the app in seconds!

## Documentation

You can check the full documentation, examples, building instructions, FAQs and a detailed guide in [the wiki](https://github.com/TelegramTools/TLImporter/wiki)

## Download

You can always grab the latest version heading over the [releases tab](https://github.com/TelegramTools/TLImporter/releases).
I built binaries for **Windows (64 bits)**, **Linux amd64** and **Linux armhf**

* On **Windows**: Simply double click on the ``.exe`` file
* On **Linux**: Download the binary, ``cd`` to the folder where the download is located and do ``./TLImporter-xxx``

If you're running other systems (like MacOS), you will need to **build the files from source**.

## Build from sources

Make sure that you replace the ``api_id`` and ``api_hash`` variables in the ``TLImporter.py`` file.
Read instructions [here](https://core.telegram.org/api/obtaining_api_id) for getting your own from Telegram.

You can't use Secret Mode if one of the sides is still using the binaries: I'm the only holder of the encryption key, so it's more
difficult for malicious people to compromise them. If you want to use the *Secret Mode*, you must build both TLImporter and TLSecret from
sources using the same password for it to work. You can specify the password used for encryption/decryption in the ``password`` variable.

## Credits

This couldn't be possible without [Telethon](https://github.com/LonamiWebs/Telethon), and his great creator, [Lonami](https://github.com/Lonami), who always was up to answering questions and helping in development. I'm so grateful for his patience :).

And also without [PyInstaller](https://www.pyinstaller.org/) which I used to build the Windows binaries.

Also, huge acknowledgements to Telegram for making such a great messenger!

**Give always credits to all the original authors and owners when using some parts of their hard work in your own projects**
