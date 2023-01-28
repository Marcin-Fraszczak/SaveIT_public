function drawGraphAbs(absValues, absDate) {
    let days = [];
    let profits = [];
    let debits = [];

    for (let value of absValues) {
        days.push(value[0]);
        profits.push(value[1]);
        debits.push(-value[2]);
    }

    new Chart("chartAbsolute", {
        type: "line",
        data: {
            labels: days,
            datasets: [{
                data: debits,
                label: "debits",
                borderColor: "red",
                fill: false
            },
            //     {
            //     data: profits,
            //     label: "profits",
            //     borderColor: "green",
            //     fill: false
            // }
            ]
        },
        options: {
            title: {
                display: true,
                text: `Absolute debits for ${absDate}`,
            },
            legend: {
                display: true,
                position: "bottom",
            }
        }
    });
}


function drawGraphCum(cumValues, cumDate) {
    let days = [];
    let profitCumulative = [];
    let debitCumulative = [];
    let plan = [];

    for (let value of cumValues) {
        days.push(value[0]);
        profitCumulative.push(value[3]);
        debitCumulative.push(-value[4]);
        plan.push(value[5]);
    }

    new Chart("chartCumulative", {
        type: "line",
        data: {
            labels: days,
            datasets: [{
                data: debitCumulative,
                label: "debits",
                borderColor: "red",
                fill: false
            },
                {
                data: profitCumulative,
                label: "profits",
                borderColor: "green",
                fill: false
            },
            {
                data: plan,
                label: "savings plan",
                borderColor: "blue",
                fill: false
            }
            ]
        },
        options: {
            title: {
                display: true,
                text: `Cumulative values for transactions ${cumDate}`,
            },
            legend: {
                display: true,
                position: "bottom",
            }
        }
    });
}


const dashboardButtons = [...document.querySelectorAll(".dash-link")]

dashboardButtons.forEach(function (button) {
    button.addEventListener("click", updateUrl);
});

function updateUrl(event) {
    event.preventDefault()

    let wordFilter = document.querySelector(`.chain-graphs`).value;

    let url = new URL(this.getAttribute('href'), document.baseURI);

    let search_params = url.searchParams
    search_params.set('chain_graphs', wordFilter)
    url.search = search_params.toString()
    let new_url = url.toString()

    event.target.setAttribute("href", new_url)

    event.target.removeEventListener("click", updateUrl);
    event.target.click()
}
