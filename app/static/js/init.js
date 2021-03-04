$(function () {
    init_share();
});

// 格式恢复
function init_share() {
    var text = $(".share").text(); //先取出未转换格式前端数据
    var des = text.replace(/\r\n/g, '<br/>').replace(/\n/g, '<br/>').replace(/\s/g, ' ');  //转换格式
    $(".share").empty();
    $(".share").append(des);
}