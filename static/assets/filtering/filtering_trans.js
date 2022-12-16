months = {
    "01": "Jan",
    "02": "Feb",
    "03": "Mar",
    "04": "Apr",
    "05": "May",
    "06": "Jun",
    "07": "Jul",
    "08": "Aug",
    "09": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
}



window.addEventListener("DOMContentLoaded", function (e) {
    searchFilter();
})

const slider = document.querySelector('.value-input');
const headers = [...document.querySelectorAll(".z")];
const link = document.querySelector(".custom-scrollbar").querySelector("a");

headers.forEach(function (header) {
    header.firstChild.addEventListener("click", updateUrl);
});

if (slider != null) {
    slider.oninput = function () {
        searchFilter();
    }
}

function searchFilter(wordFilter, valueFilter) {

    let rows = document.querySelectorAll('.data-row');
    let displaySum = document.querySelector(".value-sum");
    let displayTotal = document.querySelector(".value-total");
    let sum = 0;
    let total = 0;
    if (!wordFilter) {
        let wordInput = document.querySelector(`.search-input`);
        wordFilter = wordInput.value.toUpperCase();
    }
    if (!valueFilter) {
        let valueInput = document.querySelector(`.value-input`);
        valueFilter = Number(valueInput.value);
    }

    for (let i = 0; i < rows.length; i++) {
        let divs = [...rows[i].children];
        let names = divs.map(function (name) {
            return name.textContent
        })

        let value = Number(rows[i].children[2].textContent);

        if (names.some(function (item) {
            return item.toUpperCase().indexOf(wordFilter) > -1;
        }) && value * valueFilter >= 0) {
            rows[i].style.display = "";
            sum += value;
            total += 1;
        } else {
            rows[i].style.display = "none";
        }
    }
    displaySum.textContent = sum.toFixed(2);
    displayTotal.textContent = total.toString();
}


function updateUrl(event) {
    event.preventDefault();

    let wordFilter = document.querySelector(`.search-input`).value;
    let valueFilter = document.querySelector(`.value-input`).value;
    let fromDate = document.querySelector(".from-date-input").value;
    let toDate = document.querySelector(".to-date-input").value;

    let url = new URL(this.getAttribute('href'), document.baseURI)

    let search_params = url.searchParams;
    search_params.set('wordFilter', wordFilter);
    search_params.set('valueFilter', valueFilter);
    search_params.set('fromDate', fromDate);
    search_params.set('toDate', toDate);
    url.search = search_params.toString();
    let new_url = url.toString();

    search_params.set('json', "1");
    url.search = search_params.toString();
    let fetchUrl = url.toString();

    event.target.setAttribute("href", new_url);
    fetching(fetchUrl)

    function fetching(url) {
        fetch(url)
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                const ul = document.querySelector(".data-body")
                const scroll = ul.querySelector(".custom-scrollbar")
                const linkToClone = link.cloneNode()
                const scrollToClone = scroll.cloneNode()

                ul.removeChild(scroll)
                ul.appendChild(scrollToClone)

                const transactions = data["transactions"]

                if (transactions.length === 0) {
                    const nothingDiv = document.createElement("div")
                    nothingDiv.setAttribute("class", "col-12 align-center")
                    nothingDiv.textContent = "Nothing to display"
                    scrollToClone.appendChild(nothingDiv)
                } else {
                    for (let i = 0; i < transactions.length; i++) {
                        const rowDiv = document.createElement("div")
                        rowDiv.setAttribute("class", "row p-2 data-row")

                        const counterCol = document.createElement("div")
                        counterCol.setAttribute("class", "col-1")
                        counterCol.textContent = (i + 1).toString()
                        rowDiv.appendChild(counterCol)

                        const dateCol = document.createElement("div")
                        dateCol.setAttribute("class", "col-1")
                        let newDate = transactions[i]["date"].split("-").reverse()
                        newDate[1] = months[newDate[1]]
                        dateCol.textContent = newDate.join(" ")
                        rowDiv.appendChild(dateCol)

                        const valueCol = document.createElement("div")
                        valueCol.setAttribute("class", "col-1 text-right pr-5")
                        valueCol.textContent = transactions[i]["value"].toFixed(2)
                        rowDiv.appendChild(valueCol)

                        const cntpCol = document.createElement("div")
                        cntpCol.setAttribute("class", "col-2")
                        cntpCol.textContent = transactions[i]["counterparty"]
                        rowDiv.appendChild(cntpCol)

                        const ctgCol = document.createElement("div")
                        ctgCol.setAttribute("class", "col-2")
                        ctgCol.textContent = transactions[i]["category"]
                        rowDiv.appendChild(ctgCol)

                        const walCol = document.createElement("div")
                        walCol.setAttribute("class", "col-2")
                        walCol.textContent = transactions[i]["wallet"].join(", ")
                        rowDiv.appendChild(walCol)

                        const descCol = document.createElement("div")
                        descCol.setAttribute("class", "col-2")
                        descCol.textContent = transactions[i]["description"]
                        rowDiv.appendChild(descCol)

                        let wordFilter = document.querySelector(`.search-input`)
                        let valueFilter = document.querySelector(`.value-input`)
                        let fromDate = document.querySelector(".from-date-input")
                        let toDate = document.querySelector(".to-date-input")


                        let params = data["parameters"]
                        wordFilter.value = params["word_filter"]
                        valueFilter.value = params["value_filter"]
                        toDate.value = params["to_date"]
                        if (params["from_date"] === "2000-01-01") {
                            params["from_date"] = ""
                        }
                        fromDate.value = params["from_date"]

                        scrollToClone.appendChild(linkToClone)
                        linkToClone.appendChild(rowDiv)

                        searchFilter()
                    }
                }
            });
    }


    // event.target.removeEventListener("click", updateUrl);
    // event.target.click();
}
