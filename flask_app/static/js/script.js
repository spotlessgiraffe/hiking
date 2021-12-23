let likes_counter = document.querySelector("#likes_count");
let dislikes_counter = document.querySelector("#dislikes_count");

let num_of_likes = 0;
function display_likes() {
    num_of_likes++;
    likes_counter.innerText = "(" + num_of_likes + ")";
}

let num_of_dislikes = 0;
function display_dislikes() {
    num_of_dislikes++;
    dislikes_counter.innerText = "(" + num_of_dislikes + ")";
}