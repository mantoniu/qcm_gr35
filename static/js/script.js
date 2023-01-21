var count = 1;

$(function() {
    $(".chzn-select").chosen();
});

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

$(document).ready(function(){
    $("#new-statement").submit(function(){
        if($('#statement_name').val()==""){
            alert('Vous devez saisir un nom !');
            return false;
        }
		if ($('input:checkbox').filter(':checked').length < 1){
            alert("Il faut cocher au moins une bonne réponse !");
		    return false;
		}
        if($('input:checkbox').filter(':checked').length == count+1){
            alert("Les réponses ne peuvent pas être toutes justes !");
            return false;
        }
        let oneEmpty = false;
        $('textarea').each(function() {
            if($(this).val().trim() == '')
                oneEmpty = true;
        });
        if(oneEmpty){
            alert('Il faut remplir tous les champs !');
            return false;
        }
        return true;
        });
});


function new_card(){
    document.getElementById('button-add-card').style.display = "none";
    document.getElementById('new-statement').style.display = "flex";
}

function delete_answer(object){
    $(object).parent().remove();
}



function add_answer(){
    count ++;
    html = ' \
    <div class="response"> \
        <div class="switch"> \
            <label id="switch'+count+'" class="switch"> \
                <input type="checkbox" name="switch'+count+'" id="switch'+count+'"> \
                <span class="slider round"></span> \
            </label>  \
        </div> \
        <textarea name="statement'+count+'" type="text" placeholder="Ecrire une réponse..." class="textarea-response"></textarea> \
        <button type="button" onclick="delete_answer(this)" class="trash-button"><i class="fas fa-trash"></i></button>  \
    </div> ';
    $('#count').val(count);
    $("#list-response").append(html);
}

function renderMermaid(){
    mermaid.init(undefined,document.querySelectorAll(".mermaid"));
}

function renderMaths(){
    renderMathInElement(document.body, {
          delimiters: [
              {left: '$$', right: '$$', display: false},
              {left: '$', right: '$', display: false},
          ],
          throwOnError : true
    });
}


function preview(){
    if(document.getElementById('enonce').style.display != "none"){
        if($("#enonce").val().trim() != ''){
            document.getElementById('enonce').style.display = "none";
            $.ajax({
                data : { text : $('#enonce').val() },
                type : 'POST', 
                url : '/preview', 
                success: function (data) { 
                    html = "<div id='translation'>"+data+"</div>";
                    console.log(html);
                    $("#header").append(html);
                    renderMermaid();
                    renderMaths();
                },
                error: function (e) { console.log('Erreur') }
            });
        }
        else alert("Enonce vide !");
    }
    else{
        document.getElementById('enonce').style.display = "flex";
        $('#translation').remove();
    }
}