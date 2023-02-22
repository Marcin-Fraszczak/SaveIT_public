const categoryField = document.querySelector("select#id_category")
const counterpartyField = document.querySelector("select#id_counterparty")
const walletField = document.querySelector("select#id_wallet")

const curveField = document.querySelector("select#id_curve_type")

if (categoryField) {
    for (let field of [categoryField, counterpartyField, walletField]) {
        field.classList.add("form-control")
        field.classList.remove("select", "form-select", "selectmultiple")
    }
    walletField.size = 2
}

if (curveField) {
    curveField.classList.add("form-control")
}
