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

namespace PowerPointUnpacker
{
    class PowerPoint
    {
        private string folder = "";
        private string filename = "";

        Application pptApp;
        Presentation pptFile;
        Slides pptSlides;

        public PowerPoint(string path)
        {
            path = path.Replace("/", @"\");
            folder = Path.GetDirectoryName(path);
            filename = Path.GetFileName(path);
        }

        public Boolean Open() {
            try
            {

                pptApp = new Application();
                pptFile = pptApp.Presentations.Open(folder + @"\" + filename,
                     Microsoft.Office.Core.MsoTriState.msoFalse,
                     Microsoft.Office.Core.MsoTriState.msoTrue,
                     Microsoft.Office.Core.MsoTriState.msoTrue);

                pptSlides = pptFile.Slides;
            }
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
                return false;
            }
            return true;   
        }

        public Boolean ExportToJpg()
        {
            try
            {
                // Flush?
                if (Program.flushDirectory && System.IO.Directory.Exists(folder + @"\jpg"))
                {
                    System.IO.Directory.Delete(folder + @"\jpg");
                }

                // Create.
                if (!System.IO.Directory.Exists(folder + @"\jpg"))
                {
                    System.IO.Directory.CreateDirectory(folder + @"\jpg");
                    pptFile.SaveAs(folder + @"\jpg", PpSaveAsFileType.ppSaveAsJPG, MsoTriState.msoTrue);
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
                return false;
            }
            return true;
        }

        public Boolean ExportToHtml()
        {
            try
            {
                // Flush?
                if (Program.flushDirectory && System.IO.Directory.Exists(folder + @"\html_files"))
                {
                    System.IO.Directory.Delete(folder + @"\html_files");
                }

                // Create
                if (!System.IO.Directory.Exists(folder + @"\html_files"))
                {
                    pptFile.SaveAs(folder + @"\html", PpSaveAsFileType.ppSaveAsHTML, MsoTriState.msoTrue);
                }

            }
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
                return false;
            }
            return true;
        }

        public void Close(){
            // See http://stackoverflow.com/questions/981547/c-automate-powerpoint-excel
            // and http://stackoverflow.com/questions/158706/how-to-properly-clean-up-excel-interop-objects-in-c/159419#159419

            GC.Collect();
            GC.WaitForPendingFinalizers();
            GC.Collect();
            GC.WaitForPendingFinalizers();


            Marshal.ReleaseComObject(pptSlides);
            pptFile.Close();
            Marshal.ReleaseComObject(pptFile);

            GC.Collect();
            GC.WaitForPendingFinalizers();
            GC.Collect();
            GC.WaitForPendingFinalizers();

            pptApp.Quit();
            Marshal.ReleaseComObject(pptApp);
        }

    }
}
