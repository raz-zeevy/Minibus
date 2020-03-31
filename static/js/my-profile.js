togleEditOff(true);
$('#control-changes').hide();
$('.fa-plus-circle').hide();

$(document).on('click', function(e) {
    console.log(e.target.id);
    if (e.target.id === 'options') {
        console.log('opened options');
        $('#more-options').show();
    } else {
        $('#more-options').hide();
    }
    if (e.target.id === 'save-changes' || e.target.id === 'save-changes-logo'){
        console.log('save changes');
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
        console.log('cancle changes');
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

function togleEditOff(disableAll){
    console.log(`toggled editOFF ${disableAll}`)
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
    console.log('ok im hiding');
    $('#more-options').hide();
}
