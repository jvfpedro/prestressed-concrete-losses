# Cálculo de Perdas em Concreto Protendido�

Este repositório contém scripts desenvolvidos em Python para automatizar o cálculo de perdas de protensão em vigas de concreto, seguindo normativas de Engenharia Civil.

O projeto foi desenvolvido para auxiliar no dimensionamento e verificação de estruturas, calculando tanto as perdas que ocorrem no ato da protensão quanto as que ocorrem ao longo da vida útil da estrutura.

## Estrutura dos Arquivos

* **`perdas_imediatas.py`**: calcula as perdas que ocorrem no momento da protensão.
    * Atrito.
    * Acomodação da ancoragem (considerando diferentes hipóteses de escorregamento).
    * Encurtamento elástico imediato do concreto.
* **`perdas_prog_ret_flu.py`**: calcula as perdas progressivas dependentes do tempo.
    * Retração do concreto (considerando umidade e espessura fictícia).
    * Fluência (deformação lenta) do concreto.
* **`perdas_prog_relax.py`**: calcula a perda por relaxação do aço de protensão.

## Tecnologias Utilizadas

* **Python 3**
* Biblioteca `math` para equações complexas e funções exponenciais.

## Como usar

1. Clone o repositório ou baixe os arquivos `.py`.
2. Abra o arquivo desejado em sua IDE de preferência ou editor de texto.
3. Insira os parâmetros de entrada da sua viga no início do código (ex: número de cordoalhas, área de aço, fck, etc.).
4. Execute o script para obter os valores das perdas em kN.

---
*Desenvolvido por João Vitor Pedro*
