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

        Ppt ppt;

        // Following are Microsoft.Office.Core variables.
        Application pptApp;
        Presentation pptFile;
        Slides pptSlides;

        public PowerPoint(Ppt ppt_arg)
        {
            this.ppt = ppt_arg;
        }

        public Boolean Open() {
            try
            {
                pptApp = new Application();
                pptFile = pptApp.Presentations.Open(this.ppt.get_absolute_path(),
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
            string folder = "";
            string filename = "";

            folder = Path.GetDirectoryName(this.ppt.get_absolute_path().Replace("/", @"\"));
            filename = Path.GetFileName(this.ppt.get_absolute_path().Replace("/", @"\"));

            try
            {
                // Flush older export versions.
                if (Program.flushDirectory && System.IO.Directory.Exists(folder + @"\jpg_"+ppt.id))
                {
                    System.IO.Directory.Delete(folder + @"\jpg_"+ppt.id);
                }

                // Create.
                if (!System.IO.Directory.Exists(folder + @"\jpg_"+ppt.id))
                {
                    System.IO.Directory.CreateDirectory(folder + @"\jpg_" + ppt.id);
                    pptFile.SaveAs(folder + @"\jpg_"+ppt.id, PpSaveAsFileType.ppSaveAsJPG, MsoTriState.msoTrue);
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
                return false;
            }
            return true;
        }

        /* Feature broken in PPT 2013 update.
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
         * */

        /**
         * Added a ridiculous number of garbage collection commants, as malformed PPT files are a pain in the neck to clean-up
         */
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
