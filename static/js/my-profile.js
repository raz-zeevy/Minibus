togleEditOff(true);
loadRows(false);
$('#control-changes').hide();
$('.fa-plus-circle').hide();
var imageInput = document.getElementById('image-input');

$(document).on('click', function(e) {
    if (e.target.id === 'options') {
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
    loadRows(true);
    togleEditOff(false);
    $('#control-changes').show()
    $('.fa-plus-circle').show();
});

$('#replace-image').click(function(e){
    console.log('clicked');
    imageInput.disabled = false;
    imageInput.click();
})

document.getElementById('image-input').addEventListener('change', function(e){
    if (imageInput.files.length > 1) {
        Notiflix.Notify.Failure('יש לבחור תמונה אחת בלבד');
        imageInput.files = null;
        $('#image-form').append(imageInput);
    } else{
        image = imageInput.files[0];
        if (['image/jpeg','image/jpg','image/png','image/gip'].includes(image.type)) {
            if (image.size >= 10000000){
                Notiflix.Notify.Failure('התמונה שבחרת גדולה מדי, נא לבחור תמונות שגודלן לא עולה על 10MB');
                imageInput.files = null;
            } else{
                console.log("Input: ",imageInput.files);
                document.getElementById("image-form").submit();
                console.log("Form: ",$("#image-form").serializeArray());
            }
        }else{
            Notiflix.Notify.Failure('התמונה שבחרת לא בפורמט נתמך');
            imageInput.value = null;
        }
    }
})

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
            document.getElementById("delete-form").submit();
            Notiflix.Loading.Dots();
})});

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
