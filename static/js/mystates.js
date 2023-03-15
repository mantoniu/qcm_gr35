$(function() {
    $(".chzn-select").chosen(
        {no_results_text:"Pas d'étiquette trouvée au nom de "}
    );
});




$(document).ready(function(){ 
    $("#newqcm").submit(function(){           
        if ($('input:checkbox').filter(':checked').length < 1){
            alert("Il faut cocher au moins un énoncé !");
		    return false;
		}        

        if($('#qcm_title').val()==""){
            alert("Vous devez saisir un nom pour le questionnaire !");
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