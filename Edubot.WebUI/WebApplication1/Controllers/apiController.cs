using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Web.Http;
using System.Web.Script.Serialization;
using WebApplication1.Models;

namespace WebApplication1.Controllers
{
    public class apiController : ApiController
    {

        // POST api/values
        [HttpPost]
        public string faq(Soru soru)
        {
            MySession.soru = soru.soru;
            HttpWebRequest request = (HttpWebRequest)
WebRequest.Create("http://localhost:5001/api/faq"); request.KeepAlive = false;
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
            root.isBot = true;
            MySession.FoundQuestion = 0;
            return JsonConvert.SerializeObject(root);

        }

        // POST api/values
        [HttpGet]
        public string faqMultiple()
        {
            string resp = "";
            try
            {
                if (MySession.FoundQuestion > 0)
                {
                    HttpWebRequest request = (HttpWebRequest)
  WebRequest.Create("http://localhost:5001/api/faqCosunusArray"); request.KeepAlive = false;
                    request.ProtocolVersion = HttpVersion.Version10;
                    request.Method = "POST";


                    // turn our request string into a byte stream
                    requestQuestion r = new requestQuestion
                    {
                        Soru = MySession.soru
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
                    List<Tablo10> myDeserializedClass = JsonConvert.DeserializeObject<List<Tablo10>>(result);
                    string json1 = JsonConvert.SerializeObject(myDeserializedClass);
                    return json1;                

                }
                else
                {
                    MySession.FoundQuestion++;
                    HttpWebRequest request = (HttpWebRequest)
    WebRequest.Create("http://localhost:5001/api/faqSelect"); request.KeepAlive = false;
                    request.ProtocolVersion = HttpVersion.Version10;
                    request.Method = "POST";


                    // turn our request string into a byte stream
                    requestQuestion r = new requestQuestion
                    {
                        Soru = MySession.soru
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

                    RootMultiple root = JsonConvert.DeserializeObject<RootMultiple>(result, new JsonSerializerSettings()
                    { Culture = new System.Globalization.CultureInfo("tr-TR") });
                    return JsonConvert.SerializeObject(root);

                }
            }
            catch (Exception ex)
            {
            }
            return resp;

        }


        // POST api/values
        [HttpGet]
        [ActionName("faqFullMultiple")]
        public string faqFullMultiple()
        {
            string resp = "";
            try
            {
                if (MySession.FoundQuestion > 0)
                {
                    HttpWebRequest request = (HttpWebRequest)
  WebRequest.Create("http://localhost:5001/api/faqCosunusArray"); request.KeepAlive = false;
                    request.ProtocolVersion = HttpVersion.Version10;
                    request.Method = "POST";


                    // turn our request string into a byte stream
                    requestQuestion r = new requestQuestion
                    {
                        Soru = MySession.soru
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
                    List<Tablo10> myDeserializedClass = JsonConvert.DeserializeObject<List<Tablo10>>(result);
                    string json1 = JsonConvert.SerializeObject(myDeserializedClass);
                    return json1;

                }
                else
                {
                    MySession.FoundQuestion++;
                    HttpWebRequest request = (HttpWebRequest)
    WebRequest.Create("http://localhost:5001/api/faqFullSelect"); request.KeepAlive = false;
                    request.ProtocolVersion = HttpVersion.Version10;
                    request.Method = "POST";


                    // turn our request string into a byte stream
                    requestQuestion r = new requestQuestion
                    {
                        Soru = MySession.soru
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

                    RootMultiple root = JsonConvert.DeserializeObject<RootMultiple>(result, new JsonSerializerSettings()
                    { Culture = new System.Globalization.CultureInfo("tr-TR") });
                    return JsonConvert.SerializeObject(root);

                }
            }
            catch (Exception ex)
            {
            }
            return resp;

        }


    }
}
