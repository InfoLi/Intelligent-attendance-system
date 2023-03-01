$(function() {
      $("#login").on('click',function(){
       var form1 = $("#form1").val();
       var form2 = $("#form2").val();
        $.post('./deal',data={'username':form1,'password':form2,'method':'login'},function(ret){
           if(ret==='admin'){
                window.location.replace("/admin/home");
            }
           else{
                 window.location.replace("/person/home");
              }
                  })
       });
 });