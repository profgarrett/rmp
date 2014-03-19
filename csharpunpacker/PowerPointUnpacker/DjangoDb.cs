using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Data;
using Npgsql;

/*
 * Below is the code for using MySQL as the Django Backend.
using MySql.Data;
using MySql.Data.MySqlClient;
*/



namespace PowerPointUnpacker
{
    class DjangoDb
    {
        //MySqlConnection myCon;
        NpgsqlConnection myCon; 

        /**
         * Load connection string properties through using local_settings.py file
         * in the django folder.
         * Assume that we have directory structure of
         * rmp/
         * rmp/\csharpunpacker/PowerPointUnpacker/bin/debug
         * rmp/rmp/local_settings.py
         */
        public void Connect() {
            string conString = "Server=" + Config.server +
                ";Port=" + Config.port +
                ";User Id=" + Config.user +
                ";Database=" + Config.database +
                ";Password=" + Config.password + ";";
            
            
            // myCon = new MySqlConnection(conString);
            myCon = new NpgsqlConnection(conString); //"Server=127.0.0.1;Port=5432;User Id=rmp2_login;Password=blah2014!!!;Database=rmp2;");
            myCon.Open();
        }

        /**
         * Return a stack containing all unprocessed files
         */
        public Stack<Ppt> GetUnprocessedFiles()
        {
            Stack<Ppt> st = new Stack<Ppt>();
            string sql = "SELECT id, pptfile, jpg_export_status, jpg_export_version " +
                "FROM ppt_ppt " +
                "WHERE jpg_export_status = '0'";

            // MySqlCommand cmd = new MySqlCommand(sql, myCon);
            // MySqlDataReader rdr = cmd.ExecuteReader();
            
            NpgsqlCommand cmd = new NpgsqlCommand(sql, myCon);
            NpgsqlDataReader rdr = cmd.ExecuteReader();

            while (rdr.Read()) {
                Ppt pptFile = new Ppt();
                pptFile.id = Int32.Parse(rdr[0].ToString());
                pptFile.file = rdr[1].ToString();
                pptFile.exported_to_jpg = rdr[2].ToString();
                st.Push(pptFile);
            }
            rdr.Close();
            return st;
        }

        /**
         * Update the contents of the file in the database
         */
        public void Update(Ppt pptFile)
        {
            // Update export status.
            string sql = "UPDATE ppt_ppt " +
                    " SET jpg_export_status = '" + pptFile.exported_to_jpg + "' " +
                    " WHERE id = " + pptFile.id;
            System.IO.FileInfo file;
            System.Drawing.Bitmap img;

            //MySqlCommand cmd = new MySqlCommand(sql, myCon);
            NpgsqlCommand cmd = new NpgsqlCommand(sql, myCon);
            cmd.ExecuteNonQuery();

            // Remove all old jpg images.
            sql = "DELETE ppt_pptjpg WHERE ppt_id = " + pptFile.id;
            cmd = new NpgsqlCommand(sql, myCon);
            cmd.ExecuteNonQuery();

            for(int i = 1; i<=slide_count; i++){
                file = new System.IO.FileInfo(pptFile.get_absolute_path());

                file_size = System.IO.File.Open(config., System.IO.
                sql = "INSERT INTO ppt_pptjpg (filename, size, height, width, ppt_id) VALUES ('Slide"+i.ToString()+".jpg', "+
                    "
                        
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

}
