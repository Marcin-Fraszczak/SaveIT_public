texts = {
    "python": "Built in Python 3.11",
    "pytest": "Funcionalities tested with pytest 7.2.0 and pytest-django 4.5.2",
    "bootstrap": "CSS framework: Bootstrap 5, crispy-bootstrap5 0.7",
    "mobirise": "Frontend solutions with: Mobirise 5, django-crispy-forms 1.14.0",
    "selenium": "Databases populated using Selenium 4.7.2 for Python",
    "postgres": "Tested and ready to work with PostgreSQL database",
    "mysql": "Currently working with mySQL database",
    "saveit": "SaveIT - educational app for tracking personal finances",
    "django": "Django 4.1.3 - webapp framework for python",
}





let textField = document.querySelector(".additional-text")

let images = document.querySelectorAll(".img")

images.forEach(function (image) {
    image.addEventListener("mouseover", function (e) {
        textField.textContent = texts[image.getAttribute("alt")]
    })
    image.addEventListener("mouseleave", function (e) {
        textField.textContent = ""
    })
})
