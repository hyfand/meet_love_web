$(function () {
    init_share();
});

// 格式恢复
function init_share() {
    $(".share").each(
        function(){
            var text = $(this).text(); //先取出未转换格式前端数据
            var des = text.replace(/\r\n/g, '<br/>').replace(/\n/g, '<br/>').replace(/\s/g, ' ');  //转换格式
            $(this).empty();
            $(this).append(des);
        }
    )
}

// 为ajax请求设置 csrf 令牌
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", $("#global-token").attr("token"))
        }
    }
})

// 点赞 start
$(document).on("click", ".praise-del", function () {
                 praise(this, -1)
            });
$(document).on("click", ".praise-add", function () {
                 praise(this, 1)
            });

function praise(dom, op) {
    var share = $(dom).parents(".share-data");
    var id = share.attr("data-id");
    var data = {
        "share_id": parseInt(id),
        "op": op
    }
    var url = "/share/praise_share";
    $.ajax(
        {
            url: url,
            type: "post",
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                if (data["status"] == "ok"){
                   var praise_num = parseInt($(dom).parent().text());
                   if (op == -1){
                       $(dom).next(".praise-num").text(praise_num-1);
                       $(dom).removeClass("praise-del").addClass("praise-add");
                       $(dom).css("color", "")
                   }
                   else {
                       $(dom).next(".praise-num").text(praise_num+1);
                       $(dom).removeClass("praise-add").addClass("praise-del");
                       $(dom).css("color", "red")
                   }
                }
            },
            error: function (error) {
                console.log(error)
            }
        }
    )
}
// 点赞 end