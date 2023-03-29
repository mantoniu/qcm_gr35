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
  $('#advanced').prop("checked",false);
}


window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function exam_generator(){
  var selectedValues = $('#select-tags').val();
  if(selectedValues != null){
    for(let i=0;i<selectedValues.length;i++){
      $("#tag-list").append("<li>"+selectedValues[i]+" : <input min='0' type='number' style='width: 50px' name='"+selectedValues[i]+"' required><div id='range' style='display:none;'> - <input min='0' type='number' style='width: 50px' name='a"+selectedValues[i]+"'></div></li>");
    }
    $('#tags-modal').css('display','block');
  }
  else alert('Veuillez sélectionner des étiquettes');
}

function remove_red(e){
  e.classList.remove("red");
}

$("#tag-form").submit(function(e){
  var selectedValues = $('#select-tags').val();
  if($("#advanced").is(":checked")){
      for(let i=0;i<selectedValues.length;i++){
        let elem1 = $("input[name='"+selectedValues[i]+"']");
        let elem2 = $("input[name='a"+selectedValues[i]+"']");
        if(elem1.val()>elem2.val()){       
          elem1.addClass("red")
                .attr("onchange","remove_red(this);");
          ;
          elem2.addClass("red")
                .attr("onchange","remove_red(this);");
          alert("Le première borne ne peut pas être supérieure à la deuxième !");
          return false;
        }
      }
  }
  return true;
});


$('#advanced').change(function(){
  if(this.checked){
    $('div[id="range"]').css('display','inline');
    $('#range :input').prop("required",true);
  }
  else{
    $('div[id="range"]').css('display','none');
    $('#range :input').prop("required",false);
  }
});