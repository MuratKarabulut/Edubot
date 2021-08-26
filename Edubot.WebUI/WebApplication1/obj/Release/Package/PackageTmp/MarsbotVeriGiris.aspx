<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="MarsbotVeriGiris.aspx.cs" Inherits="WebApplication1.MarsbotVeriGiris" %>


<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <link href="Content/bootstrap-grid.min.css" rel="stylesheet" />
    <link href="Content/bootstrap.min.css" rel="stylesheet" />
    <title></title>
</head>
<body>
    <form id="form1" runat="server">
        <div class="container mt-3">

            <div class="row mt-2">
                <div class="col-md-1">
                    Etiket seçin
                </div>
                <div class="col-md-5">
                    <asp:DropDownList ID="drpTag" CssClass="form-control" runat="server"></asp:DropDownList>
                </div>
            </div>

            <div class="row">
                <div class="col-md-1">
                    Soru
                </div>
                <div class="col-md-5">
                    <textarea id="txtSorular" runat="server" rows="3" class="form-control"></textarea>
                </div>
            </div>
            <div class="row mt-2">
                <div class="col-md-1">
                    Cevap
                </div>
                <div class="col-md-5">
                    <textarea id="txtCevap" runat="server" rows="3" class="form-control"></textarea>
                </div>
            </div>

            <div class="row mt-2">
                <div class="col-md-1">
                    Cevaplar
                </div>
                <div class="col-md-5">
                    <select id="drpCevaplar" class="form-control" runat="server">
                    </select>
                </div>
            </div>
            <div class="row mt-2">
                <div class="col-md-1">
                </div>
                <div class="col-md-2">
                    <asp:Button ID="btnSoruEkle" OnClick="btnSoruEkle_Click" CssClass="btn btn-secondary" runat="server" Text="Soru-Cevap ekle" />
                </div>
                <div class="col-md-2">
                    <asp:Button ID="btnSoruCevap" OnClick="btnSoruCevap_Click" CssClass="btn btn-success" runat="server" Text="Soru- Cevap İlişkilendir" />
                </div>
                <div class="col-md-2">
                    <asp:Label ID="lblMesaj" runat="server" Text=""></asp:Label>
                </div>
            </div>

            <div class="row mt-4">
                <div class="col-md-12">
                    <table class="table">
                        <thead>
                            <tr>
                                <td>Soru</td>
                                <td>Cevap</td>
                            </tr>
                        </thead>
                        <tbody id="tbodySorular" runat="server"></tbody>

                    </table>
                </div>
            </div>
        </div>
        <input type="hidden" id="hdTag" runat="server" />
        <script src="Scripts/jquery-3.6.0.min.js"></script>
        <script src="Scripts/bootstrap.min.js"></script>
        <script src="Scripts/popper-utils.min.js"></script>
    </form>
    <script>
        $("#drpTag").change(function () {
            var tag = "";
            tag = $('#drpTag').val();
            $("#hdTag").val(tag);

        });
    </script>
</body>

</html>

