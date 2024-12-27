window.Parsley.addValidator('chavePix', {
    validateString: function(value) {
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
        return validarString(value)
    },
    messages: {
        pt: 'Chave pix inválida!'
    }
});

window.Parsley.addValidator('novaChavePix', {
    validateString: function(value, TipoChaveSelector) {
        const tipo_chave_pix = document.querySelector(TipoChaveSelector).value
        console.log(value)
        if (tipo_chave_pix === 'E-mail')
        {
            // Regex para verificar se é um email válido
            const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if(regexEmail.test(value))
            {
                return true;
            }
            else
            {
                return false;
            }
        }
        else if (tipo_chave_pix === 'CPF')
        {
            // Regex para verificar se é um CPF válido (formato 000.000.000-00)
            const regexCPF = /^\d{3}\.\d{3}\.\d{3}-\d{2}$/;
            if(regexCPF.test(value))
            {
                return true;
            }
            else
            {
                return false;
            }

        }
        else if(tipo_chave_pix === 'Número de celular')
        {
            // Regex para verificar se contém exatamente 11 números consecutivos
            const regex11Numeros = /^\d{11}$/;
            if(regex11Numeros.test(value))
            {
                return true;
            }
            else
            {
                return false;
            }
        }
        else
        {
            return true;
        }
        
    },
    messages: {
        pt: 'Chave pix inválida!'
    }
});