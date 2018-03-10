using System;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.InteropServices;

namespace TLImporter
{
    class ImporterApp
    {
        [DllImport("kernel32.dll", ExactSpelling = true)]
        private static extern IntPtr GetConsoleWindow();
        private static IntPtr ThisConsole = GetConsoleWindow();
        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        private const int HIDE = 0;
        private const int MAXIMIZE = 3;
        internal const int apiId = xxxxx; //Insert your apiID here
        internal const string apiHash = "XXXXXXXXXXXXXXXXXXXX"; //Insert your apiHash here
        internal static string filePath;
        internal static string NameUser1;
        internal static string NameUser2;
        internal static bool FileIsValid;
        internal static bool ConfirmationConfirmed = false;
        internal static bool AllIsImported = false;
        internal static string incorrectName = "This name is not valid. Please, try again, with a correct name: ";
        internal static bool UploadTXT = false;
        internal static bool NotChosenUser = false;
        internal static void Main()
        {
            Console.WriteLine("Loading Telegram Chat Importer...");
            Console.SetWindowSize(Console.LargestWindowWidth, Console.LargestWindowHeight);
            ShowWindow(ThisConsole, MAXIMIZE);
            Run();
        }
        internal static void Run()
        {
            Console.WriteLine("HELLO! WELCOME TO TELEGRAM CHAT IMPORTER!\n\nThis app will import your TXT conversations from third-party apps (like WhatsApp) into your existing Telegram Chat with your partner. \nRead all the documentation for all the important information.");
            if (File.Exists(@"sessionUser1.dat"))
            {
                File.Delete(@"sessionUser1.dat");
            }
            if (File.Exists(@"sessionUser2.dat"))
            {
                File.Delete(@"sessionUser2.dat");
            }
            Console.WriteLine("Take in mind that this app might trigger flood limits in your account. See https://github.com/TelegramTools/TLImporter/wiki/Before-starting for more information.");
            Console.WriteLine("\n\nYou must log in two users in order to import a conversation.");
            Console.WriteLine("Logging in User 1...");
            Auth.AuthUser1().Wait();
            Console.WriteLine("Logging in User 2...");
            Auth.AuthUser2().Wait();
            while (!AllIsImported)
            {
                Console.WriteLine("\nNow, please, type the complete path of the TXT file you want to import. You can also drag-and-drop it here.\n\nFILEPATH MUST NOT INCLUDE SPACES");
                filePath = Console.ReadLine();
                while (filePath.Contains(" "))
                {
                    Console.WriteLine("The filepath contains an space. Please, make sure that there aren't spaces in the filepath and try again: ");
                    filePath = Console.ReadLine();
                    if (!filePath.Contains(" "))
                    {
                        break;
                    }
                }
                CheckUsers();
                while (!ImporterApp.FileIsValid)
                {
                    Console.WriteLine("We couldn't find " + NameUser1 + " and " + NameUser2 + " in this file.\n\nPlease, check the documentation at https://github.com/TelegramTools/TLImporter to make sure that you are doing eveything right.\n\n");
                    AskConfirmation("Do you want to try again or close the app? (Yes, for trying again. No, for closing the app [y/n]", false, false, false);
                    if (!ConfirmationConfirmed)
                    {
                        Environment.Exit(0);
                    }
                    else
                    {
                        CheckUsers();
                        ConfirmationConfirmed = false;
                    }
                }
                Console.WriteLine("This file is valid to be imported. Counting the number of messages...");
                TextHandler.TotalLines();
                Console.WriteLine("The file has " + TextHandler.TotalCount + " lines.");
                TextHandler.UserLines(NameUser1, false);
                Console.WriteLine("\n\n" + NameUser1 + " has " + TextHandler.CountedLines1 + " messages.");
                TextHandler.UserLines(NameUser2, true);
                Console.WriteLine(NameUser2 + " has " + TextHandler.CountedLines2 + " messages.");
                AskConfirmation("Do you also want to upload to the chat the TXT file used? [y/n]", false, true, false);
                ConfirmationConfirmed = false;
                Console.WriteLine("Making sure that everything is ready for the import process... This will take nanoseconds :)");
                {
                    if (NameUser1.Contains(":"))
                    {
                        NameUser1.Replace(":", "");
                    }
                    if (NameUser2.Contains(":"))
                    {
                        NameUser2.Replace(":", "");
                    }
                    if (filePath == null | TextHandler.TotalCount == null | TextHandler.CountedLines1 == null | TextHandler.CountedLines2 == null | NameUser1 == null | NameUser2 == null | Auth.phone1 == null | Auth.phone2 == null | Messaging.User1Id == 0 | Messaging.User2Id == 0 | FileIsValid == false | ConfirmationConfirmed == true | AllIsImported == true)
                    {
                        Console.WriteLine("\nSomething went wrong and the app can't recover the process. You will need to start over. Press ENTER to exit and try again.");
                        Console.ReadLine();
                        Environment.Exit(0);
                    }
                    else
                    {
                        AskConfirmation("\nEverything is ready for the import process. Start? [y/n]", true, false, false);
                        ConfirmationConfirmed = false;
                        Messaging.MessageUser2("BEGGINING OF THE IMPORT OF " + filePath, false).Wait();
                        TextHandler.ParseStrings();
                        Messaging.MessageUser2("END OF THE IMPORT OF " + filePath + "\n\nA total of " + TextHandler.TotalCount + " messages were imported successfully.\n\n" + NameUser1 + " has " + TextHandler.CountedLines1 + " imported messages.\n" + NameUser2 + " has " + TextHandler.CountedLines2 + " imported messages.\n\nImported using Telegram Chat Importer. Available at https://github.com/TelegramTools/TLImporter", false).Wait();
                        if (UploadTXT)
                        {
                            Messaging.UploadFile().Wait();
                        }
                        Messaging.MarkMessagesAsRead().Wait();
                        Console.WriteLine("SUCCESS!! All the messages were imported succesfully!");
                        AskConfirmation("Do you want to import another file?. Otherwise, data will be cleared. [y/n]", false, false, true);
                        ConfirmationConfirmed = false;
                        if (NotChosenUser)
                        {
                            NotChosenUser = false;
                        }
                    }
                }
            }
            Console.WriteLine("\n\nThank you for using this app. If you like it, please, star the GitHub repository :D at https://github.com/TelegramTools/TLImporter \n\nPress ENTER to exit.");
            Console.ReadLine();
            Environment.Exit(0);
        }
        public static void CheckUsers()
        {
            Console.WriteLine("Who is User 1? (" + Auth.phone1 + ")");
            NameUser1 = Console.ReadLine();
            while (String.IsNullOrEmpty(NameUser1))
            {
                Console.WriteLine(incorrectName);
                NameUser1 = Console.ReadLine();
            }
            Console.WriteLine("Who is User 2? (" + Auth.phone2 + ")");
            NameUser2 = Console.ReadLine();
            while (String.IsNullOrEmpty(NameUser2))
            {
                Console.WriteLine(incorrectName);
                NameUser2 = Console.ReadLine();
            }
            Console.WriteLine("User 1 is " + NameUser1 + " and User 2 is " + NameUser2 + ". Checking if the file is valid to be imported...");
            TextHandler.FindUsers();
        }
        public static void AskConfirmation(string Key, bool repeat, bool UploadFile, bool logOut)
        {
            while (!ConfirmationConfirmed)
            {
                Console.WriteLine(Key);
                string option = Console.ReadLine();
                if (option == "y" || option == "Y")
                {
                    if (UploadFile)
                    {
                        UploadTXT = true;
                    }
                    if (logOut)
                    {
                        ChooseUsers();
                    }
                    ConfirmationConfirmed = true;
                }
                if (option == "n" || option == "N")
                {
                    if (logOut)
                    {
                        if (File.Exists(@"sessionUser1.dat"))
                        {
                            File.Delete(@"sessionUser1.dat");
                        }
                        if (File.Exists(@"sessionUser2.dat"))
                        {
                            File.Delete(@"sessionUser2.dat");
                        }
                        AllIsImported = true;
                    }
                    if (UploadFile)
                    {
                        UploadTXT = false;
                    }
                    if (!repeat)
                    {
                        break;
                    }
                    else
                    {
                        Console.WriteLine("You cancelled this. You will be asked again by pressing ENTER. Close the app if you don't want to be asked again.");
                        Console.ReadLine();
                    }
                    ConfirmationConfirmed = false;
                }
            }
            return;
        }
        public static void ChooseUsers()
        {            
            while (!NotChosenUser)
            {
                Console.WriteLine("OK. Which Telegram users do you want to use for the next file? Both logged users (B), only User 1 (1) or only User 2 (2)? [B/1/2]: ");
                string option = Console.ReadLine();
                if (option == "b" || option == "B")
                {
                    NotChosenUser = true;
                }
                if (option == "1")
                {
                    Console.WriteLine("Logging out User 2...");
                    if (File.Exists(@"sessionUser2.dat"))
                    {
                        File.Delete(@"sessionUser2.dat");
                    }
                    Console.WriteLine("Now, you will be asked to log in a new User 2. Press ENTER to continue");
                    Console.ReadLine();
                    Auth.AuthUser2().Wait();
                    NotChosenUser = true;
                }
                if (option == "2")
                {
                    Console.WriteLine("Logging out User 1...");
                    if (File.Exists(@"sessionUser1.dat"))
                    {
                        File.Delete(@"sessionUser1.dat");
                    }
                    Console.WriteLine("Now, you will be asked to log in a new User 1. Press ENTER to continue");
                    Console.ReadLine();
                    Auth.AuthUser1().Wait();
                    NotChosenUser = true;
                }
            }
            return;
        }
    }
}
