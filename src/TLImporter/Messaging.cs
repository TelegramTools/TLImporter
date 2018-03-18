using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using TeleSharp.TL;
using TeleSharp.TL.Messages;
using TLSharp.Core.Network;
using TLSharp.Core.Utils;

namespace TLImporter
{
    class Messaging
    {
        internal static int User1Id;
        internal static int User2Id;
        internal static string floodlimit = "\nFlood limit reached. The program will continue its tasks automatically. Waiting for ";
        internal static string confirmationMessage = "Messaged ";
        internal static string LostConnection = "Can't connect to Telegram. Please, check that your internet connection is still active, and press ENTER to continue.";
        internal static async Task MessageUser1(string MessageToSend1, bool count = true)
        {
            var client2 = Auth.Client2();
            try
            {
                await client2.ConnectAsync();
                await client2.SendMessageAsync(new TLInputPeerUser() { UserId = User1Id }, MessageToSend1);
                if (ImporterApp.printResult)
                {
                    Console.WriteLine(confirmationMessage + ImporterApp.NameUser1 + ": " + MessageToSend1);
                }
                if (count)
                {
                    TextHandler.CurrentMessage = TextHandler.CurrentMessage + 1;
                }
            }
            catch (FloodException ex)
            {
                string time1;
                time1 = ex.TimeToWait.ToString();
                ProgressBar.Draw(TextHandler.CurrentMessage, TextHandler.TotalLineCountInt, true);
                Console.WriteLine(floodlimit + time1);
                Thread.Sleep(ex.TimeToWait);
                MessageUser1(MessageToSend1).Wait();
            }
            catch (Exception ex)
            {
                ProgressBar.Draw(TextHandler.CurrentMessage, TextHandler.TotalLineCountInt, true);
                Console.WriteLine("Unknown error while sending a message to User 1. Here is the full exception code:\n\n" + ex);
                Console.WriteLine("\n\nPress ENTER to try it again. If you receive another error after trying again, please, post the full exception code in a new issue in GitHub, describing the issue as much as possible.");
                Console.ReadLine();
                MessageUser1(MessageToSend1).Wait();
            }
            return;
        }
        internal static async Task MessageUser2(string MessageToSend2, bool Count = true)
        {
            var client1 = Auth.Client1();
            try
            {
                await client1.ConnectAsync();
                if (ImporterApp.SoloImporting)
                {
                    await client1.SendMessageAsync(new TLInputPeerUser() { UserId = User1Id }, MessageToSend2);
                    if (ImporterApp.printResult)
                    {
                        if(ImporterApp.SoloImporting)
                        {
                            Console.WriteLine("Imported message: " + MessageToSend2);
                        }
                        else
                        {
                            Console.WriteLine(confirmationMessage + ImporterApp.NameUser2 + ": " + MessageToSend2);
                        }                        
                    }
                    if (Count)
                    {
                        TextHandler.CurrentMessage = TextHandler.CurrentMessage + 1;
                    }                    
                }
                else
                {
                    await client1.SendMessageAsync(new TLInputPeerUser() { UserId = User2Id }, MessageToSend2);
                    TextHandler.CurrentMessage = TextHandler.CurrentMessage + 1;
                    if (ImporterApp.printResult)
                    {
                        Console.WriteLine(confirmationMessage + ImporterApp.NameUser2 + ": " + MessageToSend2);
                    }
                }                
            }
            catch (FloodException ex)
            {
                string time2;
                time2 = ex.TimeToWait.ToString();
                ProgressBar.Draw(TextHandler.CurrentMessage, TextHandler.TotalLineCountInt, true);
                Console.WriteLine(floodlimit + time2);
                Thread.Sleep(ex.TimeToWait);
                MessageUser2(MessageToSend2).Wait();
            }
            catch (Exception ex)
            {
                ProgressBar.Draw(TextHandler.CurrentMessage, TextHandler.TotalLineCountInt, true);
                if (ImporterApp.SoloImporting)
                {
                    Console.WriteLine("Unknown error while importing the message into 'Saved Messages'. Here is the full exception code:\n\n" + ex.ToString());
                }
                else
                {
                    Console.WriteLine("Unknown error while sending a message to user 2. Here is the full exception code:\n\n" + ex.ToString());
                }                
                Console.WriteLine("\n\nPress ENTER to try it again. If you receive another error after trying again, please, post the full exception code in a new issue in GitHub, describing the issue as much as possible.");
                Console.ReadLine();
                MessageUser2(MessageToSend2).Wait();
            }
            return;
        }
        internal static async Task UploadFile()
        {
            var client1 = Auth.Client1();
            try
            {
                Console.WriteLine("\n\nUploading TXT file...");
                await client1.ConnectAsync();
                string processedPath = ImporterApp.filePath;
                string fileName = Path.GetFileName(ImporterApp.filePath);
                if (ImporterApp.SoloImporting)
                {
                    var fileResult = await client1.UploadFile(fileName, new StreamReader(ImporterApp.filePath));
                    await client1.SendUploadedDocument(
                    new TLInputPeerUser() { UserId = User1Id },
                    fileResult,
                    "Imported file by Telegram Chat Importer",
                    "text/plain",
                    new TLVector<TLAbsDocumentAttribute>());
                }
                else
                {
                    var fileResult = await client1.UploadFile(fileName, new StreamReader(ImporterApp.filePath));
                    await client1.SendUploadedDocument(
                    new TLInputPeerUser() { UserId = User2Id },
                    fileResult,
                    "Imported file by Telegram Chat Importer",
                    "text/plain",
                    new TLVector<TLAbsDocumentAttribute>());
                }                
                Console.WriteLine("\nFile uploaded succesfully!!");
            }
            catch (FloodException ex)
            {
                string time;
                time = ex.TimeToWait.ToString();
                Console.WriteLine(floodlimit + time);
                Thread.Sleep(ex.TimeToWait);
                UploadFile().Wait();
            }
            catch (Exception ex)
            {
                Console.WriteLine("Unknown error while attaching the file. Here is the full exception code:\n\n" + ex);
                Console.WriteLine("\n\nPress ENTER to try it again. If you receive another error after trying again, please, post the full exception code in a new issue in GitHub, describing the issue as much as possible.");
                Console.ReadLine();
                UploadFile().Wait();
            }
            return;
        }
        internal static async Task MarkMessagesAsRead()
        {
            try
            {
                Console.WriteLine("Marking messages as read....");
                var client1 = Auth.Client1();
                var client2 = Auth.Client2();
                await client1.ConnectAsync();
                var target2 = new TLInputPeerUser { UserId = User2Id };
                var readed2 = new TLRequestReadHistory { Peer = target2 };
                await client1.SendRequestAsync<TLAffectedMessages>(readed2);
                Console.WriteLine("Marked messages from " + ImporterApp.NameUser2 + " as read in " + Auth.phone1 + " account.");
                await client2.ConnectAsync();
                var target1 = new TLInputPeerUser { UserId = User1Id };
                var readed1 = new TLRequestReadHistory { Peer = target1 };
                await client2.SendRequestAsync<TLAffectedMessages>(readed1);
                Console.WriteLine("Marked messages from " + ImporterApp.NameUser1 + " as read in " + Auth.phone2 + " account.");
            }
            catch (FloodException ex)
            {
                string time;
                time = ex.TimeToWait.ToString();
                Console.WriteLine(floodlimit + time);
                Thread.Sleep(ex.TimeToWait);
                MarkMessagesAsRead().Wait();
            }
            catch (Exception ex)
            {
                Console.WriteLine("Unknown error while marking messages as read. Here is the full exception code:\n\n" + ex);
                Console.WriteLine("\n\nPress ENTER to try it again. If you receive another error after trying again, please, post the full exception code in a new issue in GitHub, describing the issue as much as possible.");
                Console.ReadLine();
                MarkMessagesAsRead().Wait();
            }
            return;
        }
        }
}
