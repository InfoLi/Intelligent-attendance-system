function queryApply(line) {

        var TB = document.getElementsByTagName('tbody')[line];
        var form1=TB.rows[0].cells[4].innerHTML;
        var form2=TB.rows[0].cells[0].innerHTML;
        var form3=TB.rows[0].cells[1].innerHTML;
        var form4=TB.rows[0].cells[2].innerHTML;
        var form5=TB.rows[0].cells[3].innerHTML;
//        alert(form1)
//        alert(form1+form2)
        $.post('/deal',data={'method':'returnDetailApply','ApplyTime':form1,'name':form2},function(ret){
            if(ret==='fail'){
                alert("查看失败");
            }
            else{
                 popWin.showWin("500","500","OA审批",form1,form2,form3,form4,form5,ret);
            }

        });
//       if (confirm("您真的确定要删除吗？\n\n请确认！")==true){
//          $.post('/user_register',data={'method':0,'canselApplyTime':form1},function(ret){
//               if(ret==='yes'){
//                    alert("申请已取消");
//                    windows.location.reload();
//               }
//               else{
//                    alert("取消失败稍后重试");
//               }
//
//          });
//       }else{
//         return false;
//       }


}

$(document).ready(function() {
$("#selectperson1").on('click' , function(){
popWin.showWin("500","500","OA审批","popup02.html");
});
});
