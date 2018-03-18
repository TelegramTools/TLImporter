using System;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using TeleSharp.TL;
using TeleSharp.TL.Auth;
using TLSharp.Core;
using TLSharp.Core.Network;

namespace TLImporter
{
    class Auth
    {
        internal static string phone1;
        internal static string phone2;
        static string logsuccess = " was logged in successfully!";
        static string code = "You have received a verification code in your Telegram app. Please, type it here and press ENTER afterwards: ";
        static string Twosv = "Type your Two-step verification password here. Input is hidden for security reasons: ";
        static string NoConnection = "Couldn't establish a connection to Telegram. Please, check your internet connection and press ENTER to try again.";
        static string phoneError = "\nError. Phone you entered is not in the valid format. Please, try again: ";
        static string CodeError = "Error. The verification code is not in the valid format. Please, try again: ";
        static string invalidCode = "Your verification code is incorrect. Please, try it again.\n\n";
        static string NotSignedUp = "This phone isn't signed up in Telegram. Please, sign up first using another app and press ENTER to continue.";
        internal static TelegramClient Client1()
        {
            var store1 = new FileSessionStore();
            return new TelegramClient(ImporterApp.apiId, ImporterApp.apiHash, store1, "sessionUser1", "- TLImporter 2.5.4", "PC", "en", "Windows");
        }
        internal static TelegramClient Client2()
        {
            var store2 = new FileSessionStore();
            return new TelegramClient(ImporterApp.apiId, ImporterApp.apiHash, store2, "sessionUser2", "- TLImporter 2.5.4", "PC", "en", "Windows");
        }
        internal static async Task AuthUser1()
        {
            string code1;
            string password1;
            var client1 = Client1();
            Console.Write("\nPlease, type your phone number with the prefixed code. Example: +34666777888. Press ENTER afterwards: ");
            phone1 = Console.ReadLine();
            bool includesPhone = Regex.IsMatch(phone1, @"^\+\d[0-9]{0,14}");
            while (String.IsNullOrWhiteSpace(phone1) | !includesPhone)
            {
                Console.Write(phoneError);
                phone1 = Console.ReadLine();
                includesPhone = Regex.IsMatch(phone1, @"^\+\d[0-9]{0,14}");
            }
            Console.WriteLine("Your phone is:" + phone1 + "\n\nSending verification code...");
            bool isConnected = await client1.ConnectAsync();
            while (!isConnected)
            {
                Console.WriteLine(NoConnection);
                Console.ReadLine();
                isConnected = await client1.ConnectAsync();
            }
            try
            {
                bool registered1 = await client1.IsPhoneRegisteredAsync(phone1);
                while (!registered1)
                {
                    Console.WriteLine(NotSignedUp);
                    Console.ReadLine();
                    try
                    {
                        registered1 = await client1.IsPhoneRegisteredAsync(phone1);
                    }
                    catch (FloodException ex)
                    {
                        string time1;
                        time1 = ex.TimeToWait.ToString();
                        Console.WriteLine(Messaging.floodlimit + time1 + " seconds");
                        Thread.Sleep(ex.TimeToWait);
                        registered1 = await client1.IsPhoneRegisteredAsync(phone1);
                    }
                }
                var hash1 = await client1.SendCodeRequestAsync(phone1);
                while (!client1.IsUserAuthorized())
                {
                    Console.Write(code);
                    code1 = Console.ReadLine();
                    bool includesNumber = Regex.IsMatch(code1, @"^\d[0-9]{0,4}");
                    while (String.IsNullOrWhiteSpace(code1) | !includesNumber)
                    {
                        Console.WriteLine(CodeError);
                        code1 = Console.ReadLine();
                        includesNumber = Regex.IsMatch(code1, @"^\d[0-9]{0,4}");
                    }
                    try
                    {
                        var user1 = await client1.MakeAuthAsync(phone1, hash1, code1);
                        Messaging.User1Id = user1.Id;
                    }
                    catch (CloudPasswordNeededException)
                    {
                        var password = await client1.GetPasswordSetting();
                        // Code for hiding input
                        Console.Write(Twosv);
                        password1 = null;
                        while (true)
                        {
                            var key = Console.ReadKey(true);
                            if (key.Key == ConsoleKey.Enter)
                                break;
                            password1 += key.KeyChar;
                        }
                        // End of it                
                        var password_str = password1;
                        var user1 = await client1.MakeAuthWithPasswordAsync(password, password_str);
                        Messaging.User1Id = user1.Id;
                    }
                    catch (InvalidPhoneCodeException)
                    {
                        Console.WriteLine(invalidCode);
                    }
                }
                Console.WriteLine("\n\n" + phone1 + logsuccess);
            }
            catch (FloodException ex)
            {
                string time1;
                time1 = ex.TimeToWait.ToString();
                Console.WriteLine(Messaging.floodlimit + time1);
                Thread.Sleep(ex.TimeToWait);
            }
            catch (Exception ex)
            {
                if (ex.ToString().Contains("PHONE_NUMBER_INVALID"))
                {
                    Console.Write("\nYour phone number is incorrect. Press ENTER to try the authentication again.");
                    Console.Read();
                }
                else
                {
                    Console.WriteLine("Something unknown went wrong. Here is more info:\n\n" + ex);
                    Console.WriteLine("\n\nYou can continue without any problem and try the authentication again. Press ENTER.");
                    Console.ReadLine();
                }                
                Auth.AuthUser1().Wait();
                return;
            }
            return;
        }
        internal static async Task AuthUser2()
        {
            Console.WriteLine("Logging in your partner...");
            string code2;
            string password2;
            var client2 = Client2();            
            Console.Write("\n\nPlease, type your partner's phone number with the prefixed code. Example: +34666777888. Press ENTER afterwards: ");
            phone2 = Console.ReadLine();
            bool includesPhone = Regex.IsMatch(phone1, @"^\+\d[0-9]{0,14}");
            while (String.IsNullOrWhiteSpace(phone2) | !includesPhone)
            {
                Console.Write(phoneError);
                phone2 = Console.ReadLine();
                includesPhone = Regex.IsMatch(phone1, @"^\+\d[0-9]{0,14}");
            }
            Console.WriteLine("Your phone is:" + phone2 + "\n\nSending verification code...");
            bool isConnected = await client2.ConnectAsync();
            while (!isConnected)
            {
                Console.WriteLine(NoConnection);
                Console.ReadLine();
                isConnected = await client2.ConnectAsync();
            }
            try
            {
                bool registered2 = await client2.IsPhoneRegisteredAsync(phone2);
                while (!registered2)
                {
                    Console.WriteLine(NotSignedUp);
                    Console.ReadLine();
                    try
                    {
                        registered2 = await client2.IsPhoneRegisteredAsync(phone2);
                    }
                    catch (FloodException ex)
                    {
                        string time2;
                        time2 = ex.TimeToWait.ToString();
                        Console.WriteLine(Messaging.floodlimit + time2 + " seconds");
                        Thread.Sleep(ex.TimeToWait);
                        registered2 = await client2.IsPhoneRegisteredAsync(phone2);
                    }
                }
                var hash2 = await client2.SendCodeRequestAsync(phone2);
                while (!client2.IsUserAuthorized())
                {
                    Console.Write(code);
                    code2 = Console.ReadLine();
                    bool includesNumber = Regex.IsMatch(code2, @"^\d[0-9]{0,4}");
                    while (String.IsNullOrWhiteSpace(code2) | !includesNumber)
                    {
                        Console.WriteLine(CodeError);
                        code2 = Console.ReadLine();
                        includesNumber = Regex.IsMatch(code2, @"^\d[0-9]{0,4}");
                    }
                    try
                    {
                        var user2 = await client2.MakeAuthAsync(phone2, hash2, code2);
                        Messaging.User2Id = user2.Id;
                    }
                    catch (CloudPasswordNeededException)
                    {
                        var password = await client2.GetPasswordSetting();
                        // Code for hiding input
                        Console.Write(Twosv);
                        password2 = null;
                        while (true)
                        {
                            var key = Console.ReadKey(true);
                            if (key.Key == ConsoleKey.Enter)
                                break;
                            password2 += key.KeyChar;
                        }
                        // End of it                
                        var password_str = password2;
                        var user2 = await client2.MakeAuthWithPasswordAsync(password, password_str);
                        Messaging.User2Id = user2.Id;
                    }
                    catch (InvalidPhoneCodeException)
                    {
                        Console.WriteLine(invalidCode);
                    }
                }
                Console.WriteLine("\n\n" + phone2 + logsuccess);
            }
            catch (FloodException ex)
            {
                string time2;
                time2 = ex.TimeToWait.ToString();
                Console.WriteLine(Messaging.floodlimit + time2);
                Thread.Sleep(ex.TimeToWait);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Something unknown went wrong. Here is more info:\n\n" + ex);
                Console.WriteLine("\n\nYou can continue without any problem and try the authentication again. Press ENTER.");
                Console.ReadLine();
                Auth.AuthUser2().Wait();
                return;
            }
            return;
        }
    }
}