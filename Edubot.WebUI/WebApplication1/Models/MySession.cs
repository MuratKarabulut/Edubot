using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WebApplication1.Models
{
    public static class MySession
    {
        public static string soru { get; set; }
        public static string ConUrl { get; set; }
        public static int FoundQuestion { get; set; }
    }
}