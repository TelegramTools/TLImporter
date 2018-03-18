using System;

namespace TLImporter
{
    internal sealed class ProgressBar
    {
        internal static void Draw(int progress, int tot, bool red = false)
        {
            try
            {
                int percentage = (int)((double)TextHandler.CurrentMessage / TextHandler.TotalLineCountInt * 100);
                Console.CursorLeft = 0;
                Console.Write("[");
                float onechunk;
                if (ImporterApp.printResult)
                {
                    Console.CursorLeft = 32;
                    onechunk = 30.0f / tot;
                }
                else
                {
                    Console.CursorLeft = 150;
                    onechunk = 148.0f / tot;
                }
                Console.Write("]");
                Console.CursorLeft = 1;

                int position = 1;
                for (int i = 0; i < onechunk * progress; i++)
                {
                    if (red)
                    {
                        Console.BackgroundColor = ConsoleColor.DarkRed;
                    }
                    else
                    {
                        Console.BackgroundColor = ConsoleColor.Green;
                    }
                    Console.CursorLeft = position++;
                    Console.Write(" ");
                }
                if (ImporterApp.printResult)
                {
                    for (int i = position; i <= 31; i++)
                    {
                        Console.BackgroundColor = ConsoleColor.Gray;
                        Console.CursorLeft = position++;
                        Console.Write(" ");
                    }
                }
                else
                {
                    for (int i = position; i <= 149; i++)
                    {
                        Console.BackgroundColor = ConsoleColor.Gray;
                        Console.CursorLeft = position++;
                        Console.Write(" ");
                    }
                }

                if (ImporterApp.printResult)
                {
                    Console.CursorLeft = 35;
                }
                else
                {
                    Console.CursorLeft = 153;
                }
                Console.BackgroundColor = ConsoleColor.Black;
                Console.Write(percentage.ToString() + "% completed: " + progress.ToString() + " of " + tot.ToString() + " messages imported.  ");
            }
            catch (Exception)
            {
                Console.ResetColor();
                Console.WriteLine("You must not resize this Window. Otherwise, the progress bar will not be displayed. Press ENTER to maximize it and continue.");
                Console.Read();
                Console.SetWindowSize(Console.LargestWindowWidth, Console.LargestWindowHeight);
                ImporterApp.ShowWindow(ImporterApp.ThisConsole, ImporterApp.MAXIMIZE);
                bool GivenBool = red;
                Draw(progress, tot, GivenBool);
            }            
        }
    }
}