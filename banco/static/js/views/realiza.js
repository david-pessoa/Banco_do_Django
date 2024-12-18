$(document).ready(function() {
    const Form = $('form').parsley();

    function validarString(input) {
        // Regex para verificar se contém exatamente 11 números consecutivos
        const regex11Numeros = /^\d{11}$/;

        // Regex para verificar se é um email válido
        const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
        // Regex para verificar se é um CPF válido (formato 000.000.000-00)
        const regexCPF = /^\d{3}\.\d{3}\.\d{3}-\d{2}$/;
    
        // Testa os critérios
        if (regex11Numeros.test(input) || regexEmail.test(input) || regexCPF.test(input)) {
            return true;
        }
        return false;
    }
    

    $('#save_btn').click(function(event)
    {
        const chave_pix = document.getElementById("chave").value
        const isValid = Form.validate() && validarString(chave_pix)
        if(isValid)
        {
            console.log("Formulário válido")
        }
        else
        {
            console.error("Formulário inválido!")
            event.preventDefault();
        }

    });

    document.getElementById("money").addEventListener("input", function (e) {
        let value = e.target.value;
        // Remove caracteres não numéricos
        value = value.replace(/\D/g, "");
        if(value === "" )
            value = "0.00"
        // Converte para número com duas casas decimais
        value = (parseInt(value) / 100).toFixed(2);
        
    
        // Substitui ponto por vírgula para as casas decimais
        value = value.replace(".", ",");
    
        // Adiciona os pontos para os milhares
        value = value.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        
        // Atualiza o valor no input
        e.target.value = value || "0,00";
    });

});