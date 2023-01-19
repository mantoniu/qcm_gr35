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

var count = 3;

function new_card(){
    document.getElementById('button-add-card').style.display = "none";
    html = ' \
    <form method="POST" id="new-question" action="/newstate/" class="form-card"> \
        <div class="card"> \
            <div class="header-card"> \
                <textarea name="enonce" type="text" spellcheck="false" placeholder="Ecrire l énoncé..." id="enonce"></textarea> \
            </div> \
            <div class="body-card"> \
                <div class="content" id="content-response"> \
                    <input id="count" type="hidden" name="count" value="1"> \
                    <div class="list-response" id="list-response"> \
                        <div class="response"> \
                            <div class="switch"> \
                                <input type="checkbox" name="switch0" id="switch0"> \
                                <label for="switch0"></label> \
                            </div> \
                            <textarea name="question0" type="text" placeholder="Ecrire une réponse..." class="textarea-response"></textarea> \
                            <button type="button" onclick="delete_answer(this)" class="trash-button"><i class="fas fa-trash"></i></button> \
                        </div> \
                        <div class="response"> \
                            <div class="switch"> \
                                <input type="checkbox" name="switch1" id="switch1"> \
                                <label for="switch1"></label> \
                            </div> \
                            <textarea name="question1" type="text" placeholder="Ecrire une réponse..." class="textarea-response"></textarea> \
                            <button type="button" onclick="delete_answer(this)" class="trash-button"><i class="fas fa-trash"></i></button> \
                        </div> \
                </div> \
            </div> \
                <div class="card-navbar"> \
                    <button class="animation" type="submit" id="apercu">Aperçu</button> \
                    <div onclick="add_answer()" class="circle animation"><i class="fas fa-plus"></i></div> \
                    <button class="animation" type="submit" id="ajouter">Valider</button> \
                </div> \
            </div> \
        </div> \
    </form>';
    $("body").append(html);
}

function delete_answer(object){
    $(object).parent().remove();
}

var count = 1;

function add_answer(){
    count ++;
    html = ' \
    <div class="response"> \
        <div class="switch"> \
            <input type="checkbox" id="switch'+count+'" name="switch'+count+'"> \
            <label for="switch'+count+'"></label> \
        </div> \
        <textarea name="question'+count+'" type="text" placeholder="Ecrire une réponse..." class="textarea-response"></textarea> \
        <button type="button" onclick="delete_answer(this)" class="trash-button"><i class="fas fa-trash"></i></button>  \
    </div> ';
    $('#count').val(count);
    $("#list-response").append(html);
}
