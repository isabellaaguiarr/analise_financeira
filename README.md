# AP2 - Sistema de Análise Financeira

## Descrição

 Um sistema de análise financeira que permite aos usuários explorar dados financeiros, gerar carteiras personalizadas de ações, e visualizar gráficos comparativos de desempenho entre a carteira e o índice Ibovespa. O sistema é baseado em Python e utiliza o framework Streamlit para a interface do usuário.

## Funcionalidades

1. **Geração de Carteiras**: Permite ao usuário selecionar os critérios de rentabilidade e desconto para montar uma carteira de ações.
2. **Análise Comparativa**: Compara o desempenho da carteira gerada com o Ibovespa, exibindo gráficos interativos.
3. **Visualização de Dados**: Exibe gráficos individuais para os indicadores das ações e gráficos comparativos com o índice Ibovespa.

## Requisitos

- Python 3.8+
- Streamlit
- pandas
- matplotlib
- requests
- dotenv

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/isabellaaguiarr/analise_financeira.git
    ```

2. Navegue até o diretório do projeto:

    ```bash
    cd projetoFinal
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Crie um arquivo `.env` no diretório raiz do projeto e adicione a chave `TOKEN` com o valor do token de autenticação necessário para acessar a API.

    ```bash
    TOKEN=seu_token_aqui
    ```

## Uso

### 1. Executando o aplicativo Streamlit

Para iniciar o aplicativo, basta executar o seguinte comando:

```bash
streamlit run frontend/app.py
