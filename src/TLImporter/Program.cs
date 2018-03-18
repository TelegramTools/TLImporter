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
        internal static IntPtr ThisConsole = GetConsoleWindow();
        [DllImport("user32.dll")]
        public static extern int DeleteMenu(IntPtr hMenu, int nPosition, int wFlags);
        [DllImport("user32.dll")]
        internal static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        [DllImport("user32.dll")]
        private static extern IntPtr GetSystemMenu(IntPtr hWnd, bool bRevert);
        private const int HIDE = 0;
        internal const int MAXIMIZE = 3;
        private const int MINIMIZE = 6;
        private const int RESTORE = 9;
        private const int MF_BYCOMMAND = 0x00000000;
        public const int SC_CLOSE = 0xF060;
        public const int SC_MINIMIZE = 0xF020;
        public const int SC_MAXIMIZE = 0xF030;
        public const int SC_SIZE = 0xF000;
        internal const int apiId = //INSERT YOUR APIid HERE//;
        internal const string apiHash = "//INSERT YOUR APIHASH HERE//";
        internal static string filePath;
        internal static string NameUser1;
        internal static string NameUser2;
        internal static bool FileIsValid;
        internal static bool ConfirmationConfirmed = false;
        internal static bool SoloImporting = true;
        internal static bool AllIsImported = false;
        internal static string incorrectName = "This name is not valid. Please, try again, with a correct name: ";
        internal static bool UploadTXT = false;
        internal static bool NotChosenUser = false;
        internal static bool printResult = false;
        internal static void Main(string[] args)
        {
            Console.BackgroundColor = ConsoleColor.DarkYellow;
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("Loading Telegram Chat Importer...");
            Console.ResetColor();
            if (File.Exists(@"sessionUser1.dat"))
            {
                File.Delete(@"sessionUser1.dat");
            }
            if (File.Exists(@"sessionUser2.dat"))
            {
                File.Delete(@"sessionUser2.dat");
            }
            string param1 = args.SingleOrDefault(arg => arg.Contains("--advanced"));
            if (param1 == "--advanced")
            {
                printResult = true;
            }
            DeleteMenu(GetSystemMenu(GetConsoleWindow(), false), SC_SIZE, MF_BYCOMMAND);
            Console.SetWindowSize(Console.LargestWindowWidth, Console.LargestWindowHeight);
            ShowWindow(ThisConsole, MAXIMIZE);
            Run();
        }
        internal static void Run()
        {
            Console.Clear();
            if (printResult)
            {
                Console.BackgroundColor = ConsoleColor.Yellow;
                Console.ForegroundColor = ConsoleColor.DarkRed;
                Console.WriteLine("ADVANCED MODE ENABLED: This will print detailed output while importing the chat.\n\n");
                Console.ResetColor();
            }
            Console.BackgroundColor = ConsoleColor.Blue;
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("HELLO! WELCOME TO TELEGRAM CHAT IMPORTER!\n\nThis app will import your TXT conversations from third-party apps (like WhatsApp) into your existing Telegram Chat with your partner. \nRead all the documentation on the GitHub page (https://github.com/TelegramTools/TLImporter/wiki) for all the important information.\n\nPress ENTER to continue");
            Console.ReadLine();
            Console.ForegroundColor = ConsoleColor.White;
            Console.BackgroundColor = ConsoleColor.DarkCyan;
            AskConfirmation("\nWARNING: Telegram allows only a specific and unknown amount of messages within a specific timeframe for security reasons. You might not be able to message friends for a small period of time.\nThis is known as a 'flood limitation'.\n\nThus, I suggest you to do this at night or in a period of time that you do not need to use Telegram. Check https://github.com/TelegramTools/TLImporter/wiki/Before-starting for more information.\n\nType, exactly, 'I UNDERSTOOD', to continue:", true, true, "I UNDERSTOOD");
            ConfirmationConfirmed = false;
            Console.ResetColor();
            Console.WriteLine("Logging you in Telegram...");
            Auth.AuthUser1().Wait();
            AskConfirmation("Do you want to import a conversation using two users, in a 1:1 format? Otherwise, the chat will be imported inside your 'Saved Messages'. [y/n]: ", false);
            if (ConfirmationConfirmed)
            {
                SoloImporting = false;
                ConfirmationConfirmed = false;
            }
            else
            {
                SoloImporting = true;
                ConfirmationConfirmed = false;
            }
            if (!SoloImporting)
            {
                Auth.AuthUser2().Wait();
            }
            while (!AllIsImported)
            {
                NotChosenUser = false;
                Console.Write("\n\nNow, please, type the complete path of the TXT file you want to import. You can also drag-and-drop it here.\n\nFILEPATH MUST NOT INCLUDE SPACES: ");
                filePath = Console.ReadLine();
                while (filePath.Contains(" "))
                {
                    Console.Write("\n\nThe filepath contains an space. Please, make sure that there aren't spaces in the filepath and try again: ");
                    filePath = Console.ReadLine();
                    if (!filePath.Contains(" "))
                    {
                        break;
                    }
                }
                CheckUsers();
                while (!ImporterApp.FileIsValid)
                {
                    Console.BackgroundColor = ConsoleColor.Red;
                    Console.ForegroundColor = ConsoleColor.Black;
                    Console.WriteLine("We couldn't find " + NameUser1 + " and " + NameUser2 + " in this file.\n\nPlease, check the documentation at https://github.com/TelegramTools/TLImporter to make sure that you are doing eveything right.\n\n");
                    Console.ResetColor();
                    AskConfirmation("Do you want to try again or close the app? (Yes (y), for trying again. No (n), for closing the app) [y/n]: ", false);
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
                Console.BackgroundColor = ConsoleColor.Green;
                Console.ForegroundColor = ConsoleColor.Black;
                Console.WriteLine("\nThis file is valid to be imported. Counting the number of messages...");
                Console.ResetColor();
                TextHandler.TotalLines();
                Console.WriteLine("The file has " + TextHandler.TotalCount + " lines.");
                TextHandler.UserLines(NameUser1, false);
                Console.WriteLine("\n" + NameUser1 + " has " + TextHandler.CountedLines1 + " messages.");
                TextHandler.UserLines(NameUser2, true);
                Console.WriteLine(NameUser2 + " has " + TextHandler.CountedLines2 + " messages.");
                AskConfirmation("Do you also want to upload to the chat the TXT file used? [y/n]: ", false);
                if (ConfirmationConfirmed)
                {
                    UploadTXT = true;
                    ConfirmationConfirmed = false;
                }
                else
                {
                    UploadTXT = false;
                    ConfirmationConfirmed = false;
                }
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
                    TextHandler.CurrentMessage = 0;
                    if (SoloImporting)
                    {
                        if (filePath == null | TextHandler.TotalCount == null | TextHandler.CountedLines1 == null | TextHandler.CountedLines2 == null | NameUser1 == null | NameUser2 == null | Auth.phone1 == null | Messaging.User1Id == 0 | FileIsValid == false | ConfirmationConfirmed == true | AllIsImported == true)
                        {
                            Console.WriteLine("\nSomething went wrong and the app can't recover the process. You will need to start over. Press ENTER to exit and try again.");
                            Console.ReadLine();
                            Environment.Exit(0);
                        }
                    }
                    else if (filePath == null | TextHandler.TotalCount == null | TextHandler.CountedLines1 == null | TextHandler.CountedLines2 == null | NameUser1 == null | NameUser2 == null | Auth.phone1 == null | Auth.phone2 == null | Messaging.User1Id == 0 | Messaging.User2Id == 0 | FileIsValid == false | ConfirmationConfirmed == true | AllIsImported == true)
                    {
                        Console.WriteLine("\nSomething went wrong and the app can't recover the process. You will need to start over. Press ENTER to exit and try again.");
                        Console.ReadLine();
                        Environment.Exit(0);
                    }
                    AskConfirmation("\nEverything is ready for the import process.\nREMEMBER: You might trigger flood limits in your account. Read https://github.com/TelegramTools/TLImporter/wiki/Before-starting for more information.\n\nStart? [y/n]: ", true);
                    ConfirmationConfirmed = false;
                    Console.WriteLine("");
                    Messaging.MessageUser2("BEGINNING OF THE IMPORT OF " + filePath, false).Wait();
                    TextHandler.ParseStrings();
                    Messaging.MessageUser2("END OF THE IMPORT OF " + filePath + "\n\nA total of " + TextHandler.TotalCount + " messages were imported successfully.\n\n" + NameUser1 + " has " + TextHandler.CountedLines1 + " imported messages.\n" + NameUser2 + " has " + TextHandler.CountedLines2 + " imported messages.\n\nImported using Telegram Chat Importer. Available at https://github.com/TelegramTools/TLImporter", false).Wait();
                    if (UploadTXT)
                    {
                        Messaging.UploadFile().Wait();
                    }
                    if (!SoloImporting)
                    {
                        Messaging.MarkMessagesAsRead().Wait();
                    }
                    Console.WriteLine("\n\n\nSUCCESS!! All the messages were imported succesfully!");
                    AskConfirmation("\n\nDo you want to import another file?. Otherwise, data will be cleared. [y/n]: ", false);
                    if (ConfirmationConfirmed)
                    {
                        ChooseUsers();
                        ConfirmationConfirmed = false;
                    }
                    else
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
                    ConfirmationConfirmed = false;
                }
            }
            Console.WriteLine("\nAll the data has been cleared and your session revoked. Now, you can log out the session on your mobile device or Telegram Desktop if you want.");
            Console.BackgroundColor = ConsoleColor.Cyan;
            Console.WriteLine("\n\nThank you for using this app. If you like it, please, star the GitHub repository :D at https://github.com/TelegramTools/TLImporter \n\nPress ENTER to exit.");
            Console.ReadLine();
            Environment.Exit(0);
        }
        public static void CheckUsers()
        {
            if (SoloImporting)
            {
                Console.Write("\nWho is one of the partners?: ");
            }
            else
            {
                Console.Write("\nWho are you? (" + Auth.phone1 + "): ");
            }
            NameUser1 = Console.ReadLine();
            while (String.IsNullOrEmpty(NameUser1))
            {
                Console.WriteLine(incorrectName);
                NameUser1 = Console.ReadLine();
            }
            if (SoloImporting)
            {
                Console.Write("\nWho is the other partner?: ");
            }
            else
            {
                Console.Write("\nWho is your partner? (" + Auth.phone2 + "): ");
            }
            NameUser2 = Console.ReadLine();
            while (String.IsNullOrEmpty(NameUser2))
            {
                Console.WriteLine(incorrectName);
                NameUser2 = Console.ReadLine();
            }
            if (SoloImporting)
            {
                Console.WriteLine("One of the partners is " + NameUser1 + " and the other one is " + NameUser2 + ". Checking if the file is valid to be imported...");
            }
            else
            {
                Console.WriteLine("You are " + NameUser1 + " and your partner is " + NameUser2 + ". Checking if the file is valid to be imported...");
            }
            TextHandler.FindUsers();
        }
        public static void AskConfirmation(string Key, bool repeat, bool NotYesOrNo = false , string OptionToInput = null)
        {
            while (!ConfirmationConfirmed)
            {
                Console.Write("\n" + Key);
                if (NotYesOrNo)
                {
                    Console.ResetColor();
                    string TextInputted = Console.ReadLine();
                    if (TextInputted == OptionToInput)
                    {
                        ConfirmationConfirmed = true;
                    }
                    else
                    {
                        ConfirmationConfirmed = false;
                    }
                }
                else
                {
                    string option = Console.ReadLine();
                    if (option == "y" || option == "Y")
                    {
                        ConfirmationConfirmed = true;
                    }
                    if (option == "n" || option == "N")
                    {
                        ConfirmationConfirmed = false;
                        if (!repeat)
                        {
                            break;
                        }
                        else
                        {
                            Console.WriteLine("You cancelled this. You will be asked again by pressing ENTER. Close the app if you don't want to be asked again.");
                            Console.ReadLine();
                        }
                    }
                }                
            }
            return;
        }
        public static void ChooseUsers()
        {
            while (!NotChosenUser)
            {
                if (SoloImporting)
                {
                    Console.Write("\nOK. Do you want to login a new user (N), to use a 1:1 format? Or keep importing with your own account(O)? [N/O]: ");
                    string optionSolo = Console.ReadLine();
                    if (optionSolo == "N" || optionSolo == "n")
                    {
                        SoloImporting = false;
                        Auth.AuthUser2().Wait();
                        NotChosenUser = true;
                    }
                    if (optionSolo == "O" || optionSolo == "o")
                    {
                        NotChosenUser = true;
                    }
                }
                else
                {
                    Console.WriteLine("OK. Which Telegram users do you want to use for the next file? Both logged users (B), only you (1) or only your partner (2)? [B/1/2]: ");
                    string option = Console.ReadLine();
                    if (option == "b" || option == "B")
                    {
                        NotChosenUser = true;
                    }
                    if (option == "1")
                    {
                        Console.WriteLine("Logging out your partner...");
                        if (File.Exists(@"sessionUser2.dat"))
                        {
                            File.Delete(@"sessionUser2.dat");
                        }
                        Console.WriteLine("Now, you will be asked to log in your new partner. Press ENTER to continue");
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
                        Console.WriteLine("Now, you will be asked to log you in a new account. Press ENTER to continue");
                        Console.ReadLine();
                        Auth.AuthUser1().Wait();
                        NotChosenUser = true;
                    }
                }                
            }
            return;
        }
    }
}    