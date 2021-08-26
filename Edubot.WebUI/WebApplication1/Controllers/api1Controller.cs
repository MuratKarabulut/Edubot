using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Web.Http;
using WebApplication1.Models;

namespace WebApplication1.Controllers
{
    public class api1Controller : ApiController
    {
        [HttpPost]
        public string faq1(Soru soru)
        {
            HttpWebRequest request = (HttpWebRequest)
WebRequest.Create("http://localhost:5001/api/faq1"); request.KeepAlive = false;
            request.ProtocolVersion = HttpVersion.Version10;
            request.Method = "POST";


            // turn our request string into a byte stream
            requestQuestion r = new requestQuestion
            {
                Soru = soru.soru
            };
            string json = JsonConvert.SerializeObject(r);

            byte[] postBytes = Encoding.UTF8.GetBytes(json);

            // this is important - make sure you specify type this way
            request.ContentType = "application/json; charset=UTF-8";
            request.Accept = "application/json";
            request.ContentLength = postBytes.Length;
            Stream requestStream = request.GetRequestStream();

            // now send it
            requestStream.Write(postBytes, 0, postBytes.Length);
            requestStream.Close();

            // grab te response and print it out to the console along with the status code
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();
            string result;
            using (StreamReader rdr = new StreamReader(response.GetResponseStream()))
            {
                result = rdr.ReadToEnd();
            }

            Root root = JsonConvert.DeserializeObject<Root>(result, new JsonSerializerSettings()
            { Culture = new System.Globalization.CultureInfo("tr-TR") });

            return result;

        }

        [HttpPost]
        [ActionName("faqFullAnn")]
        public string faqFullAnn(Soru soru)
        {
            HttpWebRequest request = (HttpWebRequest)
WebRequest.Create("http://localhost:5001/api/faqFullAnn"); request.KeepAlive = false;
            request.ProtocolVersion = HttpVersion.Version10;
            request.Method = "POST";


            // turn our request string into a byte stream
            requestQuestion r = new requestQuestion
            {
                Soru = soru.soru
            };
            string json = JsonConvert.SerializeObject(r);

            byte[] postBytes = Encoding.UTF8.GetBytes(json);

            // this is important - make sure you specify type this way
            request.ContentType = "application/json; charset=UTF-8";
            request.Accept = "application/json";
            request.ContentLength = postBytes.Length;
            Stream requestStream = request.GetRequestStream();

            // now send it
            requestStream.Write(postBytes, 0, postBytes.Length);
            requestStream.Close();

            // grab te response and print it out to the console along with the status code
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();
            string result;
            using (StreamReader rdr = new StreamReader(response.GetResponseStream()))
            {
                result = rdr.ReadToEnd();
            }

            Root root = JsonConvert.DeserializeObject<Root>(result, new JsonSerializerSettings()
            { Culture = new System.Globalization.CultureInfo("tr-TR") });

            return result;

        }

    }
}
