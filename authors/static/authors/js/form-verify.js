import { ValidateCPF } from "./CPF-verify.js";


function main() {
    const form = document.querySelector('.author-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        getElements();
    });
}

function getElements() {
    const elements = document.querySelectorAll('.form-control');
    validElements(elements);

    const username = document.querySelector('#id_username');
    validUsername(username);

    const cpf = document.querySelector('#id_cpf');
    validCPF(cpf);

    const password1 = document.querySelector('#id_password1');
    const password2 = document.querySelector('#id_password2');
    validPassword(password1, password2, username);
}

function addError(element, msg) {
    const newDiv = document.createElement('div');
    newDiv.className = 'error-message';
    newDiv.textContent = msg;
    
    element.insertAdjacentElement('beforebegin', newDiv);
}

function validElements(elemets) {
    const errors = document.querySelectorAll('.error-message');
    for(const element of errors) {
        element.remove();
    }

    for(const element of elemets) {
        if(!element.value) addError(element, `O ${element.name} não estar ser vazio`);
    }
}

function validUsername(username) {
    if(username.value.length > 150) addError(
        username, `O ${username.name} não pode ter mais que 150 caracteres`
    );

    return username.value.length > 150;
}

function validCPF(cpf) {
    const CPF = new ValidateCPF(cpf.value);

    if(!CPF.validate()) addError(cpf, `${cpf.name} inválido`);

    return CPF.validate();
}

function validPassword(password1, password2, username) {
    if(password1.value !== password2) {
        addError(password1, `A ${password1.name} tem que ser igual a ${password2.name}`);
        addError(password2, `A ${password2.name} tem que ser igual a ${password1.name}`);
    }

    if(password1.value.length < 8) addError(
        password1, `A ${password1.name} tem que ser maior que 8 caracteres`
    );

    if(typeof password1.value === Number) addError(
        password1, `A ${password1.name} não pode ser interamente numérica`
    );

    if(password1.value === username.value) addError(
        password1, `A ${password1.name} não pode ser igual ao ${username.name}`
    );
}

main();