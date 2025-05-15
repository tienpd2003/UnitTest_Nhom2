document.addEventListener("DOMContentLoaded", function () {
    const input_file = document.getElementById("input-pdf-file");
    const input_title_newsfeed = document.getElementById("input-title");
    const add_btn = document.getElementById("add-newsfeed");
    const stt_hidden_select = document.getElementById("stt-hidden");

    //tim kiem tin tuc
    const search_value_input = document.getElementById("search-newsfeed-input");
    const search_btn = document.getElementById("search-newsfeed-btn");

    search_btn.addEventListener("click", function () {
        const search_value = search_value_input.value;
        if (search_value != "") {
            search_newsfeed(search_value)
                .then(function (data) {
                    fill_data_to_html(data);
                });
        };
    })

    //danh sach tin tuc
    search_newsfeed("all")
        .then(function (data) {
            fill_data_to_html(data);
        });
    //nut luu tin tuc
    add_btn.addEventListener("click", function () {
        const title_newsfeed = input_title_newsfeed.value;
        const file_pdf = input_file.files[0];
        const stt_hidden = stt_hidden_select.value;
        if (file_pdf) {
            const formData = new FormData();
            formData.append("title", title_newsfeed);
            formData.append("pdf_file", file_pdf);
            formData.append("stt_hidden", stt_hidden);
            upload_pdf_to_view(formData)
                .then(function (data) {
                    alert(data.message);
                })
        }
        else {
            alert("Hãy chọn file cần tải lên trước");
        };
    });

    //nut lam moi
    const refresh = document.getElementById("refresh");
    refresh.addEventListener("click", function () {
        location.reload();
    });

    //nut xoa tin
    const delete_btn = document.getElementById("delete-btn");
    delete_btn.addEventListener("click", function () {
        delete_newsfeed()
            .then(function (data) {
                alert(data.message);
                location.reload();
            });
    });

    // tim kiem newsfeed
    function search_newsfeed(value) {
        return new Promise(function (resolve, reject) {
            $.ajax({
                url: 'get-newsfeed/' + value + '/',
                method: 'get',
                dataType: 'json',
                success: function (data) {
                    resolve(data);
                },
                error: function () {
                    alert("Có lỗi trong quá trình xử lý");
                }
            });
        });

    }
});



    // dien du lieu vao bang
    function fill_data_to_html(data) {

        const list_newsfeed = document.getElementById("newsfeed-list");
        list_newsfeed.innerHTML = "";
        data.newsfeeds.forEach(function (newsfeed) {
            const newsfeed_div = document.createElement("div");

            const post_date_div = document.createElement("div");
            const post_date_span = document.createElement("span");
            post_date_span.textContent = newsfeed.post_date;
            post_date_div.appendChild(post_date_span);
            post_date_span.classList.add("span-post-date");
            newsfeed_div.appendChild(post_date_div);
            post_date_div.classList.add("div-post-date");

            const title_div = document.createElement("div");
            const title_span = document.createElement("span");
            title_span.textContent = newsfeed.title;
            title_div.appendChild(title_span);
            title_span.classList.add("span-title1");
            newsfeed_div.appendChild(title_div);
            title_div.classList.add("div-title");

            const is_hidden_div = document.createElement("div");
            const is_hidden_span = document.createElement("span");
            is_hidden_span.textContent = newsfeed.is_hidden;
            is_hidden_div.appendChild(is_hidden_span);
            is_hidden_span.classList.add("span-is-hidden");
            newsfeed_div.appendChild(is_hidden_div);
            is_hidden_div.classList.add("div-is-hidden");

            list_newsfeed.appendChild(newsfeed_div);
            newsfeed_div.classList.add("div-newsfeed");
            newsfeed_div.setAttribute("idnf", newsfeed.id);

            newsfeed_div.addEventListener("click", function () {
                const input_title_newsfeed = document.getElementById("input-title");
                const stt_hidden_select = document.getElementById("stt-hidden");
                const delete_btn = document.getElementById("delete-btn");
                delete_btn.disabled = false;

                input_title_newsfeed.value = title_span.textContent;
                if (is_hidden_span.textContent == "Hiển thị") {
                    stt_hidden_select.value = "True";
                }
                else {
                    stt_hidden_select.value = "False";
                }
                input_title_newsfeed.setAttribute("idnf", newsfeed.id);
            });
        });
    }

    //gui file pdf toi views
    function upload_pdf_to_view(formData) {
        return new Promise(function (resolve, reject) {
            const csrfToken = getCSRFToken();
            $.ajax({
                url: 'save-newsfeed/',
                method: 'POST',
                dataType: 'json',
                data: formData,
                processData: false,
                contentType: false,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function (data) {
                    resolve(data);
                },
                error: function (data) {
                    alert("Có lỗi trong quá trình xử lý");
                },
            });
        });
    }

    //token
    function getCSRFToken() {
        const cookies = document.cookie.split('; ');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].split('=');
            if (cookie[0] === ' csrftoken') { return cookie[1]; }
        } return null;
    }

    //delete_newsfeed
    function delete_newsfeed() {
        const id_newsfeed = document.getElementById('input-title').getAttribute('idnf');
        return new Promise(function (resolve, reject) {
            $.ajax({
                url: 'delete-newsfeed/' + id_newsfeed + '/',
                method: 'get',
                dataType: 'json',
                success: function (data) {
                    resolve(data);
                },
                error: function () {
                    alert("Có lỗi trong quá trình xử lý");
                }
            });
        });
    }