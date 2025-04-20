import { ValidateCPF } from "./CPFVerify.js";


function main() {
    const form = document.querySelector('.author-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const isValid = getElements()

        if(isValid) form.submit();
    });
}

function getElements() {
    const elements = document.querySelectorAll('.form-control');
    const isValidElements = validElements(elements);

    const username = document.querySelector('#id_username');
    const isValidUsername = validUsername(username);

    const cpf = document.querySelector('#id_cpf');
    const isValidCPF = validCPF(cpf);

    const password1 = document.querySelector('#id_password1');
    const password2 = document.querySelector('#id_password2');
    const isValidPassword = validPassword(password1, password2, username);

    return isValid(isValidElements, isValidUsername, isValidCPF, isValidPassword);
}

function isValid(validElements, validUsername, validCPF, validPassword) {
    if(validElements && validUsername && validCPF && validPassword) return true;

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
            addError(element, `O ${element.name} não estar ser vazio`);

            valid = false;
        }
    }

    return valid;
}

function validUsername(username) {
    if(username.value.length > 150) addError(
        username, `O ${username.name} não pode ter mais que 150 caracteres`
    );

    if(username.value.length <= 3) addError(
        username, `O ${username.name} precisa de pelo menos 3 caracteres`
    );

    return username.name.length < 3 && username.name.length > 150;
}

function validCPF(cpf) {
    const CPF = new ValidateCPF(cpf.value);

    if(!CPF.validate()) addError(cpf, `${cpf.name} inválido`);

    return CPF.validate();
}

function validPassword(password1, password2, username) {
    let valid = true;

    if(password1.value !== password2.value) {
        addError(password1, `A ${password1.name} tem que ser igual a ${password2.name}`);
        addError(password2, `A ${password2.name} tem que ser igual a ${password1.name}`);
        valid = false;
    }

    if(password1.value.length < 8) {
        addError(
            password1, `A ${password1.name} tem que ser maior que 8 caracteres`
        );

        valid = false;
    }

    if(isNumeric(password1)) valid = false;

    if(password1.value === username.value) {
        addError(
            password1, `A ${password1.name} não pode ser igual ao ${username.name}`
        );

        valid = false;
    }

    return valid;
}

function isNumeric(password) {
    try {
        const value = Number(password.value);
        
        // if you couldn't turn it into a numerical 
        if(value) {
            addError(
                password, `A ${password.name} não pode ser interamente numérica`
            );
            
            return true;
        }
        
    } catch (error) {
        return false;
    }   
}


// If you are not on the login page
if(!document.querySelector('#id_password')) main();
