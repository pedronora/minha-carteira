function removeChildElement(parent) {
    while (parent.firstChild) {
        parent.firstChild.remove()
    }
}

function currencyFormat(value) {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value)
}

function calcCustos() {
        let sumTotal = dados.map(function(item) { return (item.preco * item.quantidade) })
            .reduce(function(a, b) { return a + b }, 0)

        let custos = totalNota - sumTotal

        if (custos >= 0) {
            removeChildElement(tabelaDados)
            mostrarTabela(custos, sumTotal)
        } else {
            dados.pop()
            alert("Erro! O valor das operações é maior que o valor da nota!")
        }
}

function mostrarTabela(custos, sumTotal) {
    dados.forEach(op => {
        let linha = document.createElement("tr")
        linha.classList.add("align-middle")
        linha.classList.add("text-center")

        let celCodigo = document.createElement("td")
        celCodigo.innerText = op.codigo

        let celPreco = document.createElement("td")
        celPreco.innerText = currencyFormat(op.preco)

        let celQuantidade = document.createElement("td")
        celQuantidade.innerText = op.quantidade

        let celCustos = document.createElement("td")
        celCustos.innerText = currencyFormat(((op.preco * op.quantidade) * custos / sumTotal))

        let celRemove = document.createElement("td")
        let removeBtn = document.createElement("button")
        removeBtn.classList.add("btn")
        removeBtn.classList.add("btn-outline-danger")
        removeBtn.classList.add("btn-sm")
        removeBtn.innerText = "Remover"

        removeBtn.addEventListener("click", _ => {
            dados.splice(dados.indexOf(op), 1)
            calcCustos()
        })
        
        celRemove.appendChild(removeBtn)

        linha.append(celCodigo, celPreco, celQuantidade, celCustos, celRemove)

        tabelaDados.appendChild(linha)
    })
}

const form = document.forms['form']
let addBtn = document.getElementById("addBtn")
let resultados = document.getElementById("resultados")
let tabela = document.getElementById("table")
let tabelaDados = document.getElementById("tableBody")

let totalNota
let dados = []
addBtn.addEventListener("click", (e) => {

    if (
        form.codigo.checkValidity(),
        form.preco.checkValidity(),
        form.quantidade.checkValidity()
    ) {
        let newObject = new Object()
        newObject.codigo = form.codigo.value
        newObject.preco = form.preco.value
        newObject.quantidade = form.quantidade.value
        totalNota = form.valorNota.value
        dados.push(newObject)

        calcCustos()

        e.preventDefault()
        form.codigo.value = ""
        form.preco.value = ""
        form.quantidade.value = ""
    }
})