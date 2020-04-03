loadRows(false);
console.log('now im disabling all and removing the cirecles');
$('.fa-plus-circle').remove();
var text_inputs = document.querySelectorAll("input");
for (var i = 0; i < text_inputs.length; ++i) {
    text_inputs[i].disabled = true;
}