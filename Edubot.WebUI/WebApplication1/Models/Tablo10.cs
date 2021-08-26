using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WebApplication1.Models
{
    public class Tablo10
    {
        public double ID { get; set; }
        public string Soru { get; set; }
        public double CevapID { get; set; }
        public string Cevap { get; set; }
        public double similarity_bow { get; set; }
    }
}