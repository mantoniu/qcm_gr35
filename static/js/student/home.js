$(document).ready(function(){
    $("#join").submit(function(){
        socket.emit('liveqcm_join',$("#id").val())
    });
});



socket.on('liveqcm_join',(data)=>{
    console.log(data);
    if(data.not_found) alert("Aucun questionnaire n'a été trouvé !");
    else{
        console.log("test")
        console.log("/student/question/"+data.qcmid)
        window.location.replace("/student/question/"+data.qcmid);
    }
});