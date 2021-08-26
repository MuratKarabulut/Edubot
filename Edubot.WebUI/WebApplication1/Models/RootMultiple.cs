using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WebApplication1.Models
{
    public class RootMultiple
    {
        public int Response { get; set; }
        public string CevapRnnID { get; set; }
        public string CevapRnnSoru { get; set; }
        public string CevapBernouilliID { get; set; }
        public string CevapBernouilliSoru { get; set; }
        public string CevapLstmID { get; set; }
        public string CevapLstmSoru { get; set; }
        public string CevapANNID { get; set; }
        public string CevapANNSoru { get; set; }
    }
}