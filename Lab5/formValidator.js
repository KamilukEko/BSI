const errors = [];

function updateInputError(input, containsErrors) {

    if (containsErrors)
    {
        if (errors.includes(input.name))
            return;

        input.previousElementSibling.classList.add("error-label");
        input.classList.add("error")
        errors.push(input.name);
        return;
    }

    if (!errors.includes(input.name))
        return;

    input.previousElementSibling.classList.remove("error-label");
    input.classList.remove("error")
    errors.remove(input.name);
}

const phoneNumberRegex = /^(\+\d{1,3}[-.\s]?)?(\(?\d{2,3}\)?[-.\s]?)?(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{3})$/;
const textRegex = /^[A-Za-ząęłńóśźżĄĘŁŃÓŚŹŻ\s]{1,64}$/;
const numbersRegex = /^[1-9][0-9]{0,3}]$/;

function validateInput(input) {

    let containsErrors = false;

    switch (input.getAttribute("validation-type")) {
        case "phone-number":
            containsErrors = !phoneNumberRegex.test(input.value);
            break
        case "text":
            containsErrors = !textRegex.test(input.value);
            break
        case "number":
            containsErrors = !numbersRegex.test(input.value);
            break
        default:
            return;
    }

    updateInputError(input, containsErrors);
}

const timeouts = {};

const inputs = document.getElementsByTagName("input")
Array.from(inputs).forEach((input) => {

    if (input.name === undefined)
        return;

    input.addEventListener("input", () => {

        if (!timeouts.hasOwnProperty(input.name))
            timeouts[input.name] = null;

        clearTimeout(timeouts[input.name]);
        timeouts[input.name] = setTimeout(() => validateInput(input), 500)
    });
});

document.getElementById('personal-data-form').addEventListener('submit', (e) => {
    if (errors.length) {
        e.preventDefault();
        alert("This form contains errors")
    }
});