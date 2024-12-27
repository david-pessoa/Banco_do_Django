$(document).ready(function () {
    $('#historico').DataTable({
        "language": {
            "url": "/static/datatables/datatables.pt-br.json"
        },
        "serverSide": true,
        "paging": true,
        "pageLength": 10,
        "ajax": {
            "url": `/historico/${usuario_id}`,
            "type": "GET",
            "dataScr": "data",
        
        },
        "columns": [
            {"data": "tipo"},
            {"data": "valor",
                "render": function(valor, type, row) {
                if (type === 'sort' || type === 'type') { //Verificar isso
                    return valor;
                }
                return valor; // Formato exibido
                }
            },
            {"data": "data",
            "render": function(data, type, row) {
                if (type === 'sort' || type === 'type') {
                    let partes = data.split(' '); // Divide em [data, hora]
                    let dataPartes = partes[0].split('/'); // Divide 'DD/MM/YYYY' em [DD, MM, YYYY]
                    let hora = partes[1]; // Obtém 'H:M'
                    // Reorganiza no formato legível pelo Date()
                    return new Date(`${dataPartes[2]}-${dataPartes[1]}-${dataPartes[0]}T${hora}`).getTime();
                }
                return data; // Formato exibido
            }
            }
        ],
        
        "createdRow": function(row, data, dataIndex) {
            // Verifica se o tipo de transação é 'DEPOSITO'
            
            value = data.valor.replace(/\D/g, "");

            // Converte para número com duas casas decimais
            value = (parseInt(value) / 100).toFixed(2);


            // Substitui ponto por vírgula para as casas decimais
            value = value.replace(".", ",");

            // Adiciona os pontos para os milhares
            value = value.replace(/\B(?=(\d{3})+(?!\d))/g, ".");

            if (data.tipo === 'DEPOSITO') {
                $('td', row).eq(0).text("Depósito");
                // Aplica a classe de cor vermelha e adiciona o sinal de menos ao valor
                $('td', row).eq(1).addClass('deposito').text('+ ' + value);
            }
            else
            {
                $('td', row).eq(1).addClass('saque').text('- ' + value);

                if(data.tipo === 'SAQUE')
                {
                    $('td', row).eq(0).text("Saque");
                }
                else
                {
                    $('td', row).eq(0).text("Pagamento PIX");
                }
            }
        },
    });
});
