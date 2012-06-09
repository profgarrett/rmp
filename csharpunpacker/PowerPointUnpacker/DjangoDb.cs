using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using MySql.Data;
using MySql.Data.MySqlClient;

namespace PowerPointUnpacker
{
    class DjangoDb
    {
        MySqlConnection myCon;

        /**
         * Load connection string properties through using local_settings.py file
         * in the django folder.
         * Assume that we have directory structure of
         * rmp/
         * rmp/\csharpunpacker/PowerPointUnpacker/bin/debug
         * rmp/rmp/local_settings.py
         */
        public void Connect() {
            string conString = "";
            string path = "../../../../rmp/local_settings.py";

            if (!System.IO.File.Exists(path)){
                throw new Exception("Invalid directory.  Could not find local_settings.py");
            }

            System.IO.StreamReader configFile = new System.IO.StreamReader(path);

            // Skip first lines and start on line 7
            for (int i = 0; i < 6; i++)
            {
                configFile.ReadLine();
            }
            conString = "server=" + stripDefault(configFile.ReadLine());
            conString += ";user=" + stripDefault(configFile.ReadLine());
            conString += ";database=" + stripDefault(configFile.ReadLine());
            conString += ";port=" + stripDefault(configFile.ReadLine());
            conString += ";password=" + stripDefault(configFile.ReadLine()) + ";";
       
            myCon = new MySqlConnection(conString);
            myCon.Open();
        }

        /**
         * Assumes input from a py file.
         * VARIABLE = 'value';
         */
        private string stripDefault(string line)
        {
            return line.Split('\'')[1];
        }

        /**
         * Return a stack containing all unprocessed files
         */
        public Stack<PptUploadedFile> GetUnprocessedFiles()
        {
            Stack<PptUploadedFile> st = new Stack<PptUploadedFile>();
            string sql = "SELECT id, ppt_id, file, exported_to_jpg, exported_to_html " +
                "FROM rmp.rating_pptuploadedfile " +
                "WHERE exported_to_jpg = '0'";

            MySqlCommand cmd = new MySqlCommand(sql, myCon);
            MySqlDataReader rdr = cmd.ExecuteReader();

            while (rdr.Read()) {
                PptUploadedFile pptFile = new PptUploadedFile();
                pptFile.id = Int32.Parse(rdr[0].ToString());
                pptFile.ppt_id = Int32.Parse(rdr[1].ToString());
                pptFile.file = rdr[2].ToString();
                pptFile.exported_to_jpg = rdr[3].ToString();
                pptFile.exported_to_html = rdr[4].ToString();
                st.Push(pptFile);
            }
            rdr.Close();
            return st;
        }

        /**
         * Update the contents of the file in the database
         */
        public void Update(PptUploadedFile pptFile)
        {
            string sql = "UPDATE rmp.rating_pptuploadedfile " +
                    " SET exported_to_jpg = '" + pptFile.exported_to_jpg + "', " +
                    " exported_to_html = '" + pptFile.exported_to_html + "'" +
                    " WHERE id = " + pptFile.id;

            MySqlCommand cmd = new MySqlCommand(sql, myCon);
            cmd.ExecuteNonQuery();        
        }

        public void Close()
        {
            try
            {
                myCon.Close();
            }
            catch (Exception e)
            {
                Console.WriteLine("Error: " + e.ToString());
            }
        }
    }


    class PptUploadedFile
    {
        public int id = 0;
        public int ppt_id = 0;
        public string file = "";
        public string exported_to_jpg = "";
        public string exported_to_html = "";
    }
}
