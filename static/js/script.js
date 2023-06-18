const search = document.getElementById("search");
const submit = document.getElementById("submit");

submit.addEventListener('click', () => {
    console.log("/pokemon/" + search.value.toLowerCase())
    window.location.href = "/pokemon/" + search.value.toLowerCase();
});