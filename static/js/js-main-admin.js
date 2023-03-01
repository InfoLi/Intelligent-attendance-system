// 获取指定名称的cookie
function getCookie(name){
    var strcookie = document.cookie;//获取cookie字符串
    var arrcookie = strcookie.split("; ");//分割
    //遍历匹配
    for ( var i = 0; i < arrcookie.length; i++) {
        var arr = arrcookie[i].split("=");
        if (arr[0] == name){
            return arr[1];
        }
    }
    return "";
}

//// 打印所有cookie
//function print() {
//    var strcookie = document.cookie;//获取cookie字符串
//    var arrcookie = strcookie.split(";");//分割
//
//    //遍历匹配
//    for ( var i = 0; i < arrcookie.length; i++) {
//        var arr = arrcookie[i].split("=");
//        console.log(arr[0] +"：" + arr[1]);
//    }
//}


function imgChange(img) {
    var user_id=getCookie('userName');
//    console.log(user_id);
    // 生成一个文件读取的对象
    const reader = new FileReader();
    reader.readAsDataURL(img.files[0]);


    reader.onload = function (ev) {
        // base64码
//        alert(reader.result);
        var imgFile =ev.target.result;//或e.target都是一样的
//        alert(typeof(imgFile))
         document.querySelector("img").src= imgFile;

         $.post('/deal',data={'name':user_id,'image':imgFile,'method':'insertPhoto'},function(ret){
           if(ret==='yes'){
            alert("上传成功");
            }
           else{
            alert("上传失败");
           }
         });




    }
    //发起异步读取文件请求，读取结果为data:url的字符串形式，
//    reader.readAsDataURL(img.files[0]);
//    alert("ssss");



}


window.onload=function(){
    var user_id=getCookie(userName)
    $.post('/user_register',data={'method':getUserPic,'name':user_id,'image':imgFile},function(imgFile){
           document.querySelector("img").src= imgFile;
//           document.querySelector("img").style.
    });

}
