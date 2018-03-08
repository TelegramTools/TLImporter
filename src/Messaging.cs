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
        internal static string floodlimit = "Flood limit reached. The program will continue its tasks automatically. Waiting for ";
        internal static string confirmationMessage = "Messaged ";
        internal static string LostConnection = "Can't connect to Telegram. Please, check that your internet connection is still active, and press ENTER to continue.";
        internal static async Task MessageUser1(string MessageToSend1, bool printresult)
        {
            var client2 = Auth.Client2();
            try
            {
                await client2.ConnectAsync();
                await client2.SendMessageAsync(new TLInputPeerUser() { UserId = User1Id }, MessageToSend1);
                if (printresult)
                {
                    Console.WriteLine(confirmationMessage + ImporterApp.NameUser1 + ": " + MessageToSend1);
                }                
            }
            catch (FloodException ex)
            {
                string time1;
                time1 = ex.TimeToWait.ToString();
                Console.WriteLine(floodlimit + time1);
                Thread.Sleep(ex.TimeToWait);
                await client2.SendMessageAsync(new TLInputPeerUser() { UserId = User1Id }, MessageToSend1);
                if (printresult)
                {
                    Console.WriteLine(confirmationMessage + ImporterApp.NameUser1 + ": " + MessageToSend1);
                }                
            }
            return;
        }
        internal static async Task MessageUser2(string MessageToSend2, bool printresult)
        {
            var client1 = Auth.Client1();
            try
            {
                await client1.ConnectAsync();
                await client1.SendMessageAsync(new TLInputPeerUser() { UserId = User2Id }, MessageToSend2);
                if (printresult)
                {
                    Console.WriteLine(confirmationMessage + ImporterApp.NameUser2 + ": " + MessageToSend2);
                }                
            }
            catch (FloodException ex)
            {
                string time2;
                time2 = ex.TimeToWait.ToString();
                Console.WriteLine(floodlimit + time2);
                Thread.Sleep(ex.TimeToWait);
                await client1.SendMessageAsync(new TLInputPeerUser() { UserId = User2Id }, MessageToSend2);
                if (printresult)
                {
                    Console.WriteLine(confirmationMessage + ImporterApp.NameUser2 + ": " + MessageToSend2);
                }                
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
                // string fileName = Path.GetFileName(ImporterApp.filePath);
                var fileResult = await client1.UploadFile("Imported_File.txt", new StreamReader(ImporterApp.filePath));
                await client1.SendUploadedDocument(
                new TLInputPeerUser() { UserId = User2Id },
                fileResult,
                "Imported file by Telegram Chat Importer",
                "text/plain",
                new TLVector<TLAbsDocumentAttribute>());
                Console.WriteLine("\nFile uploaded succesfully!!");
            }
            catch (FloodException ex)
            {
                string time;
                time = ex.TimeToWait.ToString();
                Console.WriteLine(floodlimit + time);
                Thread.Sleep(ex.TimeToWait);
                await client1.UploadFile("Imported_Chat.txt", new StreamReader(ImporterApp.filePath));
            }
            return;
        }
        internal static async Task MarkMessagesAsRead()
        {
            Console.WriteLine("Marking messages as read....");
            var client1 = Auth.Client1();
            var client2 = Auth.Client2();
            await client1.ConnectAsync();
            var target2 = new TLInputPeerUser{UserId = User2Id};
            var readed2 = new TLRequestReadHistory {Peer = target2};
            await client1.SendRequestAsync<TLAffectedMessages>(readed2);
            Console.WriteLine("Marked messages from " + ImporterApp.NameUser2 + " as read in " + Auth.phone1 + " account.");            
            await client2.ConnectAsync();
            var target1 = new TLInputPeerUser { UserId = User1Id };
            var readed1 = new TLRequestReadHistory { Peer = target1 };
            await client2.SendRequestAsync<TLAffectedMessages>(readed1);
            Console.WriteLine("Marked messages from " + ImporterApp.NameUser1 + " as read in " + Auth.phone2 + " account.");
            return;
        }
        }
}
