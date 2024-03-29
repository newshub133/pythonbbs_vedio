function bindEmailCaptchaClick(){
    $('#captcha-btn').click(function (event) {
        let $this = $(this);
        // 阻止默认的事件
        event.preventDefault();

        let email = $("input[name='email']").val();

        $.ajax({
            url: '/auth/captcha/email?email=' + email,
            method: 'GET',
            success: function (result) {
                let code = result['code'];
                if(code == 200){
                    let countdown = 60;
                    // 取消按钮点击事件
                    $this.off('click');
                    var timer = setInterval(function(){
                        $this.text(countdown);
                        countdown -= 1;
                        if(countdown <= 0){
                            // 清除定时器
                            clearInterval(timer);
                            // 将按钮文字恢复
                            $this.text("获取验证码");
                            // 恢复点击
                            bindEmailCaptchaClick();
                        }
                    }, 1000);
                    // alert('邮箱验证码发送成功！')
                }else{
                    alert(result);
                }
            },
            fail: function (error) {
                console.log(error);
            }
        })
    });
}


$(function () {
    // todo：绑定按钮点击事件之前还要再加上判断，输入了邮箱才可以点击
    bindEmailCaptchaClick();
});