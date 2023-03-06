$(function() {
    $(".chzn-select").chosen(
        {no_results_text:"Pas d'étiquette trouvée au nom de "}
    );
});


var modal = document.getElementById("myModal");

var btn = document.getElementById("button-create-qcm");

var span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
    if($('input:checkbox').filter(':checked').length == 1){
        modal.style.display = "block";
    }
    else alert("Vous devez selectionner des énoncés !")
}

span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

$(document).ready(function(){
    $("#newqcm").submit(function(){
        if($('#qcm_title').val()==""){
            alert("Vous devez saisir un nom pour le questionnaire !");
            return false;
        }
        if ($('input:checkbox').filter(':checked').length < 1){
            alert("Il faut cocher au moins un énoncé !");
		    return false;
		}
        return true
    });
    if($("#content ul li").length >= 1){
        document.getElementById("button-create-qcm").style.display = "flex";
        document.getElementById("qcm").style.display = "flex";
    }
    else{
        document.getElementById("button-create-qcm").style.display = "none";
        document.getElementById("qcm").style.display = "none";
    }
});