using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace TLImporter
{
    class TextHandler
    {
        internal static string TotalCount;
        internal static string CountedLines1;
        internal static string CountedLines2;
        internal static void TotalLines()
        {
            using (StreamReader r = new StreamReader(ImporterApp.filePath))
            {
                int i = 0;
                while (r.ReadLine() != null) { i++; }
                TotalCount = i.ToString();
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
            using (var reader = new StreamReader(ImporterApp.filePath))
            {
                string line;
                while ((line = reader.ReadLine()) != null)
                {
                    if (line.Contains(ImporterApp.NameUser1))
                    {
                        string message = line.Replace(ImporterApp.NameUser1 + ": ", "\n");
                        Messaging.MessageUser2(message, true).Wait();
                    }
                    else if (line.Contains(ImporterApp.NameUser2))
                    {
                        string message = line.Replace(ImporterApp.NameUser2 + ": ", "\n");
                        Messaging.MessageUser1(message, true).Wait();
                    }
                }
            }
            return;
        }
        public static void FindUsers()
        {
            using (var reader = new StreamReader(ImporterApp.filePath))
            {
                string line;
                while ((line = reader.ReadLine()) != null)
                {
                    if (line.Contains(ImporterApp.NameUser1) | line.Contains(ImporterApp.NameUser2))
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