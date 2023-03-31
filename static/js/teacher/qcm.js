/* Vérification de la projection du qcm et déplacement sur le bon énoncé si oui  */
function verify_statement(){
    if(projected && statement_index!=statement_number){
        window.location.replace("/qcm/"+qcm_id+"/"+statement_index);
    }
}

/* Passage à la question suivante  */
function nextquestion(){
    statement_num = parseInt(statement_number);
    socket.emit('nextquestion',liveqcm_id,statement_num);
}

/* Déplacement sur l'énoncé suivant */
socket.on('nextquestion',(statement_num)=>{
    window.location.replace("/qcm/"+qcm_id+"/"+statement_num);
});

/* Passage à la question précédente */
function previous(){
    statement_num = parseInt(statement_number)
    statement_num --;
    if(statement_number !=-1){
        window.location.replace("/qcm/"+qcm_id+"/"+statement_num);
    }
}

/* Recharge la page quand stoppé */
socket.on('stop',()=>{
    window.location.reload();
});
