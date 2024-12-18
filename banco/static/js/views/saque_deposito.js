$(document).ready(function() {

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