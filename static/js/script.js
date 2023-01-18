function inscription(){
    document.getElementById('connection').style.display ="none";
    document.getElementById("s'inscrire").style.display ="none";
    document.getElementById('inscription').style.display ="flex";
    document.getElementById('seconnecter').style.display ="flex";
}; 

function connection(){
    document.getElementById('connection').style.display ="flex";
    document.getElementById("s'inscrire").style.display ="flex";
    document.getElementById('inscription').style.display ="none";
    document.getElementById('seconnecter').style.display ="none";
}; 



function new_card(){
    $.getJSON(document.URL+"newcard",(object)=>{
        id = object.id;
        html = 
        
        "<div class='card' id ='"+id+"'> \
                    <div class='header-card'> \
                        <textarea class='enonce' type='text' spellcheck='false' placeholder='Ecrire l'énoncé...' id='enonce"+id+"'></textarea> \
                    </div> \
                    <div class='body-card'> \
                        <div class='content-response' id='content-response"+id+"'> \
                            <div class='response' id='"+id+"response1'> \
                                <div class='switch'> \
                                    <input type='checkbox' id='"+id+"switch1'> \
                                    <label for='"+id+"switch1'></label> \
                                </div> \
                                <p> de profondeur 2</p> \
                                <i class='fas fa-trash'></i> \
                            </div> \
                            <div class='response' id='"+id+"response1'> \
                                <div class='switch'> \
                                    <input type='checkbox' id='"+id+"switch2'> \
                                    <label for='"+id+"switch2'></label> \
                                </div> \
                                <p> de profondeur 2</p> \
                                <i class='fas fa-trash'></i> \
                            </div> \
                        </div> \
                        <div class='card-navbar'> \
                            <button type='submit' id='"+id+"apercu'>Aperçu</button> \
                            <div onclick='add_answer()' class='circle'><i class='fas fa-plus'></i></div> \
                            <button type='submit' id='"+id+"ajouter'>Valider</button> \
                        </div> \
                    </div> \
        </div>";
        $("body").append(html);
    });
}



function add_answer(){
    $.getJSON(document.URL+"newanswer",(object)=>{
        newcount = object.answer_count + 1;
        html = "<div class='response' id='"+id+newcount+"'><div class='switch'><input type='checkbox' id='switch"+newcount+"'><label for='switch"+newcount+"'></label></div><p>Je suis une réponse</p><i class='fas fa-trash'></i></div>";
        $("#content-response").append(html);
    });
}
