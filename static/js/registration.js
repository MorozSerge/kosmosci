    function checkPasswords(form) {
    let password1 = form.password1.value;
    let password2 = form.password2.value;

    if(String(password1).length >= 8) {
        if (password1 === '')
            alert("Пожалуйста, введите пароль");
        else if (password2 === '')
            alert("Пожалуйста, подтвердите пароль");
        else if (password1 !== password2) {
            alert("\nПароли не совпадают. Пожалуйста, попробуйте еще раз")
            return false;
        }
    } else if (password1 === password2 && password1 === '') {
        return true;
    } else {
        alert("Минимальная длина пароля - 8 символов")
        return false;
    }
}
