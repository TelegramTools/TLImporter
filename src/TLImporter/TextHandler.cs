using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace TLImporter
{
    class TextHandler
    {
        internal static string TotalCount;
        internal static string CountedLines1;
        internal static string CountedLines2;
        internal static int TotalLineCountInt = 0;
        internal static int CurrentMessage = 0;
        internal static void TotalLines()
        {
            FileStream file = new FileStream(ImporterApp.filePath, FileMode.Open, FileAccess.Read, FileShare.None);
            using (StreamReader r = new StreamReader(file))
            {
                while (r.ReadLine() != null) { TotalLineCountInt++; }
                TotalCount = TotalLineCountInt.ToString();
                return;
            }
        }
        internal static void UserLines(String UserToCount, bool user2)
        {
            string[] lines = File.ReadAllLines(ImporterApp.filePath);
            int count = lines.Count(input => input.Contains(UserToCount));
            if (user2)
            {
                CountedLines2 = count.ToString();
            }
            else
            {
                CountedLines1 = count.ToString();
            }           
            return;
        }
        
        public static void ParseStrings()
        {
            FileStream file = new FileStream(ImporterApp.filePath, FileMode.Open, FileAccess.Read, FileShare.None);
            using (var reader = new StreamReader(file))
            {
                string line;
                while ((line = reader.ReadLine()) != null)
                {
                    if (line.Contains(ImporterApp.NameUser1))
                    {
                        if (ImporterApp.SoloImporting)
                        {                            
                            Messaging.MessageUser2(line).Wait();
                            ProgressBar.Draw(CurrentMessage, TotalLineCountInt);
                        }
                        else
                        {
                            string message = line.Replace(ImporterApp.NameUser1 + ": ", "\n");
                            Messaging.MessageUser2(message).Wait();
                        }
                    }
                    else if (line.Contains(ImporterApp.NameUser2))
                    {
                        if (ImporterApp.SoloImporting)
                        {                            
                            Messaging.MessageUser2(line).Wait();
                            ProgressBar.Draw(CurrentMessage, TotalLineCountInt);
                        }
                        else
                        {
                            string message = line.Replace(ImporterApp.NameUser2 + ": ", "\n");
                            Messaging.MessageUser1(message).Wait();
                        }
                    }
                }
            }
            return;
        }
        public static void FindUsers()
        {
            FileStream file = new FileStream(ImporterApp.filePath, FileMode.Open, FileAccess.Read, FileShare.None);
            using (var reader = new StreamReader(file))
            {
                string line;
                while ((line = reader.ReadLine()) != null)
                {
                    if (line.Contains(ImporterApp.NameUser1) || line.Contains(ImporterApp.NameUser2))
                    {
                        ImporterApp.FileIsValid = true;
                    }
                    else
                    {
                        ImporterApp.FileIsValid = false;
                    }
                }
            }
            return;
        }
    }
}