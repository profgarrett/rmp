using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace PowerPointUnpacker
{
    public static class Config
    {
        public static String server;
        public static String user;
        public static String database;
        public static String port;
        public static String password;
        public static String pptfiles;

        public static void load(String path)
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
            Config.server = stripDefault(configFile.ReadLine());
            Config.user = stripDefault(configFile.ReadLine());
            Config.database = stripDefault(configFile.ReadLine());
            Config.port = stripDefault(configFile.ReadLine());
            Config.password = stripDefault(configFile.ReadLine());
            Config.pptfiles = stripDefault(configFile.ReadLine());

            configFile.Close();
        }

        /**
         * Assumes input from a py file.
         * VARIABLE = 'value';
         */
        private static string stripDefault(string line)
        {
            return line.Split('\'')[1];
        }
    }
}
