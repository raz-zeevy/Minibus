var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
    // This function will display the specified tab of the form ...
    var x = document.getElementsByClassName("tab");
    x[n].style.display = "block";
    // ... and fix the Previous/Next buttons:
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
        document.getElementById("nextBtn").innerHTML = "שלח";
        document.getElementById("nextBtn").className = "btn btn-success btn-lg";
    } else {
        document.getElementById("nextBtn").innerHTML = "הבא";
        document.getElementById("nextBtn").className = "btn btn-success";
    }
    // ... and run a function that displays the correct step indicator:
    fixStepIndicator(n)
}

function nextPrev(n) {
    // This function will figure out which tab to display
    var x = document.getElementsByClassName("tab");
    // Exit the function if any field in the current tab is invalid:
    if (n == 1 && !validateForm()) return false;
    // Hide the current tab:
    x[currentTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + n;
    // if you have reached the end of the form... :
    if (currentTab >= x.length) {
        //...the form gets submitted:
        document.getElementById("prevBtn").style.display = "none";
        document.getElementById("nextBtn").style.display = "none";
        document.getElementById("regForm").submit();
        Notiflix.Loading.Dots('נשלח בהצלחה...');
        return false;
    }
    // Otherwise, display the correct tab:
    showTab(currentTab);
}

function validateForm() {
    // This function deals with validation of the form fields
    var x, y, i, valid = true;
    x = document.getElementsByClassName("tab");
    y = x[currentTab].getElementsByClassName("crucial-input");
    // A loop that checks every input field in the current tab:
    for (i = 0; i < y.length; i++) {
        // If a field is empty...
        if (y[i].value == "") {
            // add an "invalid" class to the field:
            y[i].className += " invalid";
            // and set the current valid status to false:
            valid = false;
            var empty = true;
        }
        else{
            if (y[i].classList.contains('invalid')){
                y[i].classList.remove('invalid');
            }
        }
    }
    if (empty) {Notiflix.Notify.Failure("לא מילאת את כל שדות החובה");}
    phoneValue = parsePhone($('#phone-input')[0].value)
    if (!phoneValue[0]){
        if (!$('#phone-input')[0].classList.contains('invalid')){
        // add an "invalid" class to the field:
            $('#phone-input')[0].className += " invalid";
            Notiflix.Notify.Failure(phoneValue[1]);
        }
        // and set the current valid status to false:
        valid = false;
    } else {
        $('#phone-input')[0].value = phoneValue[1];
    }
    // If the valid status is true, mark the step as finished and valid:
    if (valid) {
        document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid; // return the valid status
}

function fixStepIndicator(n) {
    // This function removes the "active" class of all steps...
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    //... and adds the "active" class to the current step:
    x[n].className += " active";
}