
document.addEventListener("DOMContentLoaded", () => {
    const resumoCliente = document.getElementById('resumo-cliente');
    const resumoItens = document.getElementById('resumo-itens');
    const resumoTotal = document.getElementById('resumo-total');
    const clienteNomeInput = document.getElementById('cliente_nome');

    // Inicializa a variável global
    itensContainer = document.getElementById('itens');

    clienteNomeInput.addEventListener('input', () => {
        resumoCliente.textContent = clienteNomeInput.value || '-';
    });

    // Inicializa o resumo ao carregar a página
    updateResumo();
});

function updateResumo() {
    const resumoItens = document.getElementById('resumo-itens');
    const resumoTotal = document.getElementById('resumo-total');

    const itens = itensContainer.querySelectorAll('.produto-item');
    resumoItens.innerHTML = '';
    let total = 0;

    itens.forEach((item) => {
        const produtoSelect = item.querySelector('select');
        const quantidadeInput = item.querySelector('input[type="number"]');
        const valor = parseFloat(produtoSelect.options[produtoSelect.selectedIndex].dataset.valor || 0);
        const quantidade = parseInt(quantidadeInput.value || 0);

        if (quantidade > 0) {
            total += valor * quantidade;
            const listItem = document.createElement('li');
            listItem.textContent = `${produtoSelect.options[produtoSelect.selectedIndex].textContent} x ${quantidade} = R$ ${(valor * quantidade).toFixed(2)}`;
            resumoItens.appendChild(listItem);
        }
    });

    resumoTotal.textContent = total.toFixed(2);

    if (!resumoItens.children.length) {
        resumoItens.innerHTML = '<li>Nenhum item adicionado ainda</li>';
    }
}
function addProduto() {
    const select = document.createElement('select');
    const inputQuantidade = document.createElement('input');
    const buttonRemover = document.createElement('button');
    const div = document.createElement('div');
    div.classList.add('produto-item');

    // Preenche o select com as opções de produtos
    select.name = `itens[${itensContainer.children.length}][produto]`;
    select.required = true;
    select.id = 'prdform';
    select.onchange = validarProduto; // Nova validação no onchange

    produtos.forEach((produto) => {
        const option = document.createElement('option');
        option.value = produto.id; // ID do produto
        option.textContent = `${produto.nome} - R$ ${produto.valor}`;
        option.dataset.valor = produto.valor;
        select.appendChild(option);
    });

    inputQuantidade.type = 'number';
    inputQuantidade.name = `itens[${itensContainer.children.length}][quantidade]`;
    inputQuantidade.min = 1;
    inputQuantidade.placeholder = 'Quantidade';
    inputQuantidade.required = true;
    inputQuantidade.id = 'qtdeinput';
    inputQuantidade.oninput = updateResumo;

    buttonRemover.type = 'button';
    buttonRemover.textContent = 'Remover';
    buttonRemover.id = "deletebtn";
    buttonRemover.onclick = () => {
        div.remove();
        updateResumo();
    };

    div.appendChild(select);
    div.appendChild(inputQuantidade);
    div.appendChild(buttonRemover);
    itensContainer.appendChild(div);

    updateResumo();
}

// Nova função para validar se o produto já foi adicionado
function validarProduto(event) {
    const selectAtual = event.target;
    const produtoSelecionado = selectAtual.value;
    const itensExistentes = document.querySelectorAll('.produto-item select');

    for (let item of itensExistentes) {
        if (item !== selectAtual && item.value === produtoSelecionado) {
            alert(" produto já adicionado, remova da lista ou edite a quantidade!");
            selectAtual.value = ""; // Reseta a seleção para evitar duplicação
            return;
        }
    }
    
    updateResumo();
}



function removeProduto(button) {
    button.parentElement.remove();
    updateResumo();
}
