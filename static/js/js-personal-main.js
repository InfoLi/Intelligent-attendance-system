function checkpassword() {
        var password = document.getElementById("pwdChange").value;
        var repassword = document.getElementById("pwdChangeAgain").value;

        if(password == repassword) {
           document.getElementById("tishi").innerHTML="<font color='green'>两次密码输入一致</font>";

        }else{
           document.getElementById("tishi").innerHTML="<font color='red'>两次输入密码不一致!</font>";

        }
}


$(function() {
            $("#changeinfo").click(function() {
                    var form1= document.getElementById("info1").innerText;
//                    var form2=document.getElementById("info2").innerText;
                    var form3=document.getElementById("info3").innerText;
                    var form4=document.getElementById("info4").innerText;
                    var form5=document.getElementById("info5").innerText;
                    var form6=document.getElementById("info6").innerText;
                    var form7=document.getElementById("info7").innerText;

                    $("#info1").remove();
//                    $("#info2").remove();
                    $("#info3").remove();
                    $("#info4").remove();
                    $("#info5").remove();
                    $("#info6").remove();
                    $("#info7").remove();


                    var htm = "";
                    htm=" <input type='text'  value= '"+form1+"'  id='newinfo1'>";
                    $('#coninfo1').append(htm);
//                    htm=" <input type='text'  value= '"+form2+"'  id='newinfo2'>";
//                    $('#coninfo2').append(htm);
//                    htm=" <input type='text'  value= '"+form3+"'  id='pwdChange'><br>";
//                    htm = "<select type='width:100px;'><option>30</option></select>";
                    htm = '';
//                    for ( var i = 18; i < 110; i++){
//
//                    }
                    htm +="<select id='newinfo3'  class='testme'><option>18</option><option>19</option><option>20</option><option>21</option><option>22</option><option>23</option><option>24</option><option>25</option><option>26</option><option>27</option><option>28</option><option>29</option>";
                    htm +="<option>30</option><option>31</option><option>32</option><option>33</option><option>34</option><option>35</option><option>36</option><option>37</option><option>38</option><option>39</option><option>40</option><option>41</option>";
                    htm +="<option>42</option><option>43</option><option>44</option><option>45</option><option>46</option><option>47</option><option>48</option><option>49</option><option>50</option></select>";
                    $('#coninfo3').append(htm);



                    htm="<select id='newinfo4' class='testme'><option>男</option><option>女</option></select>";
                    $('#coninfo4').append(htm);
                    htm="<select id='newinfo5' class='testme'><option>研发部</option><option>运维部</option><option>财务部</option><option>人事部</option></select>";
                    $('#coninfo5').append(htm);
                    htm="<select id='newinfo6' class='testme'><option>工程师</option><option>算法架构师</option><option>会计</option><option>业务员</option></select>";
                    $('#coninfo6').append(htm);
                    htm=" <input type='text'  value= '"+form7+"'  id='newinfo7'>";
                    $('#coninfo7').append(htm);

            });

            $("#infochangeconfrim").click(function() {
               var form1 = $("#newinfo1").val();
//               var form2 = $("#newinfo2").val();
               var form3 = $("#newinfo3").val();
               var form4 = $("#newinfo4").val();
               var form5 = $("#newinfo5").val();
               var form6 = $("#newinfo6").val();
               var form7 = $("#newinfo7").val();
               if(form4==='男'){
                  form4=1;
               }
               else{
                  form4=0;
               }

               $.post('/deal',data={'method':'changeBasicInfo','name':form1,'age':form3,'sex':form4,'apartment':form5,'position':form6,'pnum':form7},function(ret){
               if(ret==='yes'){
                    alert("修改成功");

               }
               else{
                    alert("修改失败稍后重试");
               }

               });
            });



            
            $("#changepwd").click(function() {

                    var htm = "";
                    htm += "    <div>";
                    htm += "    <input type='text' placeholder='请输入密码'  onkeyup='checkpassword()' id='pwdChange'><br>";
                    htm += "    <input type='password' placeholder='请再次确认' onkeyup='checkpassword()' id='pwdChangeAgain'>";
                    htm += "    </div>";
                    $('#pwdinputoption').append(htm);

            });
//            $("#pumchange").click(function() {
//
//                    var htm = "";
//                    htm += "    <div>";
//                    htm += "    <input type='text' placeholder='请输入手机号' id='pumChange'>";
//                    htm += "    </div>";
//                    $('#puminputoption').append(htm);
//
//            });
            $("#mailboxchange").click(function() {

                    var htm = "";
                    htm += "    <div>";
                    htm += "    <input type='text' placeholder='请输入邮箱'  id='mailboxChange'>";
                    htm += "    </div>";
                    $('#mailboxinputoption').append(htm);

            });

           $("#mailboxchangeconfrim").click(function() {
               var form1 = $("#mailboxChange").val();

               $.post('/user_register',data={'method':0,'pwdChange':form1},function(ret){
               if(ret==='yes'){
                    alert("绑定成功");
               }
               else{
                    alert("绑定失败稍后重试");
               }

               });
          });



          $("#pwdchangeconfrim").click(function() {
               var form1 = $("#pwdChange").val();

               $.post('/user_register',data={'method':0,'pwdChange':form1},function(ret){
               if(ret==='yes'){
                    alert("修改成功");
               }
               else{
                    alert("修改失败稍后重试");
               }

            });

          });

});
