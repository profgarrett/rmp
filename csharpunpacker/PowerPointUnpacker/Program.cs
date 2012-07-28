using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.Office.Interop.PowerPoint;
using Microsoft.Office.Core;
using System.IO;
using System.Runtime.InteropServices;
using System.Collections;
using System.Security.Cryptography;

//using Microsoft.Office.Interop.
/*
 * See http://social.msdn.microsoft.com/Forums/en-US/oxmlsdk/thread/66ae9df8-c16c-486a-a9bc-6542134f89a9
 * http://stackoverflow.com/questions/1134965/power-point-printing-problem-using-c
 * http://support.microsoft.com/kb/303718
 * http://stackoverflow.com/questions/981547/c-automate-powerpoint-excel
 */

namespace PowerPointUnpacker
{
    class Program
    {
        // Over-ride all exported files by flushing directories.
        public static bool flushDirectory = false;

        static void Main(string[] args)
        {
            while (true)
            {
                Console.WriteLine("Searching at " + DateTime.Now.ToString());
                Go();
                System.Threading.Thread.Sleep(1000*5);
            }
        }

        static void Go() {
            DjangoDb db = new DjangoDb();
            Config config = new Config("../../../../rmp/local_settings.py"); // pathway to config file.
            db.Connect(config);

            Stack<Ppt> pptFiles = db.GetUnprocessedFiles();
            foreach(Ppt pptFile in pptFiles) {

                PowerPoint p = new PowerPoint(config.pptfiles + "userfiles/" + pptFile.file);
                Console.WriteLine("Processing " + pptFile.file);

                // Open file.
                if (!p.Open())
                {
                    pptFile.exported_to_html = "E";
                    pptFile.exported_to_jpg = "E";
                    db.Update(pptFile);
                    continue;
                }

                // Process Jpg
                pptFile.exported_to_jpg = "1";
                db.Update(pptFile);
                pptFile.exported_to_jpg = p.ExportToJpg() ? "2" : "E";
                db.Update(pptFile);

                // Process Html
                pptFile.exported_to_html = "1";
                db.Update(pptFile);
                pptFile.exported_to_html = p.ExportToHtml() ? "2" : "E";
                db.Update(pptFile);
                
                p.Close();
            }

            db.Close();

        }
    }
}
