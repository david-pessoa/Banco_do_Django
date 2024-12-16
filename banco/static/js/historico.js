$(document).ready(function () {
    $('#historico').DataTable({
        "createdRow": function(row, data, dataIndex) {
            // Verifica se o tipo de transação é 'SAQUE'
            if (data[0] === 'Saque') {
                // Aplica a classe de cor vermelha e adiciona o sinal de menos ao valor
                $('td', row).eq(1).addClass('saque').text('- ' + data[1]);
            }
            else
            {
                $('td', row).eq(1).addClass('deposito').text('+ ' + data[1])
            }
        }
    });
});
