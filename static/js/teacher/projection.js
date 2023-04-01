var fill = d3.scaleOrdinal()
.range(d3.schemeCategory20)

/* Démarrer la projection */
function projection(id){
    $('#project').html("Stopper la projection");
    $('#project').attr('onclick','stop_projection("'+statement_id+'")');
    $('#stop').css("display","flex");
    socket.emit('project',id);
}

/* Réception de l'id */
socket.on('liveqcmid',(id)=>{
    liveqcm_id = id;
    $('#liveqcm_id').text("ID du questionnaire : "+id);
});

/* Réception d'une réponse d'un étudiant */
socket.on('response',(data)=>{
    count_list = data.responses_count
    for(let i=0;i<count_list.length;i++){
        $('#progress'+i).val(count_list[i]);
    }
    $('#response_count').html("Réponses : "+data.count);
    $('#response_count').css('display','flex');
});

/* Mettre en pause la projection */
function stop(){
    socket.emit('stop_question',liveqcm_id);
    $('#stop').html("Activer réponses");
    $('#stop').attr('onclick','unstop("'+liveqcm_id+'")');
}

/* Remtettre la projection en marche */
function unstop(){
    socket.emit('unstop_question',liveqcm_id)
    $('#stop').html("Désactiver réponses");
    $('#stop').attr('onclick','stop("'+liveqcm_id+'")');
}

/* Affichage de la correction */
function correction(){
    if(!decimal){
        if($('input#valid').is(':checked')) $('input#valid').prop('checked',false);
        else $('input#valid').prop('checked',true);
    }
    else{
        if($('#decimalresponse').is(':hidden')) $('#decimalresponse').css('display','flex');
        else $('#decimalresponse').css('display','none');
    }
    socket.emit('correction',liveqcm_id);
}

/* Actualisation des compteurs */
socket.on('count',(count)=>{
    if(count!=0){
        $('#student_count').text("Nombre d'étudiants : "+count);
        $('#student_count').css('display','flex');
        $('.progress_bar').attr('max',count);
        $('.progress_bar').css("display","flex");
    }
});

/* Arreter la projection */
function stop_projection(){
    $("#cloud_word").html("");
    $('#project').html("Projeter la question");
    $('#project').attr('onclick','projection("'+statement_id+'")');
    $('#liveqcm_id').text("");
    $('#stop').css('display','none');
    $('#stop').html("Désactiver réponses");
    $('#stop').attr('onclick','stop("'+statement_id+'")');
    $('#student_count').css('display','none');
    $('#response_count').css('display','none');
    $('.progress_bar').css("display","none");
    $('.progress_bar').val(0);
    socket.emit('stop');
}


data = []

/* Actualisation du nuage de mot */
socket.on('word_cloud',(word_dict)=>{
    console.log("Reception dictionnaire");
    console.log(word_dict);
    data = [];
    maxsize = 2500;
    total_value = 0;
    for(elem in word_dict){
        total_value += word_dict[elem];
    }
    for(elem in word_dict){
        data.push({text:elem,value:(word_dict[elem]/total_value)*maxsize})
    }
    console.log(data);
    $("#cloud_word").html("");
    var layout = d3.layout.cloud()
        .size([350, 250])
        .words(data)
        .on("end", draw);
    layout.start();
});



function draw(words) {
    console.log(data)
    d3.select("#cloud_word")
        .append("g")
        .attr("transform", "translate(" + 350 / 2 + "," + 250 / 2 + ")")
        .selectAll("text")
        .data(words)
        .enter()
        .append("text")
        .text((d) => d.text)
        .style("font-size", (d) => d.size + "px")
        .style("font-family", (d) => d.font)
        .style("fill", (d, i) => fill(i))
        .attr("text-anchor", "middle")
        .attr("transform", (d) => "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")");
}