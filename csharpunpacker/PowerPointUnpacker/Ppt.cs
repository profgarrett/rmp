using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

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

        public 
    }
}
