
        function checkPassword() {
            if (document.change_password.new_password.value != document.change_password.confirm_password.value) {
                alert("New Password and Confirm Password fields do not match each other.");
                document.change_password.confirm_password.focus();
                return false;
            }
            return true;
        }

        var alertMessage = document.body.dataset.alertMessage;
        if (alertMessage) {
            alert(alertMessage);
            document.location = "/logout";
        }

        var currPassWrongMessage = document.body.dataset.currPassWrongMessage;
        if (currPassWrongMessage) {
            alert(currPassWrongMessage);
            document.location = "/change_password";
        }