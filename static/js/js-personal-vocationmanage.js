function cancelApply(form1) {
//       var TB = document.getElementsByTagName('tbody')[line];
//       var form1=TB.rows[0].cells[4].innerHTML;
      if (confirm("您真的确定要删除吗？\n\n请确认！")==true){
          $.post('/deal',data={'method':'cancelApply','canselApplyTime':form1},function(ret){
               if(ret==='yes'){
                    alert("申请已取消");
//                    windows.location.reload();
               }
               else{
                    alert("取消失败稍后重试");
               }
          });
       }else{
         return false;
       }


}