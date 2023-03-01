$(function() {

   $("#askforleave").on('click',function(){

       var form1 = $("#startTime").val();
       var form4 = $("#endTime").val();
       var form7 = $("#leavereason").val();
       var form8 = $("#pvdepartment").val();
//       alert(111);
//       form1=form1+'-'+form2+'-'+form3
//       form4=form4+'-'+form5+'-'+form6
       $.post('/deal',data={'starttime':form1,'endtime':form4,'reason':form7,'department':form8,'method':'apply'},function(ret){
               if(ret=="yes"){
                    alert("申请已提交");
               }
               else{
                    alert("提交失败稍后重试");
               }

        })
   });

});