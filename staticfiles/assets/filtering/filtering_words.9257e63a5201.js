window.addEventListener("DOMContentLoaded", function (e) {
    searchWordFilter()
})

function searchWordFilter(wordFilter) {

    let rows = document.querySelectorAll('.data-row');
    if (!wordFilter) {
        let wordInput = document.querySelector(`.search-input`);
        wordFilter = wordInput.value.toUpperCase();
    }

    for (let i = 0; i < rows.length; i++) {
        let divs = [...rows[i].children];
        let names = divs.map(function (name) {
            return name.textContent
        })

        if (names.some(function (item) {
            return item.toUpperCase().indexOf(wordFilter) > -1;
        })) {
            rows[i].style.display = "";
        } else {
            rows[i].style.display = "none";
        }
    }
}





const headers = [...document.querySelectorAll(".z")]

headers.forEach(function (header) {
    header.firstChild.addEventListener("click", updateUrl);
});

function updateUrl(event) {
    event.preventDefault()

    let wordFilter = document.querySelector(`.search-input`).value.toUpperCase();

    let url = new URL(this.getAttribute('href'), document.baseURI)

    let search_params = url.searchParams
    search_params.set('wordFilter', wordFilter)
    url.search = search_params.toString()
    let new_url = url.toString()

    event.target.setAttribute("href", new_url)

    event.target.removeEventListener("click", updateUrl);
    event.target.click()
}
