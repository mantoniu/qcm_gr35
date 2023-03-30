function student_join(){
    socket.emit('studentjoin',liveqcmid);
}

window.onload = student_join;

function verify_input(){
    if(decimal){
        if($("#decimal-response").val()){
            return true;
        }
        return false;        
    }
    else if(open_question){
        if($("#open_response").val()){
            return true;
        }
        return false;       
    }
    else{
        for(let i=0; i<possibles_responses_number; i++){
            if($('#switch'+i).is(":checked")){
                return true;
            }
        }
        return false;
    }
}


function send_response(){
        if(verify_input()){
            response_list = []
            if(decimal){
                response_list.push($('decimal-response').val());
            }
            else if(open_question){
                response_list.push($("#open_response").val());
            }
            else{
                for(let i=0; i<possibles_responses_number; i++){
                    $('#switch'+i).attr("onclick","return false;");
                    if($('#switch'+i).is(":checked")){
                        response_list.push(i)
                    }
                }
            }
            socket.emit("newresponse",response_list,liveqcmid);
        }
        else{
            alert("Veuillez remplir les champs de réponses");
        }
}

socket.on('response_success',(success)=>{
    if(success) alert('Réponse envoyée avec succès !');
    else alert('Vous avez déjà répondu au questionnaire ! ');
});

socket.on('stop_question',()=>{
    $('#valider').attr("onclick","alert('Vous ne pouvez pas répondre pour le moment');");
    for(let i=0; i<possibles_responses_number; i++){
        $('#switch'+i).attr("onclick","return false;");
    }
});

socket.on('unstop_question',()=>{
    $('#valider').attr("onclick","send_response()");
    for(let i=0; i<possibles_responses_number; i++){
        $('#switch'+i).attr("onclick","");
    }
})

socket.on('nextquestion',()=>{
    window.location.reload();
});

socket.on('stop',()=>{
    window.location.replace('/student');
})

socket.on('correction',(data)=>{
    $('#valider').attr("onclick","alert('Vous ne pouvez pas répondre pendant la correction');");
    if(data.decimal){
        $("#decimal-response").css('display','none');
        $("#decimalresponse_correction")
        .html(data.valids_responses[0])
        .css('display',"flex");
    }
    else{
        for(let i=0; i<possibles_responses_number; i++){
            $('#switch'+i).attr("onclick","return false;");
            if(data.valids_responses.includes(i)){
                $('#switch'+i).prop('checked',true);
            }
            else{
                $('#switch'+i).prop('checked',false);
            }
        }
    }
});