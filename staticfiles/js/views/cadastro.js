$(document).ready(function() {
    const Form = $('#form').parsley();

    $('#save_btn').click(function(event){
        const isValid = Form.validate()
        if(isValid)
        {
            console.log("Formulário válido")
        }
        else
        {
            console.error("Formulário inválido!")
        }

    });

    document.getElementById("cpf").addEventListener("input", function (e) {
        let value = e.target.value;
        
        // Remove qualquer caractere que não seja número
        value = value.replace(/\D/g, "");
    
        // Formata o CPF automaticamente (000.000.000-00)
        value = value.replace(/^(\d{3})(\d)/, "$1.$2");
        value = value.replace(/^(\d{3})\.(\d{3})(\d)/, "$1.$2.$3");
        value = value.replace(/^(\d{3})\.(\d{3})\.(\d{3})(\d)/, "$1.$2.$3-$4");
    
        e.target.value = value;
    });



});