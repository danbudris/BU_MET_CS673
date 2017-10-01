// function to validate password, matches 6 to 20 characters which contain at least one numeric digit, one uppercase, one lowercase letter, a inspiring message and a spell

$(document).ready(function () {

    // listens to the user input at password text box, handles event when key up.
    $("#id_password1").keyup(function () {
        validatePassword();
    });

    //listens to the the password confirmation input
    $("#id_password2").keyup(function () {
        matchPasswords();
    });

    // removes alerts classes if either of the text box is empty
    $("input").blur(function () {
        cleanUp();
    });


    // matches both password
    function matchPasswords() {
        var pwd1 = $("#id_password1").val();
        var pwd2 = $("#id_password2").val();
        console.log(pwd1 + " " + pwd2);

        var notMatched = '<p id = "not-matched" style="font-size:1em" class = "bg-danger"> Passwords do not match </p>';

        if (validatePassword() && pwd1 == pwd2) {
            $("#not-matched").remove();
            $("#id_password2").removeClass("alert-danger");
            $("#id_password2").addClass('alert-success');
            $("#activate").prop("disabled", false);

        } else {
            if (!$("#not-matched").length) $(notMatched).insertAfter("#id_password2");
            $("#id_password2").removeClass("alert-success");
            $("#id_password2").addClass("alert-danger");
            $("#activate").prop("disabled", true);

        }
    }

    function cleanUp() {
        var pwd1 = $("#id_password1").val();
        var pwd2 = $("#id_password2").val();

        if (pwd1 == "") $("#id_password1").removeClass("alert-danger");
        if (pwd2 == "") $("#id_password2").removeClass("alert-danger");

        if (pwd1 == "" && pwd2 == "") {
            $("#not-matched").remove();
            $("#info-text").remove();
            $("#id_password1").removeClass("alert-danger");
            $("#id_password2").removeClass("alert-danger");
        }
    }

    function validatePassword() {
        // regex for password validation
        var passwRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/;
        var pwd1 = $("#id_password1").val();

        var invalidPwd = '<p id = "info-text" class = "bg-danger" style = "font-size: 1em"> Please enter a password of 6 to 20 characters which contain at least one numeric digit, one uppercase, one lowercase letter</p>';

        if (pwd1.match(passwRegex)) {
            $("#info-text").remove();
            $("#id_password1").removeClass("alert-danger");
            $("#id_password1").addClass('alert-success');
            return true;

        } else {
            if (!$("#info-text").length) $(invalidPwd).insertAfter("#id_password1");
            $("#id_password1").removeClass("alert-success");
            $("#id_password1").addClass("alert-danger");
            return false;

        }

    }


});
