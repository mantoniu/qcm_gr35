document.addEventListener("DOMContentLoaded", init);

function init() {
  var select = document.querySelector("select[name='quiz']");
  var submitBtn = document.querySelector("input[type='submit']");
  var selectedTag = document.getElementById("selected-tag");
  var tags = []; // tableau pour stocker les options sélectionnées

  select.addEventListener("change", function() {
    if (select.value === "other") {
      var newOption = prompt("Entrez le nom du nouveau sujet :");
      if (newOption) {
        var option = new Option(newOption, newOption);
        select.add(option);
        select.value = newOption;
      }
    }
  });

  submitBtn.addEventListener("click", function(e) {
    e.preventDefault();
    if (select.value !== "other") {
      var selectedOption = select.options[select.selectedIndex];
      if (!tags.includes(selectedOption.text)) {
        var tag = document.createElement("span");
        tag.classList.add("tag");
        tag.innerHTML = selectedOption.text;
        selectedTag.appendChild(tag);
        selectedTag.style.display = "block";
        tags.push(selectedOption.text);
      } else {
        alert("Cette option a déjà été sélectionnée.");
      }
    } else {
      alert("Veuillez sélectionner une option valide avant de soumettre.");
    }
  });

  // event pour supprimer le tag en le cliquant
  selectedTag.addEventListener("click", function(e){
      if(e.target.classList.contains("tag")){
          var tag = e.target;
          var tagText = tag.innerHTML;
          tag.remove();
          var index = tags.indexOf(tagText);
          tags.splice(index, 1);
      }
  });
}
