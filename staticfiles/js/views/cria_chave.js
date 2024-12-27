$(document).ready(function() {
    const Form = $('form').parsley();

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

});