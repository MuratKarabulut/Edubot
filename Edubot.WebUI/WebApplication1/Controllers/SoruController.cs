using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using WebApplication1.Models;

namespace WebApplication1.Controllers
{
    public class SoruController : ApiController
    {
        [HttpGet]
        public string faqQuestionAnswer(string soruID)
        {
            string response = "";
            MySession.ConUrl = "Data Source=45.158.14.59;Initial Catalog=dbBS;User ID=ysfugurlu1;Password=Yusuf.1997";
            DataTable dt = new DataTable();
            try
            {
                using (SqlConnection con = new SqlConnection(MySession.ConUrl))
                {
                    using (SqlCommand cmd = new SqlCommand())
                    {
                        con.Open();
                        cmd.Connection = con;
                        cmd.CommandText = "select Cevaplar.Cevap from Sorular inner join Cevaplar on Cevaplar.ID = Sorular.CevapID where Sorular.ID='" + soruID + "'";
                        SqlDataReader rd = cmd.ExecuteReader();
                        if (rd.HasRows)
                        {
                            dt.Load(rd);
                        }

                        con.Close();
                    }
                }
            }
            catch (Exception)
            {
            }
            response = JsonConvert.SerializeObject(dt);
            return response;
        }
    }
}
