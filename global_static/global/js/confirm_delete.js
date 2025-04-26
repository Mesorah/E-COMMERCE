function my_scope() {
    const forms = document.querySelectorAll('.form-delete');
    for (const form of forms) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();

        const formAction = form.getAttribute('action');

        let confirmed = false;

        if (formAction.includes('ordered')) {
          confirmed = confirm('Voce tem certeza que quer concluir?');
        } else {
          confirmed = confirm('Voce tem certeza que quer excluir?');
        };
        
        if (confirmed) {
          form.submit();
        }
      });
    }
  }
  my_scope();