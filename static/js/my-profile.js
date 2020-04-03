togleEditOff(true);
$('#control-changes').hide();
$('.fa-plus-circle').hide();

$(document).on('click', function(e) {
    if (e.target.id === 'options') {
        console.log('opened options');
        $('#more-options').show();
    } else {
        $('#more-options').hide();
    }
    if (e.target.id === 'save-changes' || e.target.id === 'save-changes-logo'){
        $('#control-changes').hide();
        inputs = $('input')
        for (var i=0;i<inputs.length;i++){
            if (inputs[i].value == '' || inputs[i].value == ' '){
                inputs[i].id = 'to_delete';
            }
            $('#to_delete').remove();
        }
        document.getElementById("my-profile").submit();

    } else if (e.target.id === 'cancle' || e.target.id === 'cancle-changes-logo'){
        $('#control-changes').hide();
        $('.fa-plus-circle').hide();
        togleEditOff(true);
    } 
});

$('#options-edit').click(function(e){
    togleEditOff(false);
    $('#control-changes').show()
    $('.fa-plus-circle').show();
});

$('#delete-profile').click(function(e){
    if (profile['gender'] == 'male'){
        var content = 'בטוח שאתה רוצה למחוק את הפרופיל?'
    } else{
        var content = 'בטוחה שאת רוצה למחוק את הפרופיל?'
    }
    Notiflix.Confirm.Show('מחיקת פרופיל "מיניבוס"',content,'לא','כן',
                function(){
                    // Yes button callbackaler
                },
                function(){
                // No button callback
                alert('If you say so...');});
});

function togleEditOff(disableAll){
    var text_inputs = document.querySelectorAll("input");
    for (var i = 0; i < text_inputs.length; ++i) {
        text_inputs[i].disabled = disableAll
    }
    var gender = document.querySelector("select");
    gender.disabled = disableAll;
    // gender.value = profile['gender'];
    // var date = document.querySelector("input[type=date]");
    // date.disabled = disableAll;
    // date.value = profile['date_of_birth']
    // var date = document.querySelector("input[type=tel]");
    // date.disabled = disableAll;
    // date.value = profile['phone_number']
}

function optionsClose(){
    $('#more-options').hide();
}
