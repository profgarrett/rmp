using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Drawing;


namespace PowerPointUnpacker
{
    class Ppt
    {
        public int id = 0;
        public string file = "";
        public string exported_to_jpg = "";
        public string exported_to_html = "";

        public string get_absolute_path()
        {
           return Config.pptfiles + "userfiles/" + this.file;
        }

        public Stack<PptJpg> getJpgsFromFileSystem()
        {
            Stack<PptJpg> st = new Stack<PptJpg>();
            string path = Path.GetDirectoryName(this.get_absolute_path()) + "/jpg_" + this.id;

            // See if the jpgs exist before continuing;
            if(Directory.Exists(path)) {
                string[] jpgs = Directory.GetFiles(path);
                foreach (string filePathAndName in jpgs)
                    st.Push(new PptJpg(filePathAndName));

            }
            return st;
        }

    }

    class PptJpg
    {
        public string filename = "";
        public long size = 0;
        public int width = 0;
        public int height = 0;

        public PptJpg(string filePathAndName)
        {
            FileInfo file;
            Bitmap img;


            this.filename = Path.GetFileName(filePathAndName);

            file = new System.IO.FileInfo(filePathAndName);
            this.size = file.Length;
            
            img = new Bitmap(filePathAndName);
            this.width = img.Width;
            this.height = img.Height;
        }
    }
}
