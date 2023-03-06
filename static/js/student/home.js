$(document).ready(function(){
    $("#join").submit(function(){
        $.ajax({
            data : { id : $("#id").val() },
            type : 'POST', 
            url : '/student/join', 
            success: function (data) { 
                if(data.not_found){
                    alert("Aucun questionnaire n'a été trouvé !");
                }
                else{
                    window.location.replace("/student/question/"+$("#id").val());
                }
            },
            error: function (e) { console.log('Erreur') }
          }); 
    });
});