const output = document.getElementById("output");
output.textContent = "0";


function addValue(button) {
      if (output.textContent === "0")
            output.textContent = "";

      const newOperation = button.querySelector('h1').textContent

      output.textContent += newOperation;
}

const standardButtons = document.getElementsByClassName('standard-button');
Array.from(standardButtons).forEach((button) => {

    button.addEventListener('click', () => {

        addValue(button);
    });
});

document.getElementById('clear-button').addEventListener('click', () => {

    output.textContent = "0";
});

document.getElementById('evaluate-button').addEventListener('click', () => {

    try {
        output.textContent = eval(output.textContent);
    }
    catch (error) {
        alert(error.textContent);
    }
});