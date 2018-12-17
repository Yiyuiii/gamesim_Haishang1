console.log("bbs.js在工作！")
$(document).ready(function () {
    var ww=$(window).width();

    BBS.bg=$("<div style='position:fixed; z-index: 19; left: 0; top:0; background-color: rgba(0,0,0,0.6);'></div>");
    BBS.bg.appendTo(document.body);
    BBS.bg.css("width",ww);
    BBS.bg.css("height","100%");
    BBS.bg.hide();
    BBS.bg.appendTo(document.body);
    BBS.bg.click(function () {
        BBS.hide();
    });
    BBS.is_visible=false;



});
var BBS={
    head_size:40,
    set_left: function (c)
    {
        if (gameControl.screen=="竖版")
        {
            c="<div style='padding: "+(60*gameControl.scale)+"px; height: 100%;'>"+c+"</div>";
        }
        $("#bbs1").html(c);
    },
    set_right: function (c)
    {
        if (gameControl.screen=="横版")
        {
            $("#bbs2").html(c);
        }
        else
        {
            this.set_left(c);
        }
    },
    hide: function () {
        this.div.hide();
        this.bg.hide();
        this.div.cha.hide();
        BBS.is_visible=false;
    },
    show: function ()
    {
        BBS.is_visible=true;
        var ww=$(window).width(),w,h;

        BBS.is_manager=true;
        var c="";
        if (!this.div)
        {
            if (gameControl.screen=="横版")
            {
                BBS.div=$("<div align='center' style='position:fixed; z-index: 20; left: 0; top:0; background: url(img/ui/book.png) no-repeat; background-size: contain'></div>");
                c+="<table width='95%' cellpadding='5' style='height: 100%;'><tr><td id='bbs1' width='50%' align='center' valign='middle'></td><td id='bbs2' width='50%' align='center' valign='middle'></td></tr></table>";
                BBS.div.html(c);
            }
            else
            {
                BBS.div=$("<div id='bbs1' style='position:fixed; z-index: 20; left: 0; top:0; background: url(img/ui/shu2.png) no-repeat; background-size: contain;'></div>");
            }
            BBS.div.appendTo(document.body);

            c="<div id='msg_close' style='position: fixed; z-index: 51; cursor: pointer; '>";
            var w=gameControl.scale*100;
            c+="<img src='img/ui/cha.png' width='"+w+"'>";
            c+="</div>";
            BBS.div.cha=$(c);
            BBS.div.cha.hide();
            BBS.div.cha.appendTo(document.body);
            BBS.div.cha.click(function () {
                BBS.hide();
            });
        }

        var top=($(window).height()-this.div.cha.height())/2;
        this.div.cha.css("top",top);
        if (gameControl.screen=="横版")
        {
            this.div.cha.css("left",(ww-this.div.width())/2+this.div.width()-this.div.cha.width());
            this.div.cha.css("top",gameControl.top);
        }
        else
        {
            this.div.cha.css("left",gameControl.left+this.div.width()-this.div.cha.width());
        }
        this.div.cha.show();

        if (gameControl.screen=="横版")
        {
            w=gameControl.scale*1194;
            h=gameControl.scale*753;
        }
        else
        {
            w=gameControl.scale*750;
            h=gameControl.scale*1149;
        }
        BBS.div.css("width",w);
        BBS.div.css("height",h);
        var top=($(window).height()-this.div.height())/2;
        var left=(ww-this.div.width())/2;
        this.div.css("top",top);
        this.div.css("left",left);
        this.div.cha.css("top",top);
        this.div.show();

        this.div.cha.css("left",this.div.width()+left-this.div.cha.width());

        this.set_left("读取中...");
        this.set_right("请选择版块");
        if (gameControl.screen=="横版")
        {
            $("#bbs1").css("padding-left",60*gameControl.scale);
            $("#bbs1").css("padding-right",30*gameControl.scale);
            $("#bbs2").css("padding-right",40*gameControl.scale);
            $("#bbs1").css("padding-top",20*gameControl.scale);
            $("#bbs2").css("padding-top",20*gameControl.scale);
            $("#bbs2").css("padding-bottom",30*gameControl.scale);
        }

        this.div.show();
        this.bg.show();
        this.bid=1;
        server.Send({type:"bbs_board_read"});
    },
    newtopic: function(dt)
    {
        var msg="<a href=# style='color: yellow; pointer-events: auto' onclick='BBS.reply_read("+dt.tid+")'>《"+nohtml(dt.title)+"》</a>";
        Chat.newmsg({un:dt.un,msg:msg});
        if (dt.un==myinfo.user.un)
        {
            BBS.reply_read(dt.tid,0)
        }
    },
    show2: function (dt)
    {
        var c="";
        var w=100*gameControl.scale;
        if (gameControl.screen=="竖版") w=200*gameControl.scale;
        this.board=dt.board;
        //c+="<p style='clear:both;'><h4>论坛</h4></p>";

        c+="<div class='middle'>";
        c+="<div>";
        for (var i in dt.board)
        {
            if (dt.board[i].sid<=0 || dt.board[i].sid==myinfo.sid || this.is_manager)
            {
                c+="<div onclick='BBS.topic_read("+i+",0)' style='float: left; margin: 10px;'>";
                c+="<img src='img/nation/city3.png' style='width: "+w+"px'><br>";
                c+="<h4>";
                c+=dt.board[i].msg;
                c+="</h4>";
                c+="<br><img src='img/icon_sm2/001_06.png'>";
                /*
                c+="<br>";
                c+="今:"+dt.board[i].today+"帖<br>";
                c+="昨:"+dt.board[i].yesterday+"帖";*/
                c+="</div>";
            }
            else
            {
                continue;
                c+="<div onclick='floatwin.msg(\"你是"+myinfo.sid+"区玩家，无法看外国论坛\")' style='float: left; margin: 10px;'>";
                c+="<img src='img/nation/city3.png' style='width: "+w+"px'><br>";
                c+="<h4>";
                c+=dt.board[i].msg;
                c+="</h4>";
                c+="<br><img src='img/icon_sm2/001_05.png'>";
                c+="</div>";
            }

        }
        c+="</div>";
        c+="</div>";

        this.set_left(c);
    },
    topic_read: function (id,pg)
    {
        if (id==-2)
        {
            BBS.show();
            return;
        }
        var bid=this.board[id].id;
        this.sid=this.board[id].sid;
        this.board_data=this.board[id];
        this.bid=bid;
        this.bid0=id;
        server.Send({type:"bbs_topic_read",bid:bid,pg:pg});
    },
    topic_read2: function (dt)
    {
        this.pg_topic=dt.pg;
        var c="";
        /*
        if (this.sid>0)
        {
            c+="<h4>"+this.sid+"区论坛</h4>";
        }
        else
        {
            c+="<h4>公共讨论区</h4>";
        }
        c+="<hr>";
*/
        if (!dt.topic) dt.topic={};
        if (dt.topic=={} && this.pg_topic==0)
        {
            //this.pg_topic--;
            $("#bbs2").find("button:eq(2)").attr("disabled",true);
            c+="暂无帖子<p>";
            if (this.sid>-1 || this.is_manager) c+="<button class='button2' onclick='BBS.topic_new()'>发帖</button>";
            this.set_right(c)
        }
        else if (dt.topic.id)
        {
            c+="<tr onclick='BBS.reply_read("+dt.topic.id+",0)'>";
            c+="<td>";
            c+=nohtml(dt.topic.title)+"<br>";
            c+=dt.topic.un;
            c+="</td>";
            c+="<td>";
            c+="<img src="+res_domain+"img/bbs/reply.png>";
            c+=dt.topic.reply;
            c+="</td>";
            c+="</tr>";
            $("#bbs2").find("tbody:eq(0)").append(c);
        }
        else
        {
            if (gameControl.screen=="竖版")
            {
                var x=$("#bbs1").height()-100;
                c+="<div align='left' style='height: "+x+"px; overflow-y: auto;'>";
            }
            else
            {
                c+="<div align='left' style='height: 80%; overflow-y: auto;'>";
            }
            for (var i in dt.topic)
            {
                c+="<div style='color: #999999; font-size: 12px; margin: 3px; margin-top: 10px;'>";
                c+="<b>";
                if (dt.topic[i].sid!=myinfo.sid && dt.topic[i].sid*1>0) c+=dt.topic[i].sid+"区";
                c+=dt.topic[i].un+"</b>";
                c+="("+cdate(time()-dt.topic[i].reply_date)+"前):";
                c+="</div>";
                if (dt.topic[i].is_top==1) c+="<img src=img/icon_sm2/arrow_up.png>";
                if (dt.topic[i].is_good==1) c+="<img src=img/icon_sm2/001_18.png>";
                c+="<span style='background: rgba(0,0,0,0.1); cursor: pointer; border-radius: 5px; padding: 5px;' onclick='BBS.reply_read(\""+dt.topic[i].id+"\",0)'>";
                c+=nohtml(dt.topic[i].title);
                c+="</span>";
                if (dt.topic[i].reply>0)
                {
                    c+="(+";
                    c+=dt.topic[i].reply;
                    c+=")";
                }
            }
            c+="</div>";

            var w=gameControl.scale*50;
            c+="<table width='100%'><tr>";
            c+="<td align='left'>";
            if (this.pg_topic>0)
            {
                c+="<img style='cursor: pointer' width='"+w+"' onclick='BBS.topic_read(BBS.bid0,BBS.pg_topic-1)' src='img/guanka/zuo.png'>";
            }
            else
            {
                c+="<img class='gray' width='"+w+"' src='img/guanka/zuo.png'>";
            }

            c+="</td>";
            c+="<td align='center' class='ts'>";
            if (this.sid>-1 || this.is_manager) c+="<button class='button3' onclick='BBS.topic_new()'>发帖</button>";
            if (gameControl.screen=="竖版")
            {
                c+="<button class='button3' onclick='BBS.show()'>返回</button>";
            }
            c+="</td>";
            c+="<td align='right'>";
            c+="<img style='cursor:pointer;' width='"+w+"' onclick='BBS.topic_read(BBS.bid0,BBS.pg_topic+1)' src='img/guanka/you.png'>";
            c+="</td>";
            c+="</tr></table>";



            this.set_right(c);
        }
    },
    reply_read: function (tid,pg) {
        if (this.is_visible==false) this.show();
        floatwin.hide();
        server.Send({type:"bbs_reply_read",tid:tid,pg:pg});
    },
    del_reply: function(rid)
    {
        if (!confirm("确定删楼吗？")) return;
        server.Send({type:"bbs_del_reply",rid:rid})
    },
    settop: function()
    {
        if (!confirm("确定吗？")) return;
        server.Send({type:"bbs_set_top",tid:this.tid})
    },
    setgood: function()
    {
        if (!confirm("确定吗？")) return;
        server.Send({type:"bbs_set_good",tid:this.tid})
    },
    del_topic: function()
    {
        if (!confirm("确定删整个帖子吗？")) return;
        server.Send({type:"bbs_del_topic",tid:this.tid})
    },
    follow: function () {
        server.Send({type:"bbs_follow",tid:this.tid})
    },
    reply_read2: function (dt) {
        if (dt.topic)
        {
            this.tid=dt.topic.id;
            this.topic=dt.topic;
            this.pg_reply=dt.pg;
            var c="";
            var h=gameControl.height_h5*0.8;
            c+="<div style='100%; height: "+h+"px; overflow-y: auto; overflow-x: hidden' align='center'>";
            c+="<p align='center'><h4>"+nohtml(dt.topic.title)+"</h4>";
            var v="";
            if (dt.follow==1 || myinfo.user.un==dt.topic.un) v="checked";
            c+="<br><input type='checkbox' "+v+" id='follow' onclick='BBS.follow()'><label for='follow' style='font-size: 12px; color: #666666'>关注本帖</label>";
            c+="</p>";
            c+="<table width='100%' id='reply'>";

            if (!dt.reply) dt.reply=[];
            for (var i=0;i<dt.reply.length;i++)
            {
                c+="<tr>";
                c+="<td style='line-height: 30px;'>";
                c+="<div style='float: left; padding: 10px; line-height: 18px;' align='center'>";
                c+="<img width='"+BBS.head_size+"' src='"+res_domain+"../headimg/"+dt.reply[i].head+"'><br>";
                if (this.pg_reply==0 && i==0) c+="楼主"; else c+=i*1+this.pg_reply*10+"楼";
                c+="</div>";
                c+=dt.reply[i].un;
                if (dt.reply[i].sid*1>0) c+="("+dt.reply[i].sid+"区)";
                c+=":<br>";
                c+=nohtml(dt.reply[i].content).replaceAll("\n","<br>");

                c+="<br>";
                c+="<span style='font-size: 12px; color: #999999'>";
                c+="发表于:"+cdate(time()-dt.reply[i].date)+"前 ";
                c+="</span>";
                if (this.is_manager)
                {
                    if (this.pg_reply==0 && i==0)
                    {
                        c+="<a style='color: #336699' href='#' onclick='BBS.del_topic()'>[删帖]</a>";
                        if (dt.topic.is_top==1)
                        {
                            c+="<a style='color: #336699' href='#' onclick='BBS.settop()'>[撤顶]</a>";
                        }
                        else
                        {
                            c+="<a style='color: #336699' href='#' onclick='BBS.settop()'>[置顶]</a>";
                        }
                        if (dt.topic.is_good==1)
                        {
                            c+="<a style='color: #336699' href='#' onclick='BBS.setgood()'>[撤精]</a>";
                        }
                        else
                        {
                            c+="<a style='color: #336699' href='#' onclick='BBS.setgood()'>[加精]</a>";
                        }
                    }
                    else
                    {
                        c+="<a style='color: #336699' href='#' onclick='BBS.del_reply("+dt.reply[i].id+")'>[删楼]</a>";
                    }
                }
                c+="</td>";

                c+="</tr>";
            }
            c+="</table>";
            c+="<table width='90%'>";
            c+="<tr>";
            c+="<td>";
            c+="回帖";
            c+="</td>";
            c+="<td>";
            c+="<textarea style='width: 100%' rows='4'></textarea>";
            c+="</td>";
            c+="</tr>";
            c+="</table>";
            var w=gameControl.scale*50;
            c+="<table width='100%'><tr>";
            c+="<td align='left'>";
            if (this.pg_reply>0)
            {
                c+="<img width='"+w+"' onclick='BBS.reply_read(BBS.tid,BBS.pg_reply-1)' src='img/guanka/zuo.png'>";
            }
            else
            {
                c+="<img class='gray' width='"+w+"' src='img/guanka/zuo.png'>";
            }

            c+="</td>";
            c+="<td width='80%' align='center'>";
            c+="第"+(this.pg_reply+1)+"页";
            c+="</td>";
            c+="<td align='right'>";
            c+="<img width='"+w+"' onclick='BBS.reply_read(BBS.tid,BBS.pg_reply+1)' src='img/guanka/you.png'>";
            c+="</td>";
            c+="</tr></table>";

            c+="<button class='button2' onclick='BBS.reply_new()'>回帖</button>";
            var ok=-2;
            for (var j in BBS.board)
            {
                if (dt.topic.bid==BBS.board[j].id)
                {
                    ok=j;
                    break;
                }
            }
            c+="<button class='button2' onclick='BBS.topic_read("+ok+","+this.pg_topic+")'>返回</button>";
            c+="<div id='bbs_msg'></div>";

            c+="</div>";
            this.set_right(c);
        }
        else
        {
            var c="";
            c+="<tr>";
            c+="<td>";
            c+="<div style='float: left; padding: 10px;' align='center'>";
            c+="<img width='"+BBS.head_size+"' src='"+res_domain+"../headimg/"+dt.head+"'><br>";
            c+="新回帖";
            c+="</div>";
            c+=dt.un+"(";
            c+=dt.sid+"区)<br>";
            c+=nohtml(dt.content);
            c+="</td>";
            c+="</tr>";
            $("#reply tbody").append(c);
        }
    },
    reply_new: function ()
    {
        var content=this.div.find("textarea").val();
        content=Word.filter(content);
        this.div.find("textarea").val("");
        server.Send({type:"bbs_reply_new",tid:this.tid,content:content,ok:1})
    },
    topic_new: function ()
    {
        var c="";
        c+="<div id='bbs_msg'></div>";
        c+="<table>";
        c+="<tr>";
        c+="<td>";
        c+="<input class='inputbox' placeholder='标题'>";
        c+="</td>";
        c+="</tr>";
        c+="<tr>";
        c+="<td>";
        c+="<textarea cols='35' rows='5'></textarea>";
        c+="</td>";
        c+="</tr>";
        c+="<tr>";
        c+="<td>";
        c+="<button class='button2' onclick='BBS.topic_new2()'>发帖</button>";
        c+="</td>";
        c+="</tr>";
        c+="</table>";
        this.div2=floatwin.msg(c);
    },
    topic_new2: function () {
        var title=this.div2.find("input:eq(0)").val();
        var content=this.div2.find("textarea").val();
        if (title.length<4)
        {
            $("#bbs_msg").html("标题不能少于4字");
            return;
        }
        if (content.length<4)
        {
            $("#bbs_msg").html("正文不能少于4字");
            return;
        }
        content=Word.filter(content);
        title=Word.filter(title);
        server.Send({type:"bbs_topic_new",bid:this.bid,content:content,title:title,ok:1});
        floatwin.hide();
    }
};