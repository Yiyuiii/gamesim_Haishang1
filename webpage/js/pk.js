console.log("pk.js在工作！")
$(document).ready(function () {
    setInterval(function () {
        if (!pk.bid) return;
        pk.bidmsg2();
        pk.bid_check();

        var v=time()-pk.data.date;
        var c="";
        if (v<120)
        {
            v=Math.floor(v/3)+15;
            c+="每投<h4 style='color: yellow'>"+v+"</h4>券<br>险金<h4 style='color: #66ff99'>+1%</h4>";
        }
        else
        {
            v=25-Math.floor((v-120)/3);
            c+="每投<h4 style='color: yellow'>"+v+"</h4>券<br>险金<h4 style='color: #ff0033'>-1%</h4>";
        }

        $("#baoxian").html(c);
    },1000)
});

function doSave(value, type, name) {
            var blob;
            if (typeof window.Blob == "function") {
                blob = new Blob([value], {type: type});
            } else {
                var BlobBuilder = window.BlobBuilder || window.MozBlobBuilder || window.WebKitBlobBuilder || window.MSBlobBuilder;
                var bb = new BlobBuilder();
                bb.append(value);
                blob = bb.getBlob(type);
            }
            var URL = window.URL || window.webkitURL;
            var bloburl = URL.createObjectURL(blob);
            var anchor = document.createElement("a");
            if ('download' in anchor) {
                anchor.style.visibility = "hidden";
                anchor.href = bloburl;
                anchor.download = name;
                document.body.appendChild(anchor);
                var evt = document.createEvent("MouseEvents");
                evt.initEvent("click", true, true);
                anchor.dispatchEvent(evt);
                document.body.removeChild(anchor);
            } else if (navigator.msSaveBlob) {
                navigator.msSaveBlob(blob, name);
            } else {
                location.href = bloburl;
            }
        }
		
var pk={
    mp:0,waiting:"",bid_money:0,bid_team:0,div:[],
    game_round: function (dt)
    {
        Adventure.data.round=dt.round;
        this.clock.html("<span class='ts'>"+(25-dt.round)+"回合"+"</span>");
        this.bid_refresh2();
    },
    bid_check:function ()
    {
        if (pk.bid_money>0)
        {
            if (pk.data.flag=="比赛" || Adventure.is_adventure)
            {
                pk.bid_money=0;
                return;
            }
            if (pk["list"+pk.bid_team][myinfo.user.un]*1>=500)
            {
                pk.bid_money=0;
                return;
            }
            var num=Math.floor(pk.bid_money/16+1);
            if (num>30) num=30;
            if (num>pk.bid_money) num=pk.bid_money;
            pk.bid_money-=num;
            server.Send({type:"pk_buy",p:pk.bid_team,num:num});
        }
    },
    bid_refresh2: function () {
        var c="",v;
        if (gameControl.screen=="横版")
        {
            v=this.list1[myinfo.user.un];
            if (!v) v=0;
            c+="<table width='80%'><tr><td width='33%'>";
            c+="总投资: $"+this.data.total1;
            c+="</td>";
            c+="<td width='33%'>";
            if (v==0) c+="已投资: $"+v; else c+="已投资: <h2 style='color: yellow'>$"+v+"</h2>";
            c+="</td>";
            c+="<td width='33%'>";
            v=1;
            v+=(pk.data.total2*1+10)/(pk.data.total1*1+10)*0.8;
            v=int1(v);
            if (v<1.1) v=1.1;
            v=Math.floor(v*100);
            c+="回报率:<br><h4 style='color: white'>"+v+"</h4>%";
            c+="</td>";
            c+="</tr></table>";
            this.info1.html(c);
            this.info1.find("td").css("color","white");

            c="";
            c+="<table width='80%'><tr><td width='33%'>";
            v=1;
            v+=(pk.data.total1*1+10)/(pk.data.total2*1+10)*0.8;
            v=int1(v);
            if (v<1.1) v=1.1;
            v=Math.floor(v*100);
            c+="回报率:<br><h4 style='color: white'>"+v+"</h4>%";
            c+="</td>";
            c+="<td width='33%'>";
            v=this.list2[myinfo.user.un];
            if (!v) v=0;
            if (v==0) c+="已投资: $"+v; else c+="已投资: <h2 style='color: yellow'>$"+v+"</h2>";
            c+="</td>";
            c+="<td width='33%'>";
            c+="总投资: $"+this.data.total2+"";
            c+="</td>";
            c+="</tr></table>";
            this.info2.html(c);
            this.info2.find("td").css("color","white");
        }
        else
        {
            c+="<table width='100%'><tr>";
            c+="<td width='33%'>";
            v=1;
            v+=(pk.data.total2*1+10)/(pk.data.total1*1+10)*0.8;
            v=int1(v);
            if (v<1.1) v=1.1;
            v=Math.floor(v*100);
            c+="<span style='color: #999999'>回报率:</span><br>"+v+"%";
            c+="</td>";

            v=this.list1[myinfo.user.un];
            if (!v) v=0;
            c+="<td width='33%'>";
            c+="<span style='color: #999999'>已投资:</span> <br>";
            if (v==0) c+="$"+v; else c+="<h4 style='color: yellow' class='ts'>$"+v+"</h4>";
            c+="</td>";

            c+="<td width='33%'>";
            c+="<span style='color: #999999'>总投资: </span><br>$"+this.data.total1;
            c+="</td>";
            c+="</tr></table>";
            this.info1.html(c);
            this.info1.find("td").css("color","white");

            c="";
            c+="<table width='100%'><tr>";
            v=1;
            v+=(pk.data.total1*1+10)/(pk.data.total2*1+10)*0.8;
            v=int1(v);
            if (v<1.1) v=1.1;
            v=Math.floor(v*100);
            c+="<td width='33%'>";
            c+="<span style='color: #999999'>回报率:</span><br>"+v+"%";
            c+="</td>";
            c+="<td width='33%'>";
            v=this.list2[myinfo.user.un];
            if (!v) v=0;
            c+="<span style='color: #999999'>已投资:</span> <br>";
            if (v==0) c+="$"+v; else c+="<h4 style='color: yellow' class='ts'>$"+v+"</h4>";
            c+="<td>";
            c+="<td width='33%'>";
            c+="<span style='color: #999999'>总投资:</span> <br>$"+this.data.total2+"";
            c+="</td>";
            c+="</tr></table>";
            this.info2.html(c);
            this.info2.find("td").css("color","white");


        }
    },
    mst_upgrade: function (dt)
    {
        var dna;
        if (dt.p==1) dt.y=5-dt.y;
        var m0=this.data["monsters"+dt.p].split(";");

        var list="";
        for (var i in m0)
        {
            if (m0[i]=="") continue;
            var m2=m0[i].split(",");
            if (m2[1]==dt.x && m2[2]==dt.y)
            {
                m2[3]=dt.dna;
                var m4=m2[3].split("|");
                m2[4]=m4.length-1;
            }
            list+=m2[0]+","+m2[1]+","+m2[2]+","+m2[3]+","+m2[4]+";";
        }
        this.data["monsters"+dt.p]=list;

        var m=monster.find({x:dt.x,y:dt.y});
        if (!m) return;
        m=m[0];
        dna=dt.dna.split("|");
        Movies.play("kaibaoxiang", m.x, m.y,2);

        m.data.dna=dna;
        m.scheduleOnce(function () {
            var it=this.item.split(":");
            if (it[0]=="宝物")
            {
                m.msg(it[1],res_domain+"img/adventure/"+this.img);
            }
            else
            {
                m.msg(this.item);
            }
        }.bind({item:dt.item,img:dt.img}),1);
        m.set_upgrade(1);
    },
    buy0: function (team,num)
    {
        if (myinfo.user.money*1<num)
        {
            floatwin.msg("失败，魔法券不足");
            return;
        }
        if (pk.data.flag=="比赛") return;
        if (pk["list"+team][myinfo.user.un]*1>=500) return;
        if (this.bid_team!=team) this.bid_money=0;
        this.bid_team=team;

        if (this.bid_money+num+pk["list"+team][myinfo.user.un]*1>500)
        {
            this.bid_money=500-num-pk["list"+team][myinfo.user.un]*1
        }
        else
        {
            this.bid_money+=num;
        }
    },
    buy: function (dt)
    {
        if (!this["list"+dt.p]) return;
        if (!this["list"+dt.p][dt.un])
        {
            this["list"+dt.p][dt.un]=dt.num*1;
            //this["insurance"+dt.p][dt.un]=dt.insurance*1;
        }
        else
        {
            this["list"+dt.p][dt.un]=this["list"+dt.p][dt.un]*1+dt.num*1;
            //this["insurance"+dt.p][dt.un]=dt.insurance*1;
        }
        this.data["total"+dt.p]=this.data["total"+dt.p]*1+dt.num*1;

        this.bidmsg(dt);
        this.bid_refresh();
    },
    game_start: function ()
    {
        this.bid_money=0;
        server.Send({type:"pk_watch",is_game:1});
    },
    monster_refresh: function ()
    {
        monster.remove_all();
        for (var team=1;team<=2;team++)
        {
            var m=this.data["monsters"+team].split(";");
            for (var i in m)
            {
                if (m[i]=="") continue;
                var m2=m[i].split(",");
                var dna="";
                if (m2[3]) dna=m2[3].split("|");
                if (team==1) m2[2]=5-m2[2];
                challenge.monster_add({name:m2[0],x:m2[1],y:m2[2],dna:dna,team:team});
            }
        }
    },
    bid_refresh: function ()
    {
        myinfo.refresh_user();
        this.bid_refresh2();
        if (!this.btn1) return;
        this.btn1.unbind();
        this.btn2.unbind();
        this.btn1.click(function () {
            var c="";
            c+="投资1队<p>";
            c+="<button>10魔法券</button>";
            c+="<button>30魔法券</button>";
            c+="<button>100魔法券</button>";
            c+="<button>200魔法券</button>";
            c+="<button>500魔法券</button>";
            var div=floatwin.show_html(c);
            div.find("button").click(function () {
                var id=div.find("button").index(this);
                var num=[10,30,100,200,500];
                pk.buy0(1,num[id]);
                floatwin.hide();
            })
        });

        this.btn2.click(function () {
            var c="";
            c+="投资2队<p>";
            c+="<button>10魔法券</button>";
            c+="<button>30魔法券</button>";
            c+="<button>100魔法券</button>";
            c+="<button>200魔法券</button>";
            c+="<button>500魔法券</button>";
            var div=floatwin.show_html(c);
            div.find("button").click(function () {
                var id=div.find("button").index(this);
                var num=[10,30,100,200,500];
                pk.buy0(2,num[id]);
                floatwin.hide();
            })
        });
    },
    bidmsg2: function ()
    {
        var c="",color;
        if (gameControl.screen=="竖版")
        {
            for (var i in this.bid)
            {
                this.bid[i].cdt--;
                if (this.bid[i].cdt<=0) continue;
                if (this.bid[i].team==1) color="rgba(150,50,0,0.5)"; else color="rgba(50,100,150,0.5)";
                c+="<span style='background-color: "+color+"; border-radius: 5px; padding: 6px; margin: 5px; color: white; min-width: 200px;'>";
                c+=this.bid[i].team+"队:"+this.bid[i].un+"+$"+this.bid[i].bid;
                c+="</span>";

                if (this.bid[i].insurance>0)
                {
                    c+="<span style='background: rgba(0,0,0,0.5); font-size: 12px; color: #33ff99'>";
                    c+="+"+this.bid[i].insurance+"%";
                    c+="</span>";
                }
                if (this.bid[i].insurance<0)
                {
                    c+="<span style='background: rgba(0,0,0,0.5); font-size: 12px; color: #ff0033'>";
                    c+=""+this.bid[i].insurance+"%";
                    c+="</span>";
                }

                c+="<br>";
            }
            var div=this.msg.find("td");
            div.html(c);
        }
        else
        {
            if (!this.msg1) return;
            var c1="",c2="";
            for (var i in this.bid)
            {
                this.bid[i].cdt--;
                if (this.bid[i].cdt<=0) continue;
                if (this.bid[i].team==1)
                {
                    color="rgba(150,50,0,0.5)";
                    c1+="<span style='background-color: "+color+"; border-radius: 5px; padding: 6px; margin: 5px; color: white; min-width: 200px;'>";
                    c1+=this.bid[i].team+"队:"+this.bid[i].un+"+$"+this.bid[i].bid;
                    c1+="</span>";

                    if (this.bid[i].insurance>0)
                    {
                        c1+="<span style='background: rgba(0,0,0,0.5); font-size: 12px; color: #33ff99'>";
                        c1+="+"+this.bid[i].insurance+"%";
                        c1+="</span>";
                    }
                    if (this.bid[i].insurance<0)
                    {
                        c1+="<span style='background: rgba(0,0,0,0.5); font-size: 12px; color: #cc0033'>";
                        c1+=""+this.bid[i].insurance+"%";
                        c1+="</span>";
                    }

                    c1+="<br>";
                }
                else
                {
                    color="rgba(50,100,150,0.5)";
                    c2+="<span style='background-color: "+color+"; border-radius: 5px; padding: 6px; margin: 5px; color: white; min-width: 200px;'>";
                    c2+=this.bid[i].team+"队:"+this.bid[i].un+"+$"+this.bid[i].bid;
                    c2+="</span>";

                    if (this.bid[i].insurance>0)
                    {
                        c2+="<span style='background: rgba(0,0,0,0.5); font-size: 12px; color: #33ff99'>";
                        c2+="+"+this.bid[i].insurance+"%";
                        c2+="</span>";
                    }
                    if (this.bid[i].insurance<0)
                    {
                        c2+="<span style='background: rgba(0,0,0,0.5); font-size: 12px; color: #ff0033'>";
                        c2+=""+this.bid[i].insurance+"%";
                        c2+="</span>";
                    }
                    c2+="<br>";
                }
            }
            var div=this.msg1.find("td");
            div.html(c1);
            div=this.msg2.find("td");
            div.html(c2);
        }

        /*
        for (var i in this.bid)
        {
            if (this.bid[i].cdt<=0)
            {
                this.bid.splice(i,1);
                i--;
            }
        }*/
    },
    bidmsg: function (dt)
    {
        for (var i in this.bid)
        {
            if (this.bid[i].un==dt.un && this.bid[i].team==dt.p)
            {
                this.bid[i].bid+=dt.num*1;
                this.bid[i].cdt=3;
                if (dt.insurance) this.bid[i].insurance=dt.insurance;
                return;
            }
        }
        this.bid.push({bid:dt.num*1,cdt:3,team:dt.p,un:dt.un})
    },
    read: function (dt)
    {
        this.data=dt.data;
        var c;

        if (gameControl.screen=="横版")
        {
            this.clock=create_div({left:50,top:50,width:200});
            c="<table cellspacing='0' cellpadding='0' style='width: 100%; height: 100%;'><tr><td style='overflow: hidden' valign='middle' align='center'></td></tr></table>";
            this.msg1=create_div({left:20,top:50,width:600, height:500});
            this.msg1.css("line-height","36px");
            this.msg1.css("pointer-events","none");
            this.msg1.html(c);
            c="<table cellspacing='0' cellpadding='0' style='width: 100%; height: 100%;'><tr><td style='overflow: hidden' valign='middle' align='center'></td></tr></table>";
            this.msg2=create_div({left:80,top:50,width:600, height:500});
            this.msg2.css("line-height","36px");
            this.msg2.css("pointer-events","none");
            this.msg2.html(c);
        }
        else
        {
            this.clock=create_div({left:10,top:52,width:200});
            c="<table cellspacing='0' cellpadding='0' style='width: 100%; height: 100%;'><tr><td style='overflow: hidden' valign='middle' align='center'></td></tr></table>";
            this.msg=create_div({left:50,top:50,width:gameControl.width, height:700});
            this.msg.css("line-height","36px");
            this.msg.css("pointer-events","none");
            this.msg.html(c);
        }
        c="";
        if (this.data.flag=="下注")
        {
            c+="<br><span class='ts' style='color: white' id='baoxian'></span>";
            c+="<br><span class='span_cdt ts' style='color: white'>"+(this.data.date*1+180)+"</span>";
        }
        else
        {
            if (gameControl.screen=="横版")
            {
                c+="<button onclick='pk.watch()'>观战</button>";
            }
            else
            {
                c+="<button onclick='pk.watch()'>观战</button>";
                this.clock[0].data.left=50;
            }
        }
        this.clock.attr("align","center");
        this.clock.css("z-index",10);
        this.clock.html(c);

        this.back=create_div({left:95,top:12});
        this.back.html("<img src='"+res_domain+"img/zhandou/fanhui.png'>");
        this.back.find("img").click(function () {
            gameControl.gohome();
        });

        this.insurance1=[];
        this.insurance2=[];
        this.list1=[];
        this.list2=[];
        push_data(this.list1,dt.data.list1);
        push_data(this.list2,dt.data.list2);
        this.monster_refresh();
        this.bid_refresh();

        resize();
    },
    watch3: function (dt)
    {

    },
    watch2: function (sid, un2)
    {
        gameControl.screen_mode=0;

        server.ip0=server.ip;
        server.ip="mxj"+sid+".seagame.com";
        server.un2=un2;
        server.skt.close();
    },
    watch: function (un)
    {
        if (!un)
        {
            server.Send({type:"pk_watch",is_game:1});
        }
        else
        {
            server.Send({type:"pk_watch",un:un});
        }
    },
	downTxt: function ()
    {
        doSave(this.data["monsters1"]+"-"+this.data["monsters2"], "text/plain", "jjc.txt");
		console.log(this.data["monsters1"])
		console.log(this.data["monsters2"])
    },
    init2: function () {
        var c;
        myinfo.banner_init();
        myinfo.refresh_user();
        if (gameControl.screen=="横版")
        {
            this.clock=create_div({left:50,top:50,width:200});

            this.info1=create_div({left:25,top:95,width:gameControl.width/2.1,height:100});
            this.info1.css("background","rgba(0,0,0,0.5)");
            this.info1.css("color","white");
            this.info1.css("border-radius","5px");
            this.info1.addClass("middle");

            this.info2=create_div({left:75,top:95,width:gameControl.width/2.1,height:100});
            this.info2.css("background","rgba(0,0,0,0.5)");
            this.info2.css("color","white");
            this.info2.css("border-radius","5px");
            this.info2.addClass("middle");

            this.chat=create_div({left:95,top:80});
            this.chat.html("<img src=img/ui/chat.png>");
            this.chat.click(function () {
                Chat.show();
            });

            this.btn1=create_div({left:5,top:95});
            this.btn1.html("<button class='button4'>投资</button>");
            this.btn2=create_div({left:55,top:95});
            this.btn2.html("<button class='button4'>投资</button>");

            this.btn3=create_div({left:90,top:80});
            this.btn3.html("<button class='button4'>保险</button>");
			
			this.btnDown=create_div({left:90,top:70});
            this.btnDown.html("<button class='button4'>txt</button>");
			this.btnRe=create_div({left:90,top:60});
            this.btnRe.html("<button class='button4'>更新</button>");
        }
        else
        {
            this.chat=create_div({left:95,top:50});
            this.chat.html("<img src=img/ui/chat.png>");
            this.chat.click(function () {
                Chat.show();
            });

            this.clock=create_div({left:10,top:52,width:200});
            this.info1=create_div({left:50,top:90,width:500});
            this.info1.css("background","rgba(0,0,0,0.5)");
            this.info1.css("border-radius","5px");
            this.info1.css("padding","5px");
            this.info1.addClass("middle");
            this.info1.addClass("ts");

            this.info2=create_div({left:50,top:12,width:500});
            this.info2.css("background","rgba(0,0,0,0.5)");
            this.info2.css("padding","5px");
            this.info2.css("border-radius","5px");
            this.info2.addClass("middle");
            this.info2.addClass("ts");

            this.btn1=create_div({left:10,top:90});
            this.btn1.html("<button class='button4'>投资</button>");
            this.btn2=create_div({left:10,top:12});
            this.btn2.html("<button class='button4'>投资</button>");

            this.btn3=create_div({left:92,top:90});
            this.btn3.html("<button class='button4'>保险</button>");
        }
        this.btn3.click(function () {
            Bank.show();
        });

		this.btnDown.click(function () {
            pk.downTxt();
        });
		this.btnRe.click(function () {
            pk.init();
        });
		
        this.clock.attr("align","center");
        this.clock.css("z-index",10);

    },
    init: function ()
    {
        gameControl.empty();
        $("#game").css("background","");
        Adventure.mode="竞技场";
        this.bid_money=0;
        this.bid=[];
        cc.director.runScene(new Adventure.cc.SCENE);
        server.Send({type:"pk_read"});
        /*
        cc.LoaderScene.preload(Images.res, function () {
            cc.director.runScene(new Adventure.cc.SCENE);
            server.Send({type:"pk_read"});
        }, this);*/
    }
};
