var vue;
console.log($(document))
$(document).ready(() => {
    console.log("init..")
    vue = new Vue({
        el: "#login-form", data: {
            identifier: "",
            password: "", loading: false
        }, methods: {
            submit: function () {
                if (!this.identifier || !this.password) {
                    showErrorModal("请输入用户名或密码");
                    return;
                }
                this.loading = true;
                $.post("/api/login", { identifier: this.identifier, password: md5WithSalt(this.password) }).done((ret) => {
                    ret = JSON.parse(ret);
                    console.log(ret);
                    vue.loading = false;
                    if (!ret.code) {
                        showErrorModal(ret.message);
                        return;
                    }
                    window.location.href = "/"
                })
            }
        }
    })
});