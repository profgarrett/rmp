using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace PowerPointUnpacker
{
    class Config
    {
        public String server;
        public String user;
        public String database;
        public String port;
        public String password;
        public String pptfiles;

        public Config(String path)
        {
            if (!System.IO.File.Exists(path))
            {
                throw new Exception("Invalid directory.  Could not find local_settings.py");
            }

            System.IO.StreamReader configFile = new System.IO.StreamReader(path);

            // Skip first lines and start on line 7
            for (int i = 0; i < 6; i++)
            {
                configFile.ReadLine();
            }
            this.server = stripDefault(configFile.ReadLine());
            this.user = stripDefault(configFile.ReadLine());
            this.database = stripDefault(configFile.ReadLine());
            this.port = stripDefault(configFile.ReadLine());
            this.password = stripDefault(configFile.ReadLine());
            this.pptfiles = stripDefault(configFile.ReadLine());

            configFile.Close();
        }

        /**
 * Assumes input from a py file.
 * VARIABLE = 'value';
 */
        private string stripDefault(string line)
        {
            return line.Split('\'')[1];
        }
    }
}
