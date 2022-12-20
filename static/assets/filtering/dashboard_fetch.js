// const triggers = document.querySelectorAll(".trigger")
//
// triggers.forEach(function (trigger) {
//     trigger.addEventListener("click", function (e) {
//         e.preventDefault()
//         fetchforDashboard(this.getAttribute("href")+"&json=1")
//     })
// })
//
// function fetchforDashboard(url) {
//     // console.log(url)
//     fetch(url)
//             .then((response) => {
//                 return response.json();
//             })
//             .then((d) => {
//                 console.log(d)
//
//
//                 let chainGraphs = document.querySelector("#chain_graphs")
//                 let chainGraphsParameter = chainGraphs.value
//                 chainGraphs.value = `${d["chain_graphs"]}`
//
//                 let absButtonLeft = document.querySelector("#abs_button_left")
//                 absButtonLeft.setAttribute("href", `?abs_year=${d["abs_year"]}&abs_month=${d["abs_month"]-1}
//                 &chain_graphs=${chainGraphsParameter}`)
//
//                 let absButtonRight = document.querySelector("#abs_button_right")
//                 absButtonRight.setAttribute("href", `?abs_year=${d["abs_year"]}&abs_month=${d["abs_month"]+1}
//                 &chain_graphs=${chainGraphsParameter}`)
//
//                 let topBeam = document.querySelector("#top_beam")
//                 topBeam.textContent = `Summary for wallet: ${d["default_wallet"]["name"]} in ${d["abs_displayed_date"]}`
//
//                 let absNoTransactions = document.querySelector("#abs_no_transactions")
//                 absNoTransactions.textContent = `${d["abs_no_transactions"]}`
//
//                 let showMonthTransactions = document.querySelector("#show_month_transactions")
//                 let transUrl = new URL(showMonthTransactions.getAttribute("href"), document.baseURI)
//                 let dateParams = transUrl.searchParams
//                 dateParams.set('fromDate', `${d["abs_year"]}-${d["abs_month"]}-1`)
//                 transUrl.search = dateParams.toString()
//                 let newTransUrl = transUrl.toString()
//                 showMonthTransactions.setAttribute("href", newTransUrl)
//
//                 let monthlyProfit = document.querySelector("#monthly_profit")
//                 monthlyProfit.textContent = `${d["monthly_profit"]}`
//
//                 let monthlyDebit = document.querySelector("#monthly_debit")
//                 monthlyDebit.textContent = `${d["monthly_debit"]}`
//
//                 let monthlyBalance = document.querySelector("#monthly_balance")
//                 monthlyBalance.textContent = `${d["monthly_balance"]}`
//
//                 let cumButtonLeft = document.querySelector("#cum_button_left")
//                 cumButtonLeft.setAttribute("href", `?cum_year=${d["cum_year"]}&cum_month=${d["cum_month"]-1}
//                 &chain_graphs=${chainGraphsParameter}`)
//
//                 let cumButtonRight = document.querySelector("#abs_button_right")
//                 cumButtonRight.setAttribute("href", `?cum_year=${d["cum_year"]}&cum_month=${d["cum_month"]+1}
//                 &chain_graphs=${chainGraphsParameter}`)
//
//                 let bottomBeam = document.querySelector("#bottom_beam")
//                 bottomBeam.textContent = `Summary for wallet: ${d["default_wallet"]["name"]}`
//
//                 let totalTransactions = document.querySelector("#total_transactions")
//                 totalTransactions.textContent = `${d["total_transactions"]}`
//
//                 let showByWallet = document.querySelector("#show_by_wallet")
//                 let walletUrl = new URL(showByWallet.getAttribute("href"), document.baseURI)
//                 let walletParams = walletUrl.searchParams
//                 walletParams.set('filter_val', `${d["default_wallet"]["pk"]}`)
//                 walletUrl.search = walletParams.toString()
//                 let newWalletUrl = walletUrl.toString()
//                 showByWallet.setAttribute("href", newWalletUrl)
//
//                 let totalProfit = document.querySelector("#total_profit")
//                 totalProfit.textContent = `${d["total_profit"]}`
//
//                 let totalDebit = document.querySelector("#total_debit")
//                 totalDebit.textContent = `${d["total_debit"]}`
//
//                 let totalBalance = document.querySelector("#total_balance")
//                 totalBalance.textContent = `${d["total_balance"]}`
//
//                 let absValues = d["abs_values_list"]
//                 let cumValues = d["cum_values_list"]
//                 let absDate = d["abs_displayed_date"]
//                 let cumDate = d["cum_displayed_date"]
//                 drawGraphAbs(absValues, absDate)
//                 drawGraphCum(cumValues, cumDate)
//
//             })
// }