var liveqcm_id = "{{ liveqcm_id }}";

/* Vérification de la projection du qcm et déplacement sur le bon énoncé si oui  */
function verify_statement(){
    if("{{ projected|tojson }}"==="true" && "{{ statement_index }}"!= "{{ statement_number }}"){
        window.location.replace("/qcm/"+"{{ qcm.id }}/"+"{{ statement_index }}");
    }
}

/* Passage à la question suivante  */
function nextquestion(){
    statement_number = parseInt("{{statement_number}}");
    socket.emit('nextquestion',liveqcm_id,statement_number);
}

/* Déplacement sur l'énoncé suivant */
socket.on('nextquestion',(statement_number)=>{
    window.location.replace("/qcm/"+"{{ qcm.id }}"+"/"+statement_number);
});

/* Passage à la question précédente */
function previous(){
    statement_number = parseInt("{{statement_number}}")
    statement_number --;
    if(statement_number !=-1){
        window.location.replace("/qcm/"+"{{ qcm.id }}"+"/"+statement_number);
    }
}

/* Recharge la page quand stoppé */
socket.on('stop',()=>{
    window.location.reload();
});
