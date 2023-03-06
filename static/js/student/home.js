$(document).ready(function(){
    $("#join").submit(function(){
        $.ajax({
            data : { id : $("#id").val() },
            type : 'POST', 
            url : '/student/join', 
            success: function (data) { 

            },
            error: function (e) { console.log('Erreur') }
          }); 
        if($('#id').val()=="88888888"){
            alert("fueqzrngirng");
        }
    });
});