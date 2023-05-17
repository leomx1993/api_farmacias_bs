# api_farmacias_bs
Projeto em Python para utilização de API com DB para uma rede de farmácias com autenticação

API - Backend 
Esta API backend foi desenvolvida como parte de um teste para a empresa Bluestorm. Ela fornece endpoints para autenticação, consulta de pacientes, farmácias e transações.

Endpoints Disponíveis
A API oferece os seguintes endpoints:

Autenticação

POST /auth: Realiza a autenticação e gera um token de acesso.
Pacientes

GET /patients: Retorna uma lista de pacientes com opção de filtragem por nome e sobrenome.
Farmácias

GET /pharmacies: Retorna uma lista de farmácias com opção de filtragem por nome e cidade.
Transações

GET /transactions: Retorna uma lista de transações com opção de filtragem por nome do paciente e nome da farmácia.
Requisitos de Instalação
Para executar a API localmente, você precisa ter o seguinte instalado em sua máquina:

Python 3
Flask
Flask-JWT-Extended
SQLite3

Abra um terminal e navegue até o diretório raiz do projeto.

Execute o seguinte comando para iniciar o servidor da API:

 python projeto_teste_bluestorm.py
 
Testes Automatizados:

A API inclui testes automatizados para verificar o funcionamento correto dos endpoints. Para executar os testes automatizados, siga estas etapas:

Certifique-se de que a API esteja em execução localmente.

Execute o seguinte comando para iniciar os testes:

python test_api.py

Os testes serão executados e os resultados serão exibidos no terminal.

Observações
A senha para autenticação é definida como "Senha123@" para o usuário "admin". Por motivos de segurança, é altamente recomendável alterar essa senha em um ambiente de produção.

Os dados são armazenados em um banco de dados SQLite chamado "backend_test.db".

Os filtros de pesquisa nos endpoints de pacientes, farmácias e transações são fornecidos como parâmetros de consulta. Os filtros são opcionais e podem ser combinados para refinar a pesquisa.

Certifique-se de que todas as dependências mencionadas no código-fonte estejam instaladas corretamente antes de executar a API ou os testes automatizados.

Este é um exemplo básico de implementação de uma API Flask e pode ser aprimorado para atender a requisitos adicionais de segurança, desempenho e funcionalidade.
