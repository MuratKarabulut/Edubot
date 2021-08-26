<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="indexFullModel.aspx.cs" Inherits="WebApplication1.indexFullModel" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
    <style>
        body {
            background-color: #fff
        }

        ::-webkit-scrollbar {
            width: 10px
        }

        ::-webkit-scrollbar-track {
            background: #eee
        }

        ::-webkit-scrollbar-thumb {
            background: #888
        }

            ::-webkit-scrollbar-thumb:hover {
                background: #555
            }

        .wrapper {
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #651FFF
        }

        .main {
            background-color: #eee;
            width: 620px;
            position: relative;
            border-radius: 8px;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
            padding: 6px 0px 0px 0px
        }

        .scroll {
            overflow-y: scroll;
            scroll-behavior: smooth;
            height: 325px
        }

        .img1 {
            border-radius: 50%;
            background-color: #66BB6A
        }

        .name {
            font-size: 8px
        }

        .msg {
            background-color: #fff;
            font-size: 11px;
            padding: 5px;
            border-radius: 5px;
            font-weight: 500;
            color: #3e3c3c
        }

        .between {
            font-size: 8px;
            font-weight: 500;
            color: #a09e9e
        }

        .navbar {
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)
        }

        .form-control {
            font-size: 12px;
            font-weight: 400;
            width: 230px;
            height: 30px;
            border: none
        }

        form-control: focus {
            box-shadow: none;
            overflow: hidden;
            border: none
        }

        .form-control:focus {
            box-shadow: none !important
        }

        .icon1 {
            color: #7C4DFF !important;
            font-size: 18px !important;
            cursor: pointer
        }

        .icon2 {
            color: #512DA8 !important;
            font-size: 18px !important;
            position: relative;
            left: 8px;
            padding: 0px;
            cursor: pointer
        }

        .icondiv {
            border-radius: 50%;
            width: 15px;
            height: 15px;
            padding: 2px;
            position: relative;
            bottom: 1px
        }
    </style>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" />
</head>
<body>
    <div class="wrapper">
        <div class="main">
            <div id="chat" class="px-2 scroll">
                <div class="d-flex align-items-center text-right justify-content-end ">
                    <div class="pr-2">
                        <span class="name">Sanal Asistan</span>
                        <p class="msg">Hey Merhaba! Ben Üniversite botuyum. Üniversite ile ilgili genel soruları cevaplayabilirim.</p>
                    </div>
                    <div>
                        <img src="img/robot.png" width="30" class="img1" />
                    </div>
                </div>
            </div>
            <nav class="navbar bg-white navbar-expand-sm d-flex justify-content-between">
                <input type="text" id="txtSoru" class="form-control" placeholder="Bir şey yazın.">
                <div class="icondiv d-flex justify-content-end align-content-center text-center ml-2">
                    <i id="btnSend" class="fa fa-arrow-circle-right icon2"></i>
                </div>
            </nav>
        </div>
    </div>

    <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js'></script>
    <script src='https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js'></script>

    <script>
        $("#txtSoru").keydown(function (e) {
            if (e.keyCode == 13) {
                var txtSoru = $("#txtSoru").val();
                if (txtSoru.length > 0) {
                    Kosunus(txtSoru);
                }
            }
        });
        $("#btnSend").click(function () {
            var txtSoru = $("#txtSoru").val();
            if (txtSoru.length > 0) {
                Kosunus(txtSoru);
            }
        });
        function Kosunus(txtSoru) {
            var soruS = '<div class="d-flex align-items-center">';
            soruS += ' <div class="text-left pr-1"><img src="https://img.icons8.com/color/40/000000/guest-female.png" width="30" class="img1" /></div>';
            soruS += ' <div class="pr-2 pl-1"> <span class="name">ÖĞRENCİ</span>';
            soruS += ' <p class="msg">' + txtSoru + '</p>';
            soruS += "</div></div>";
            var chat1 = $("#chat").html();

            chat1 = chat1 + soruS;
            $("#chat").html(chat1);
            var soru1 = {
                "soru": txtSoru
            };
            $.ajax({
                url: 'api/api/faq',
                async: true,
                dataType: 'json',
                type: 'POST',
                data: JSON.stringify(soru1),
                contentType: 'application/json; charset=utf-8',
                success: function (data) {
                    data = $.parseJSON(data);
                    console.log(data);
                    if (data.Response != null) {
                        if (data.Response == 200) {
                            // $("#txtCosunus").val(data.Cevap);
                            var chat = $("#chat").text();
                            var tmp = " <div class='d-flex align-items-center text-right justify-content-end '>";
                            tmp += "<div class='pr-2'>";
                            tmp += '<span class="name">Sanal Asistan</span>';
                           // tmp += '<p class="msg">'+data.Soru+'</br> '+ data.Cevap;
                            tmp += '<p class="msg">'+ data.Cevap;
                            tmp += '<br /><br /><span class="text-right">';
                            tmp += ' <i class="fa fa-thumbs-o-up fa-2x likes" data-ID=' + data.SoruID + ' aria-hidden="true"></i>';
                            tmp += '<i class="fa fa-thumbs-o-down fa-2x ml-2 dislikes" data-ID=' + data.SoruID + ' aria-hidden="true"></i>';
                            tmp += '</span>';
                            tmp += "</p>";
                            tmp += "</div>";

                            tmp += "<div>";
                            tmp += ' <img src="img/robot.png" width="30" class="img1" />';
                            tmp += "</div>";

                            tmp += "</div>";

                            var chat = $("#chat").html();

                            chat = chat + tmp;
                            $("#chat").html(chat);
                            $("#chat").animate({ scrollTop: $('#chat').prop("scrollHeight") }, 1000);
                            $("#txtSoru").val("");
                            /*
                    <div class="d-flex align-items-center text-right justify-content-end ">
                        <div class="pr-2">
                            <span class="name">Dr. Hendrikson</span>
                            <p class="msg">Twice a day, at breakfast and before bed</p>
                        </div>
                        <div>
                            <img src="https://i.imgur.com/HpF4BFG.jpg" width="30" class="img1" />
                        </div>
                    </div>

                             */
                        }
                        else {
                            alert("hata " + data.Cevap);
                            return "";
                        }
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    alert(xhr.responseText);
                    console.log(thrownError);
                    return "";
                }
            });
        }
        $(document).on("click", ".likes", function () {
            try {
                $(this).attr("class", "fa fa-thumbs-up fa-2x");
                var id = $(this).attr("data-id");
                var chat = $("#chat").text();
                var tmp = " <div class='d-flex align-items-center text-right justify-content-end '>";
                tmp += "<div class='pr-2'>";
                tmp += '<span class="name">Sanal Asistan</span>';
                tmp += '<p class="msg">Sorunuzu doğru bildiğime göre yeni sorulara geçebiliriz :)';
                tmp += "</p>";
                tmp += "</div>";

                tmp += "<div>";
                tmp += ' <img src="img/robot.png" width="30" class="img1" />';
                tmp += "</div>";

                tmp += "</div>";

                var chat = $("#chat").html();

                chat = chat + tmp;
                $("#chat").html(chat);
                $("#chat").animate({ scrollTop: $('#chat').prop("scrollHeight") }, 1000);
            } catch (e) {

            }

        })


        $(document).on("click", ".selectquestion", function () {
            try {
                var id = $(this).attr("data-id");
                var soru1 = {
                    "soruID": id
                };
                $.ajax({
                    url: 'api/Soru/faqQuestionAnswer',
                    async: true,
                    dataType: 'json',
                    type: 'get',
                    // data: JSON.stringify(soru1),
                    data: soru1,
                    contentType: 'application/json; charset=utf-8',
                    success: function (data) {
                        data = $.parseJSON(data);
                        console.log(data);
                        // $("#txtCosunus").val(data.Cevap);
                        if (data.length > 0) {

                            var chat = $("#chat").text();
                            var tmp = " <div class='d-flex align-items-center text-right justify-content-end '>";
                            tmp += "<div class='pr-2'>";
                            tmp += '<span class="name">Sanal Asistan</span>';
                            tmp += '<p class="msg">' + data[0].Cevap;
                            tmp += '<br /><br /><span class="text-right">';
                            tmp += ' <i class="fa fa-thumbs-o-up fa-2x likes" data-ID=' + id + ' aria-hidden="true"></i>';
                            tmp += '<i class="fa fa-thumbs-o-down fa-2x ml-2 dislikes" data-ID=' + id + ' aria-hidden="true"></i>';
                            tmp += '</span>';
                            tmp += "</p>";
                            tmp += "</div>";

                            tmp += "<div>";
                            tmp += ' <img src="img/robot.png" width="30" class="img1" />';
                            tmp += "</div>";

                            tmp += "</div>";

                            var chat = $("#chat").html();

                            chat = chat + tmp;
                            $("#chat").html(chat);
                            $("#chat").animate({ scrollTop: $('#chat').prop("scrollHeight") }, 1000);
                        }
                        /*
                <div class="d-flex align-items-center text-right justify-content-end ">
                    <div class="pr-2">
                        <span class="name">Dr. Hendrikson</span>
                        <p class="msg">Twice a day, at breakfast and before bed</p>
                    </div>
                    <div>
                        <img src="https://i.imgur.com/HpF4BFG.jpg" width="30" class="img1" />
                    </div>
                </div>
 
                         */

                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        alert(xhr.responseText);
                        console.log(thrownError);
                        return "";
                    }
                });
            } catch (e) {

            }

        })


        //
        $(document).on("click", ".dislikes", function () {
            try {
                $(this).attr("class", "ml-2 fa fa-thumbs-down fa-2x");
                var id = $(this).attr("data-id");

                var soru1 = {
                    "soru": txtSoru
                };
                $.ajax({
                    url: 'api/api/faqFullMultiple',
                    async: true,
                    dataType: 'json',
                    type: 'get',
                    // data: JSON.stringify(soru1),
                    data: "{}",
                    contentType: 'application/json; charset=utf-8',
                    success: function (data) {
                        var metin = "";
                        data = $.parseJSON(data);
                        console.log(data);
                        if (data.Response != null) {
                            if (data.Response == 200) {
                                // $("#txtCosunus").val(data.Cevap);
                                var i = 1;
                                metin = "<p class='msg'>Aşağıda sorulardan hangisi sorduğunuz soruya yakındır.</br></br> ";
                                metin += "<span id='btn_rnn_" + data.CevapRnnID + "' class='btn btn-success mb-2 selectquestion' style='font-size:10px; width:100%;' data-id='" + data.CevapRnnID + "'>1- " + data.CevapRnnSoru + "</span></br>";
                                metin += "<span id='btn_rnn_" + data.CevapBernouilliID + "' class='btn btn-success mb-2 selectquestion' style='font-size:10px; width:100%;' data-id='" + data.CevapBernouilliID + "'>2-" + data.CevapBernouilliSoru + "</span></br>";
                                metin += "<span id='btn_rnn_" + data.CevapLstmID + "' class='btn btn-success mb-2 selectquestion' style='font-size:10px; width:100%;;' data-id='" + data.CevapLstmID + "'>3- " + data.CevapLstmSoru + "</span></br>";
                                metin += "<span id='btn_rnn_" + data.CevapANNID + "' class='btn btn-success mb-2 selectquestion' style='font-size:10px; width:100%;' data-id='" + data.CevapANNID + "'>4- " + data.CevapANNSoru + "</span>";
                                var chat = $("#chat").text();
                                var tmp = " <div class='d-flex align-items-center text-right justify-content-end '>";
                                tmp += "<div class='pr-2'>";
                                tmp += '<span class="name">Sanal Asistan</span>';
                                tmp += '' + metin + '';
                                tmp += '<br /><br /><span class="text-right">';
                                tmp += ' <i class="fa fa-thumbs-o-up fa-2x likes" data-ID=' + data.SoruID + ' aria-hidden="true"></i>';
                                tmp += '<i class="fa fa-thumbs-o-down fa-2x ml-2 dislikes" data-ID=' + data.SoruID + ' aria-hidden="true"></i>';
                                tmp += '</span></p>';
                                tmp += "</div>";

                                tmp += "<div>";
                                tmp += ' <img src="img/robot.png" width="30" class="img1" />';
                                tmp += "</div>";

                                tmp += "</div>";

                                var chat = $("#chat").html();

                                chat = chat + tmp;
                                $("#chat").html(chat);
                                $("#chat").animate({ scrollTop: $('#chat').prop("scrollHeight") }, 1000);
                                $("#txtSoru").val("");
                            }
                            else {
                                alert("hata " + data.Cevap);
                                return "";
                            }
                        }
                        else {
                            if (data.length > 0) {
                                metin = "<p class='msg'>Aşağıda sorulardan hangisi sorduğunuz soruya yakındır.</br></br> ";
                                for (var i = 0; i < data.length; i++) {
                                    metin += "<span id='btn_" + data[i].ID + "' class='btn btn-success mb-2 selectquestion' style='font-size:10px; width:100%;' data-id='" + data[i].ID + "'>" + (i + 1) + "- " + data[i].Soru + "</span></br>";
                                }
                                var chat = $("#chat").text();
                                var tmp = "</p> <div class='d-flex align-items-center text-right justify-content-end '>";
                                tmp += "<div class='pr-2'>";
                                tmp += '<span class="name">Sanal Asistan</span>';
                                tmp += '' + metin + '';
                                tmp += "</div>";

                                tmp += "<div>";
                                tmp += ' <img src="img/robot.png" width="30" class="img1" />';
                                tmp += "</div>";

                                tmp += "</div>";

                                var chat = $("#chat").html();

                                chat = chat + tmp;
                                $("#chat").html(chat);
                                $("#chat").animate({ scrollTop: $('#chat').prop("scrollHeight") }, 1000);
                                $("#txtSoru").val("");

                            }
                            else {
                            var chat = $("#chat").text();
                            var tmp = " <div class='d-flex align-items-center text-right justify-content-end '>";
                            tmp += "<div class='pr-2'>";
                            tmp += '<span class="name">Sanal Asistan</span>';
                            tmp += '<p class="msg">ooops! Soruyu anlayamadım. Soruyu farklı şekilde sorar mısın?';
                            tmp += '<br /><br /><span class="text-right">';
                            tmp += '</span>';
                            tmp += "</p>";
                            tmp += "</div>";

                            tmp += "<div>";
                            tmp += ' <img src="img/robot.png" width="30" class="img1" />';
                            tmp += "</div>";

                            tmp += "</div>";

                            var chat = $("#chat").html();

                            chat = chat + tmp;
                            $("#chat").html(chat);
                            $("#chat").animate({ scrollTop: $('#chat').prop("scrollHeight") }, 1000);
                            }
                        }
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        alert(xhr.responseText);
                        console.log(thrownError);
                        return "";
                    }
                });
            } catch (e) {

            }

        })
    </script>
</body>
</html>
