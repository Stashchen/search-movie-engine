let modal = document.querySelector("#modal");
let modalEdit = document.querySelector("#modal-edit");
let modalOverlay = document.querySelector("#modal-overlay");
let closeButton = document.querySelector("#close-button");
let closeButtonEdit = document.querySelector("#close-button-edit");
let openButton = document.querySelector("#open-button");
let cards = document.getElementsByClassName("movie-card");
let edit_fields = document.querySelectorAll("#edit_form .field input, #edit_form .field select, #edit_form .field textarea");
let submit_edit = document.querySelector("#edit_form input[type=submit]");

console.log(submit_edit);
submit_edit.setAttribute("disabled", "true");

function enable_edit() {
    for (let field of edit_fields) {
        field.removeAttribute("disabled");
    }
    submit_edit.removeAttribute("disabled");
}

for (let field of edit_fields) {
    field.setAttribute("disabled", "true");
}

closeButton.addEventListener("click", function(){
    modal.classList.toggle("closed");
    modalOverlay.classList.toggle("closed");
})

closeButtonEdit.addEventListener("click", function(){
    modalEdit.classList.toggle("closed");
    modalOverlay.classList.toggle("closed");
})

openButton.addEventListener("click", function(){
    modal.classList.toggle("closed");
    modalOverlay.classList.toggle("closed");
})

for (let i = 0; i < cards.length; i++) {
    element = cards[i];
    element.addEventListener("click", function(){
        fetch("http://localhost:8000/api/movies/" + this.children[0].innerHTML)
        .then(response => response.json())
        .then(data => {
            for (let field of edit_fields) {
                if (field.name == "actors" || field.name == "writers") {
                    let array = data[field.name]; // From JSON writers or actors
                    for (let elem of array) {
                        for (let i = 0; i < field.options.length; i++) {
                            if (field.options[i].value == elem.id) {
                                field.options[i].selected = true;
                            }
                        }
                    }
                } else {
                    field.value = data[field.name];
                }
            }
        });
        modalEdit.classList.toggle("closed");
        modalOverlay.classList.toggle("closed");
    })
}


