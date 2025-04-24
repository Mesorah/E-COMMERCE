function main() {
    const form = document.querySelector('.crud-product-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const isValid = getElements()

        if(isValid) form.submit();
    });
}

function getElements() {
    const elements = document.querySelectorAll('.form-control');
    const isValidElements = validElements(elements);

    const name = document.querySelector('#id_name');
    const isValidName = validName(name);

    const price = document.querySelector('#id_price');
    const isValidPrice = validPrice(price);

    const stock = document.querySelector('#id_stock');
    const isValidStock = validStock(stock);

    return isValid(isValidElements, isValidName, isValidPrice, isValidStock);
}

function isValid(validElements, validName, ValidPrice, ValidStock) {
    if(validElements && validName && ValidPrice && ValidStock) return true;

    return false;
}

function addError(element, msg) {
    const newDiv = document.createElement('div');
    newDiv.className = 'error-message';
    newDiv.textContent = msg;
    
    element.insertAdjacentElement('beforebegin', newDiv);
}

function validElements(elemets) {
    const errors = document.querySelectorAll('.error-message');
    let valid = true;

    for(const element of errors) {
        element.remove();
    }

    for(const element of elemets) {
        if(!element.value){
            addError(element, `O ${element.name} não estar ser vazio.`);

            valid = false;
        }
    }

    return valid;
}

function validName(name) {
    if(name.value.length <= 2) {
        addError(
            name, 'Nome de produto muito pequeno, precisa-se de pelo menos 3 caracteres.'
        );

        return false;
    }

    return true;
}

function validPrice(price) {
    if(price.value < 0) {
        addError(
            price, 'O preço do produto não pode ser menor ou igual a 0.'
        );

        return false;
    }

    return true;
}

function validStock(stock) {
    if(stock.value < 0) {
        addError(
            stock, 'O valor do stock não pode ser menor que 0.'
        );

        return false;
    }

    return true;
}

main();