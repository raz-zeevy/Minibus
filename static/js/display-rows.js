console.log("now im working on the rows");
var tabs = document.querySelectorAll(".tab");
  for (var i=0; i < tabs.length; ++i){
    tab = tabs[i]
    text_inputs = $(tab).find('input')
    var keep_tab = false;
    for (var j=0; j < text_inputs.length; ++j){
      if (profile[text_inputs[j].name] == "" || profile[text_inputs[j].name]== [""]){
        text_inputs[j].style.display='none';
      }
      else{
      text_inputs[j].disabled = true;
      text_inputs[j].value = profile[text_inputs[j].name];
      keep_tab = true;
    }}
    if (!keep_tab){
      tabs[i].style.display = "none";
    }}

var army = profile['army'];
var inst_army = profile['inst_army'];
if (typeof(army) == 'string'){
    army = [army];
    inst_army = [inst_army];
}
for (var i=0; i < army.length; i++){
    $('#army').append(`<div class="row">
    <div class="col-5">
        <input type="text" value="${inst_army[i]}" class="form-control" placeholder="יחידה" name="inst_army">
    </div>
    <div class="col-6">
        <input type="text" value="${army[i]}" class="form-control" placeholder="תפקיד" name="army">
    </div>
    <div id="add-army" class="col-1 text-center">
        <span id="add-army" style="color:0e606d;" class="fas fa-plus-circle"></span>
    </div>
</div>`);   
};

var education = profile['education'];
var inst_education = profile['inst_education'];
if (typeof education == 'string'){
    education = [education];
    inst_education = [inst_education];
}
for (var i=0; i < education.length; i++){
    if (i==0){
        $('#education').append(`<div class="row">
        <div class="col text-right">
            <label for="">השכלה:</label>
        </div>
    </div>`);
    }
    $('#education').append(`<div class="row">
    <div class="col-5">
        <input type="text" value="${inst_education[i]}" class="form-control" placeholder="מוסד" name="inst_education">
    </div>
    <div class="col-6">
        <input type="text" value="${education[i]}" class="form-control" placeholder="תואר" name="education">
    </div>
    <div id="add-degree" class="col-1 text-center">
        <span id="add-degree" style="color:0e606d;" class="fas fa-plus-circle"></span>
    </div>
</div>`);  
};

var job = profile['job'];
var inst_job = profile['inst_job'];
if (typeof job == 'string'){
    job = [job];
    inst_job = [inst_job];
}
for (var i=0; i < job.length; i++){
    if (i==0){
        $('#positions').append(`<div class="row">
        <div class="col text-right">
            <label for="">מקומות עבודה:</label>
        </div>
    </div>`);
    }
    $('#positions').append(`<div class="row">
    <div class="col-5">
        <input type="text" value="${inst_job[i]}" class="form-control" placeholder="ארגון" name="inst_job">
    </div>
    <div class="col-6">
        <input type="text" value="${job[i]}" class="form-control" placeholder="תפקיד" name="job">
    </div>
    <div id="add-position" class="col-1 text-center">
        <span id="add-position" style="color:0e606d;" class="fas fa-plus-circle"></span>
    </div>
</div>`);  
};
