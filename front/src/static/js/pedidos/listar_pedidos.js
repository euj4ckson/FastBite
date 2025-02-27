async function abrirModal(pedidoId) {
    const modal = document.getElementById('detalhesModal');
    const detalhesDiv = document.getElementById('detalhesPedido');

    try {
        // Realizando a requisição para obter os detalhes do pedido
        const response = await fetch(`/api/pedido/${pedidoId}`);
        if (response.ok) {
            const pedido = await response.json();

            // Montando o HTML com os dados do pedido
            let html = `
                <p><strong>ID do Pedido:</strong> ${pedido.id}</p>
                <p><strong>Cliente:</strong> ${pedido.cliente_nome}</p>
                <p><strong>Observação:</strong> ${pedido.observacao}</p>
                <p><strong>Valor Total:</strong> R$ ${parseFloat(pedido.valor_total).toFixed(2)}</p>
                <h4>Itens do Pedido:</h4>
                <table>
                    <thead>
                        <tr>
                            <th>Produto</th>
                            <th>Quantidade</th>
                            <th>Valor Unitário</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            // Iterando sobre os itens para preencher a tabela
            for (const item of pedido.itens) {
                const produto = item.produto || {};
                html += `
                    <tr>
                        <td>${produto.nome || 'Produto não encontrado'}</td>
                        <td>${item.quantidade}</td>
                        <td>R$ ${produto.valor ? parseFloat(produto.valor).toFixed(2) : '0.00'}</td>
                        <td>R$ ${(produto.valor ? produto.valor * item.quantidade : 0).toFixed(2)}</td>
                    </tr>
                `;
            }

            html += `
                    </tbody>
                </table>
            `;

            // Exibindo os dados no modal
            detalhesDiv.innerHTML = html;
            modal.style.display = 'block';
        } else {
            // Exibindo mensagem de erro no modal
            detalhesDiv.innerHTML = `<p>Erro ao carregar os detalhes do pedido.</p>`;
            modal.style.display = 'block';
        }
    } catch (error) {
        // Exibindo mensagem de erro no modal
        detalhesDiv.innerHTML = `<p>Erro ao carregar os detalhes do pedido.</p>`;
        console.error('Erro ao buscar os detalhes do pedido:', error);
        modal.style.display = 'block';
    }
}

// Fechar o modal
function fecharModal() {
    const modal = document.getElementById('detalhesModal');
    modal.style.display = 'none';
}
