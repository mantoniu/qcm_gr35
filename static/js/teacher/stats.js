/* Envoie de la demande de données à la sélection */
$('#liveqcm_select').on('change',function(){
    var option = $(this).find("option:selected");
    var option_value = option.val();
    if(option_value!="option"){
        socket.emit('stats',option_value);
    }
});

/* Envoie de la demande de données à la sélection */
$('#student_select').on('change',function(){
    var option = $(this).find("option:selected");
    var option_value = option.val();
    if(option_value!="option"){
        socket.emit('student_stats',option_value);
    }
});

/* Réception des stats et affichage du graphique */
socket.on('stats',(data)=>{
    const xValues = data.x_values;
    const yValues = data.y_values;

    new Chart("liveqcm_stats", {
    type: "line",
    data: {
        labels: xValues,
        datasets: [{
        backgroundColor:"rgba(0,0,255,1.0)",
        borderColor: "rgba(0,0,255,0.1)",
        data: yValues
        }]
    },
    options: {
        scales :{
            yAxes:[{
                ticks:{
                    stepSize:1.0
                }
            }]
        },
        legend:{display:false},
        title:{
            display:true,
            text:"Nombre de réponses par question",
            fontSize:16
        }
    }
    });
    $("liveqcm_stats").css("display","flex");
});

socket.on('student_stats',(msg)=>{
    console.log(msg);
});
