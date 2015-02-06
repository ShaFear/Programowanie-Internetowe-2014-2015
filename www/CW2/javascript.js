window.addEventListener('load', main, false);

var nameError = document.createElement('nameError');
document.getElementById("nameDiv").appendChild(nameError);

var surnameError = document.createElement('surnameError');
document.getElementById("surnameDiv").appendChild(surnameError);

var pass1Error = document.createElement('pass1Error');
document.getElementById("pass1Div").appendChild(pass1Error);

var pass2Error = document.createElement('pass2Error');
document.getElementById("pass2Div").appendChild(pass2Error);

var dateError = document.createElement('dateError');
document.getElementById("dateDiv").appendChild(dateError);

var loginError = document.createElement('loginError');
document.getElementById("loginDiv").appendChild(loginError);

var peselError = document.createElement('peselError');
document.getElementById("peselDiv").appendChild(peselError);

var sexError = document.createElement('sexError');
document.getElementById("sexDiv").appendChild(sexError);

var avatarError = document.createElement('avatarError');
document.getElementById("avatarDiv").appendChild(avatarError);

var submitError = document.createElement('submitError');
document.getElementById("submitDiv").appendChild(submitError);

function main() {

    var nameElement = document.getElementById("name");
    nameElement.addEventListener("input", checkName);

    var submitElement = document.getElementById("submit");
    submitElement.addEventListener("click", checkSubmit);

    document.addEventListener("input", function f() {
        submitElement.disabled = false
    });

    function checkName() {
        if (!nameElement.value) {
            nameError.innerHTML = "<p> To pole nie może pozostać puste! </p>";
            return false;
        } else {

            if (/[^a-zA-Z]/.test(nameElement.value)) {
                nameError.innerHTML = "<p> Imię powinno składać się z samych liter! (bez polskich znaków) </p>";
                return false;
            }
            else {
                nameError.innerHTML = null;
                return true;
            }
        }
    }

    var surnameElement = document.getElementById("surname");
    surnameElement.addEventListener("input", checkSurname);

    function checkSurname() {
        if (!surnameElement.value) {
            surnameError.innerHTML = "<p> To pole nie może pozostać puste! </p>";
            return false;
        } else {
            if (/[^a-zA-Z]/.test(surnameElement.value)) {
                surnameError.innerHTML = "<p> Nazwisko powinno składać się z samych liter! (bez polskich znaków) </p>";
                return false;
            }
            else {
                surnameError.innerHTML = null;
            }
        }
        return true;
    }

    var pass1Element = document.getElementById("pass1");
    pass1Element.addEventListener("input", checkPass1);

    function checkPass1() {

        if ((/^([a-zA-Z0-9_-]){8,16}$/.test(pass1Element.value) == false) || (pass1Element.value.search(/[a-zA-Z]/) == -1) || (pass1Element.value.search(/\d/) == -1)) {
            pass1Error.innerHTML = "<p> Hasło powinno skłądać się conajmniej z 8 znaków i nie więcej niż z 16, jednocześnie posiadając co najmniej jedną literę i jedną cyfrę! </p>";
            return false;
        }
        else {
            pass1Error.innerHTML = null;
            return true;
        }
    }

    var pass2Element = document.getElementById("pass2");
    pass2Element.addEventListener("input", checkPass2);

    function checkPass2() {
        if (!pass2Element.value) {
            pass2Error.innerHTML = "<p> To pole nie może pozostać puste! </p>";
            return false;
        } else {
            if (pass2Element.value != pass1Element.value) {
                pass2Error.innerHTML = "<p> Hasła nie są takie same! </p>";
                return false;
            }
            else {
                pass2Error.innerHTML = null;
            }
        }
        return true;
    }

    var dateElement = document.getElementById("date");
    dateElement.addEventListener("input", checkDate);

    function checkDate() {
        if (!dateElement.value) {
            dateError.innerHTML = "<p> To pole nie może pozostać puste! </p>";
            return false;
        } else {
            var isDateValid = true;
            var today = new Date();
            var Bdate = new Date(dateElement.value);

            if (Bdate.getFullYear() > today.getFullYear()) isDateValid = false;
            else if (Bdate.getFullYear() == today.getFullYear()) {
                if (Bdate.getMonth() > today.getMonth()) isDateValid = false;
                else if ((Bdate.getMonth() == today.getMonth()) && (Bdate.getDate() > today.getDate())) isDateValid = false;
            }

            if (Bdate.getFullYear() < 1900) isDateValid = false;
            else if ((Bdate.getFullYear() == 1900) && (Bdate.getMonth() == 0) && (Bdate.getDate() == 1)) isDateValid = false;


            if (!isDateValid) {
                dateError.innerHTML = "<p> Data urodzenia musi być większa od 1900-01-01 i nie może być większa niż data dnia dzisiejszego!</p>";
                return false;
            }
            else {
                dateError.innerHTML = null;
            }
        }
        return true;
    }

    var peselElement = document.getElementById("pesel");
    var boyElement = document.getElementById("boy");
    var girlElement = document.getElementById("girl");
    peselElement.addEventListener("input", checkPesel);
    boyElement.addEventListener("click", checkSexElements);
    girlElement.addEventListener("click", checkSexElements);
    var sex = peselElement.value[10];

    function checkPesel() {
        if ((/^([0-9]){11,11}$/.test(peselElement.value)) == false) {
            peselError.innerHTML = "<p> PESEL powinien składać się z 11 cyfr! </p>";
            return false;
        }
        else {
            var Bdate = new Date(dateElement.value);
            var y = (peselElement.value[0].toString() + peselElement.value[1].toString());
            var m = (peselElement.value[2].toString() + peselElement.value[3].toString()) - 1;
            var d = (peselElement.value[4].toString() + peselElement.value[5].toString());
            var yB = Bdate.getFullYear().toString()[2] + Bdate.getFullYear().toString()[3];
            var mB = Bdate.getMonth();
            var dB = Bdate.getDate();
            sex = peselElement.value[10];

            if (y != yB || m != mB || d != dB) {
                peselError.innerHTML = "<p> PESEL nie zgadza się z datą urodzenia! </p>";
                return false;
            }
            else {
                peselError.innerHTML = null;
                if (sex % 2 == 0) {
                    boyElement.checked = true;
                    girlElement.checked = false;
                }
                else {
                    boyElement.checked = false;
                    girlElement.checked = true;
                }
            }
        }
        return true;
    }

    function checkSexElements() {
        if (checkPesel() == false) {
            boyElement.checked = false;
            girlElement.checked = false;
            return false;
        }
        else {
            if (sex % 2 == 0) {
                boyElement.checked = true;
                girlElement.checked = false;
            }
            else {
                boyElement.checked = false;
                girlElement.checked = true;
            }
        }
        return true;
    }

    var avatarElement = document.getElementById("avatar");
    avatarElement.addEventListener("change", checkAvatar);

    function checkAvatar() {
        if (!avatarElement.value) {
            avatarError.innerHTML = "<p> Nie przesłano żadnego avatara! </p>";
            return false;
        } else {
            avatarError.innerHTML = null;
        }
        submitElement.disabled = false;
        return true;
    }

    var loginElement = document.getElementById("login");
    loginElement.addEventListener("input", checkLogin);

    var tmpLogin;

    function checkLogin() {
        if (loginElement.value == tmpLogin) return false;
        if (!loginElement.value) {
            loginError.innerHTML = "<p> To pole nie może pozostać puste! </p>";
            return false;
        } else {
            if (/^([a-zA-Z0-9_-]){4,16}$/.test(loginElement.value) == false) {
                loginError.innerHTML = "<p> Login powinien mieć od 4 do 16 znaków, i nie posiadać znaków specjalnych ani polskich liter! </p>";
                return false;
            }
            else {
                var isAble = true;
                var request = new XMLHttpRequest();
                request.onreadystatechange = function () {
                    if (request.readyState == 4) {
                        if (request.readyState == 200) {
                        }
                        var responseText = JSON.parse(request.responseText);
                        if (responseText[loginElement.value] == true) {
                            loginError.innerHTML = "<p> Ten login jest już zajęty!";
                            tmpLogin = loginElement.value;
                            isAble = false;
                        }
                    }
                }
                request.open('GET', 'http://len.iem.pw.edu.pl/staff/~chaberb/apps/register/check/' + loginElement.value, true);
                request.send(null);

                if (isAble)
                    loginError.innerHTML = null;
            }
        }

        return true;
    }

    function checkSubmit() {
        var isProblem = false;
        if (!checkName()) isProblem = true;
        if (!checkSurname()) isProblem = true;
        if (!checkPass1()) isProblem = true;
        if (!checkPass2()) isProblem = true;
        if (!checkDate()) isProblem = true;
        if (!checkLogin()) isProblem = true;
        if (!checkPesel()) isProblem = true;
        if (!checkAvatar()) isProblem = true;
        if (!checkSexElements()) isProblem = true;
        if (isProblem) {
            alert("W formularzu są błedy! - nie można wysłać");
            submitElement.disabled = true;
        }
        else {
            submitElement.disabled = false;
        }
    }

}

