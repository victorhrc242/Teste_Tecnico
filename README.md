# API Produtos Worten

## Descrição do Projeto
Este projeto foi desenvolvido como parte de um **desafio técnico para vaga de Backend**.  
O objetivo é criar um sistema que lê uma planilha de produtos (`worten.xlsx`), busca informações atualizadas no site [worten.pt](https://www.worten.pt/) e disponibiliza esses dados via API REST.  

O projeto permite:  
- Processar e importar uma planilha inicial de produtos.  
- Buscar automaticamente os produtos na Worten, obtendo: nome, link, menor preço, vendedor e disponibilidade.  
- Salvar os dados em um arquivo Excel (`worten_final.xlsx`).  
- Gerenciar produtos via API (CRUD) e realizar download do Excel atualizado.  
- Garantir idempotência: produtos duplicados são ignorados.  

---

## Arquitetura do Sistema

O projeto segue uma arquitetura **MVC desacoplada com camadas de responsabilidade bem definidas**:

     +----------------+
     |   FastAPI App  |
     +--------+-------+
              |
              v
     +--------+-------+
     |   Controller    |  --> Recebe requisições HTTP, valida e chama o serviço
     +--------+-------+
              |
              v
     +--------+-------+
     |    Service     |  --> Lógica de negócio, processamento da planilha e scraping
     +--------+-------+
              |
              v
     +--------+-------+
     | Repository/DB  |  --> Persistência em Excel (.xlsx)
     +--------+-------+
              |
              v
     +--------+-------+
     |   Scraper      |  --> SeleniumBase para buscar dados na Worten.pt
     +----------------+
markdown
Copiar código

### Fluxo de Dados

1. O usuário coloca a planilha `worten.xlsx` dentro da pasta `data/`.  
2. O endpoint `/products/import-local` processa a planilha:  
   - Lê a planilha e verifica produtos já processados.  
   - Para cada produto novo, o `WortenScraper` consulta o site Worten.  
   - Extrai dados: nome, link, menor preço, vendedor e status.  
   - Salva os dados em `worten_final.xlsx`.  
3. O usuário pode listar produtos, adicionar manualmente, atualizar ou deletar via API.  
4. O usuário pode baixar o arquivo atualizado através do endpoint `/products/download`.  

---

## Tecnologias Utilizadas

- **Python 3.10+**  
- **FastAPI** → Criação de API REST e documentação automática via Swagger.  
- **uvicorn** → Servidor ASGI para rodar FastAPI.  
- **Pandas** → Manipulação de planilhas Excel (.xlsx).  
- **SeleniumBase** → Scraper automatizado para buscar dados na Worten.  
- **Pydantic** → Validação e serialização de dados.  
- **Dataclasses** → Modelagem de objetos de forma limpa e tipada.  
- **Excel (.xlsx)** → Persistência de dados (entrada e saída).  
- **Chrome** → Necessário para SeleniumBase funcionar.  

---

## Instalação

1. **Clonar o repositório**

```bash
git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_PROJETO>
Criar e ativar ambiente virtual

bash
Copiar código
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
Instalar dependências

bash
Copiar código
pip install -r requirements.txt
Preparar a pasta de dados

Criar a pasta data/

Colocar a planilha de entrada worten.xlsx dentro da pasta

Instalar o Google Chrome

SeleniumBase precisa do Chrome instalado para funcionar corretamente.

Certifique-se que a versão do Chrome seja compatível com o ChromeDriver do SeleniumBase.

Como Rodar
bash
Copiar código
uvicorn main:app --reload
A API estará disponível em: http://127.0.0.1:8000/

Documentação Swagger em: http://127.0.0.1:8000/docs

Endpoints da API
Método	Rota	Descrição
GET	/	Verifica se a API está funcionando
GET	/products/	Lista todos os produtos do Excel final
POST	/products/import-local	Processa a planilha worten.xlsx e adiciona produtos não duplicados
POST	/products/	Adiciona um produto manual via JSON:
{ "Name": "Nome do Produto" }
PUT	/products/{product_id}	Atualiza dados de um produto existente
DELETE	/products/{product_id}	Remove um produto do Excel
GET	/products/download	Baixa o Excel atualizado (worten_final.xlsx)

Exemplo de requisição POST manual
json
Copiar código
POST /products/
{
  "Name": "Notebook Dell Inspiron"
}
Testes e Validação
Unitários: testar funções do ProductService e ProductRepository.

Integração: verificar se o endpoint /products/import-local processa corretamente a planilha.

Manual: via Swagger ou Postman, testar:

Listagem de produtos

Criação manual

Atualização e remoção

Download do Excel

O scraper lida com produtos indisponíveis ou não encontrados, evitando falhas da aplicação.

Boas Práticas Implementadas
Arquitetura modular e desacoplada (Controller, Service, Repository, Scraper).

Uso de Pydantic e dataclasses para tipagem e validação.

Persistência imediata em Excel para evitar perda de dados.

Tratamento de erros:

Arquivo de entrada ausente

Produto não encontrado

Falha de scraping

Comentários e docstrings explicativos.

Idempotência: produtos duplicados não são processados novamente.

Observações Éticas
Este projeto é estritamente para avaliação técnica e não será usado comercialmente.

Arquivos temporários e Excel gerado estão incluídos no .gitignore.

Autor
Victor Hugo Rodrigues Costa
Desenvolvedor Backend
