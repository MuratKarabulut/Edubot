using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WebApplication1.Models
{
    public class Root
    {
        public int Response { get; set; }
        public string Cevap { get; set; }
        public string Soru { get; set; }
        public string SoruID { get; set; }
        public bool isBot { get; set; }
    }
}