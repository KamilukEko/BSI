const errors = [];

function updateInputError(input, containsErrors) {
    if (containsErrors) {
        if (!errors.includes(input.name)) {
            input.previousElementSibling?.classList.add("error-label");
            input.classList.add("error");
            errors.push(input.name);
        }
        return;
    }

    if (errors.includes(input.name)) {
        input.previousElementSibling?.classList.remove("error-label");
        input.classList.remove("error");
        errors.splice(errors.indexOf(input.name), 1);
    }
}

const phoneNumberRegex = /^(\+\d{1,3}[-.\s]?)?(?\d{2,3}?[-.\s]?)?(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{3})$/;
const textRegex = /^[A-Za-ząęłńóśźżĄĘŁŃÓŚŹŻ\s]{1,64}$/;
const numbersRegex = /^[1-9][0-9]{0,3}$/;

function validateInput(input) {
    let containsErrors = false;

    switch (input.getAttribute("validation-type")) {
        case "phone-number":
            containsErrors = !phoneNumberRegex.test(input.value.trim());
            break;
        case "text":
            containsErrors = !textRegex.test(input.value.trim());
            break;
        case "number":
            containsErrors = !numbersRegex.test(input.value.trim());
            break;
        default:
            return;
    }

    updateInputError(input, containsErrors);
}

const timeouts = {};

const inputs = document.querySelectorAll("input");
inputs.forEach((input) => {
    if (!input.name) return;

    input.addEventListener("input", () => {
        clearTimeout(timeouts[input.name]);
        timeouts[input.name] = setTimeout(() => validateInput(input), 500);
    });
});

document.getElementById("personal-data-form").addEventListener("submit", (e) => {
    if (errors.length > 0) {
        e.preventDefault();
        alert("This form contains errors.");
    }
});