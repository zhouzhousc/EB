var tr = document.getElementsByTagName("tr");
var td;
for(var i = 0 ; i < tr.length ; i++){
	td = tr[i].getElementsByTagName("td");
	td[td.length-1].style.borderRight = "1px solid rgba(201, 201, 201, 1)";
	td[0].style.fontFamily = "'思源黑体CN Regular', '思源黑体CN'";
	td[0].style.fontSize = "14px";
}
var bo_td = document.getElementsByClassName("bottom_td");
for(var i = 0 ; i < bo_td.length ; i++){
	bo_td[i].style.borderBottom = "1px solid rgba(201, 201, 201, 1)";
}
window.onload = function(){
    //1.获取表格
    var tblEle = document.getElementById("table");
    //2.获取表格中tbody里面的行数(长度)
    var len = tblEle.tBodies[0].rows.length;
    //alert(len);
    //3.对tbody里面的行进行遍历
    for(var i=0;i<len;i++){
        if(i%2==0){
        //4.对偶数行设置背景颜色
            tblEle.tBodies[0].rows[i].style.backgroundColor="rgba(242, 242, 242, 1)";
        }else{
            //5.对奇数行设置背景颜色
            tblEle.tBodies[0].rows[i].style.backgroundColor="rgba(255, 255, 255, 1)";
        }
    }
}
