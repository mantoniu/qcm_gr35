var modal = document.getElementById("csv-modal");
var btn = document.getElementById("add-student");
var span = document.getElementsByClassName("close")[1];
var span2 = document.getElementsByClassName("close")[0];

btn.onclick = function() {
  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}

span2.onclick = function() {
  $('#tags-modal').css('display','none');
  $('#tag-list').html("");
}


window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function exam_generator(){
  var selectedValues = $('#select-tags').val();
  for(let i=0;i<selectedValues.length;i++){
    $("#tag-list").append("<li>"+selectedValues[i]+" : <input type='number' name='"+selectedValues[i]+"'></li>");
  }
  $('#tags-modal').css('display','block');
}

function checkvalues(){
  let error=0;
  $("#tag-form :input").map(function(){
      if(!$(this).val()) {
        error ++;
      }
  });
  if(error!=0){
    alert('Veuillez remplir tous les champs');
    return false;
  }
  return true;
}