document.addEventListener("DOMContentLoaded", function(){
    const input_old = document.getElementById("current-password");
    const input_new = document.getElementById("new-password");
    const input_repeat = document.getElementById("repeat-password");
    const btn_change = document.getElementById("change-password");

    btn_change.addEventListener("click", function() {
        const old_password = input_old.value;
        const new_password = input_new.value;
        const repeat_password = input_repeat.value;
        var check_valid = true;
        if (new_password != repeat_password) {
            document.getElementById("wrong-repeat").classList.remove("ok");
            document.getElementById("wrong-repeat").classList.add("not-ok");
            check_valid = false;
        };

        if (new_password.length < 6) {
            document.getElementById("too-short").classList.remove("ok");
            document.getElementById("too-short").classList.add("not-ok");
            check_valid = false;
        };

        if (new_password == old_password) {
            document.getElementById("same-old-pass").classList.remove("ok");
            document.getElementById("same-old-pass").classList.add("not-ok");
            check_valid = false;
        };




        if(check_valid){
            change_password(old_password, new_password)
                .then(function(data){
                    if(data.ok){
                        location.reload();
                        alert("Đổi mật khẩu thành công");
                    }
                    else{
                        document.getElementById("wrong-current").classList.remove("ok");
                         document.getElementById("wrong-current").classList.add("not-ok");
                    }
                })
                .catch(function (error) {
                    alert(error);
                });
        };
    });
});


function change_password(old_password, new_password){
    return new Promise(function(resolve, reject){
        const csrfToken = getCSRFToken();
        var data_send = JSON.stringify({
            old_password: old_password,
            new_password: new_password
        });

        $.ajax({
            url: 'change-password-admin/',
            method: 'post',
            dataType: 'json',
            data:  data_send,
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(data){
                resolve(data);
            },
            erorr: function () {
                reject("Có lỗi trong quá trình xử lý");
            },
        });
    });
}


//token
function getCSRFToken() {
    const cookies = document.cookie.split('; ');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].split('=');
        if (cookie[0] === 'csrftoken') {
            return cookie[1];
        }
    }
    return null;
}