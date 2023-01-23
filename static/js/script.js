var count = 1;

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

function addOption(){
    console.log('test')
    html = "Nom de l'étiquette : <input type='text' name='tag_name'>";
    $('#info').append(html);
    $('#select-tags').append('<option value="foo">Bar</option>');
    $('#select-tags').trigger("chosen:updated");
}

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
    console.log($(object).attr("id"));
    for(let i=$(object).attr("id");i<=count;i++){
        $("#switch"+i).attr("id", "switch"+ (i-1).toString());
        $("#input"+i).attr("name", "switch"+ (i-1).toString());
        $("#input"+i).attr("id", "input"+ (i-1).toString());
        $("#"+i).attr("id",(i-1).toString())
        $("#text"+i).attr("name","statement"+(i-1).toString())
        $("#text"+i).attr("id", "text"+(i-1).toString())
    }
    count --;
    $(object).parent().remove();
}



function add_answer(){
    count ++;
    html = ' \
    <div class="response"> \
        <div class="switch"> \
            <label id="switch'+count+'" class="switch"> \
                <input id="input'+count+'" type="checkbox" name="switch'+count+'"> \
                <span class="slider round"></span> \
            </label>  \
        </div> \
        <textarea id="text'+count+'" name="statement'+count+'" type="text" placeholder="Ecrire une réponse..." class="textarea-response"></textarea> \
        <button id='+count+' type="button" onclick="delete_answer(this)" class="trash-button"><i class="fas fa-trash"></i></button>  \
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
