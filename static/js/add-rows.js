$(document).on('click', function(e) {
    if (e.target.id === 'add-position'){
      console.log("clicked on add position")
        $('#positions').append(`<div class="row">
        <div class="col-5">
            <input type="text" class="form-control" placeholder="ארגון" name="inst_job">
        </div>
        <div class="col-5">
            <input type="text" class="form-control" placeholder="תפקיד" name="job">
        </div>
        <div id="add-position" class="col-1 text-center">
            <span id="add-position" style="color:0e606d;" class="fas fa-plus-circle"></span>
        </div>
    </div>`)
    }
    if (e.target.id === 'add-degree'){
      console.log("clicked on add degree")
        $('#education').append(`<div class="row">
        <div class="col-5">
            <input type="text" class="form-control" placeholder="מוסד" name="inst_education">
        </div>
        <div class="col-6">
            <input type="text" class="form-control" placeholder="תואר,תחום,תעודה" name="education">
        </div>
        <div id="add-degree" class="col-1 text-center">
            <span id="add-degree" style="color:0e606d;" class="fas fa-plus-circle"></span>
        </div>
    </div>`)
    }
    if (e.target.id === 'add-army'){
      console.log("clicked on add degree")
        $('#army').append(`<div class="row">
        <div class="col-5">
            <input type="text" class="form-control" placeholder="יחידה" name="inst_army">
        </div>
        <div class="col-6">
            <input type="text" class="form-control" placeholder="תפקיד" name="army">
        </div>
        <div id="add-army" class="col-1 text-center">
            <span id="add-army" style="color:0e606d;" class="fas fa-plus-circle"></span>
        </div>
    </div>`)
    }    
  });