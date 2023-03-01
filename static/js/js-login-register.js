$(function() {
      $("#forRegister").on('click',function(){
       var form0 = $("#form0").val();
       var form1 = $("#form1").val();
       var form2 = $("#form2").val();
       var form3 = $('input[name=sex]:checked').val();
       var form4 = $("#form4").val();
       var form5 = $("#form5").val();
       var form6 = $("#form6").val();
       var form7 = $("#form7").val();
        $.post('/deal',data={'Name':form0,'userName':form1,'password':form2,'userSex':form3,'userRge':form4,'userDepartment':form5,'userPosition':form6,'userPhone':form7,'method':'register'},function(ret){
            if(ret==='注册失败'){
            alert("请稍后重试");}
           else{
                 var second = confirm("注册成功立即登录");
                 if(second){
                      window.location.replace("/person/home")
                  }
                  else{
                       alert("留在此页");
                  }
              }
                  })
       });
 });