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
    document.getElementById('button-add-card').style.display = "none";
    html = ' \
    <form action="/newcard" class="form-card"> \
        <div class="card"> \
            <div class="header-card"> \
                <textarea type="text" spellcheck="false" placeholder="Ecrire l énoncé..." id="enonce"></textarea> \
            </div> \
            <div class="body-card"> \
                <div class="content" id="content-response"> \
                    <div class="list-response"> \
                        <div class="response" id="response3"> \
                            <div class="switch"> \
                                <input type="checkbox" id="switch3"> \
                                <label for="switch3"></label> \
                            </div> \
                            <textarea type="text" placeholder="Ecrire une réponse..." class="textarea-response"></textarea> \
                            <button onclick="deleteAnswer()" class="trash-button"><i class="fas fa-trash"></i></button> \
                        </div> \
                        <div class="response" id="response3"> \
                            <div class="switch"> \
                                <input type="checkbox" id="switch3"> \
                                <label for="switch3"></label> \
                            </div> \
                            <textarea type="text" placeholder="Ecrire une réponse..." class="textarea-response"></textarea> \
                            <button class="trash-button"><i class="fas fa-trash"></i></button> \
                        </div> \
                </div> \
            </div> \
                <div class="card-navbar"> \
                    <button class="animation" type="submit" id="apercu">Aperçu</button> \
                    <div class="circle animation"><i class="fas fa-plus"></i></div> \
                    <button class="animation" type="submit" id="ajouter">Valider</button> \
                </div> \
            </div> \
        </div> \
    </form>';
    $("body").append(html);
}



function add_answer(){
    html = ' \
    <div class="response" id="response3"> \
        <div class="switch"> \
            <input type="checkbox" id="switch3"> \
            <label for="switch3"></label> \
        </div> \
        <textarea type="text" placeholder="Ecrire une réponse..." class="textarea-response"></textarea> \
        <button class="trash-button"><i class="fas fa-trash"></i></button> \
    </div> ';

    $("#content-response").append(html);
}
