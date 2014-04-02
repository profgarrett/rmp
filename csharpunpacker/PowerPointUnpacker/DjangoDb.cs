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

            //MySqlCommand cmd = new MySqlCommand(sql, myCon);
            NpgsqlCommand cmd = new NpgsqlCommand(sql, myCon);
            cmd.ExecuteNonQuery();

            // Now update jpg files.
            this.UpdatePptJpgs(pptFile);
        }

        private void UpdatePptJpgs(Ppt pptFile) {
            // Remove all old jpg images.
            string sql = "DELETE FROM ppt_pptjpg WHERE ppt_id = " + pptFile.id;
            NpgsqlCommand cmd = new NpgsqlCommand(sql, myCon);
            cmd.ExecuteNonQuery();

            // Add each into the db again.
            Stack<PptJpg> st = pptFile.getJpgsFromFileSystem();
            foreach(PptJpg pptJpg in st) {
                sql = "INSERT INTO ppt_pptjpg (filename, size, height, width, ppt_id) VALUES ('" +
                    pptJpg.filename + "', " + pptJpg.size.ToString() + ", " + pptJpg.height.ToString() + ", " +
                    pptJpg.width.ToString() + ", " + pptFile.id.ToString() + ")";
                cmd = new NpgsqlCommand(sql, myCon);
                cmd.ExecuteNonQuery();
            }
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
