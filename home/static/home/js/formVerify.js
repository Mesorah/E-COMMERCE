import { validateCreditCard } from './cardValidator.js';

function main() {
    const form = document.querySelector('.payment-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const isValid = getElements()

        if(isValid) form.submit();
    });
}

function getElements() {
    const elements = document.querySelectorAll('.form-control');
    const isValidElements = validElements(elements);

    const creditCard = document.querySelector('#id_credit_card');
    const isValidCreditCard = validCreditCard(creditCard);

    const zipCode = document.querySelector('#id_zip_code');
    const isValidZipCode = validZipCode(zipCode);

    const expirationDate = document.querySelector('#id_expiration_date');
    const isValidExpirationDate = validExpirationDate(expirationDate);

    return isValid(isValidElements, isValidCreditCard, isValidZipCode, isValidExpirationDate);
}

function isValid(validElements, validCreditCard, isValidZipCode, ValidExpirationDate) {
    if(validElements && validCreditCard && isValidZipCode && ValidExpirationDate) return true;

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

function validCreditCard(cardNumber) {
    if(!validateCreditCard(cardNumber.value)) {
        addError(
            cardNumber, 'Cartão inválido.'
        );

        return false;
    }

    return true;
}

function validExpirationDate(expirationDate) {
    let valid = true;

    try {
        const parts = expirationDate.value.split('/');

        if(parts.length !== 2) {
            addError(
                expirationDate, 'Formato de data inválido. Use MM/AA ou MM/YYYY.'
            );

            valid = false;
        }
        
        let [month, year] = parts;

        month = Number(month);
        console.log(month, year)

        if(month < 1 || month > 12) {
            addError(
                expirationDate, 'Mês inválido.'
            );

            valid = false;
        }

        if(year.length === 2) year = '20' + year;
        year = Number(year);

        const currentYear = new Date().getFullYear();
        const currentMonth = new Date().getMonth() + 1;

        if (year < currentYear || (year === currentYear && month < currentMonth)) {
            addError(
                expirationDate, 'Ano de validade inválido.'
            );
            valid = false;
        }

    } catch(error) {
        addError(
            expirationDate, 'Formato de data inválido. Use MM/AA ou MM/YYYY.'
        );

        valid = false
    }

    return valid;
}

function validZipCode(zipCode) {
    if(zipCode.value !== '86390000') {
        addError(
            zipCode, 'CEP diferente de cambará'
        );

        return false;
    }

    return true
}

main();