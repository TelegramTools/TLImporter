# What you will need

* VS 2017 Community with .NET Framework 4.5 installed

# Dependencies

This project only depends on TLSharp and its references. They will be downloaded automatically from NuGet after opening the project and building from sources.

# Setting up

- Create your working directory and name it whatever you want.

- Download my fork of TLSharp [here](https://github.com/TelegramTools/TLSharp). Extract them in the root of your working directory.

- Download the sources of TLImporter and extract the contents inside the **src** folder in the root of your working directory.

- Open ``Program.cs`` file and edit the following lines:

``internal const int apiId = XXXXX; //Insert your apiID here``

``internal const string apiHash = "XXXXXXXXXXXXXXXXXXX"; //Insert your apiHash here``

You must obtain your apiID and apiHash from Telegram. Read [the official documentation from Telegram](https://core.telegram.org/api/obtaining_api_id) to get started.

Now, you are ready to build the app yourself.
