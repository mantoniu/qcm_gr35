$(document).ready(function(){
    $("#join").submit(function(){
        $.ajax({
            data : { id : $("#id").val() },
            type : 'POST', 
            url : '/student/join', 
            success: function (data) { 
                if(!data){
                    alert("Aucun questionnaire n'a été trouvé !");
                } 
            },
            error: function (e) { console.log('Erreur') }
          }); 
    });
});