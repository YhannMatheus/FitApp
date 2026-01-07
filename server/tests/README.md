# Testes do KiloCal API

Este diretório contém os testes automatizados da API KiloCal usando pytest.

## Estrutura

```
tests/
├── conftest.py          # Configurações e fixtures globais
└── user/                # Testes das rotas de usuário
    ├── __init__.py
    ├── test_register.py # Testes de registro
    ├── test_login.py    # Testes de login
    └── test_profile.py  # Testes de perfil
```

## Instalação das dependências

```bash
pip install pytest pytest-asyncio httpx
```

## Executar os testes

### Executar todos os testes
```bash
pytest
```

### Executar testes de um módulo específico
```bash
pytest tests/user/test_register.py
pytest tests/user/test_login.py
pytest tests/user/test_profile.py
```

### Executar um teste específico
```bash
pytest tests/user/test_register.py::test_register_success
```

### Executar com mais verbosidade
```bash
pytest -v
```

### Executar e mostrar print statements
```bash
pytest -s
```

### Executar com coverage
```bash
pytest --cov=src --cov-report=html
```

## Fixtures disponíveis

### `client`
Cliente HTTP assíncrono para fazer requisições à API.

```python
async def test_example(client: AsyncClient):
    response = await client.get("/endpoint")
    assert response.status_code == 200
```

### `test_user_data`
Dados de um usuário de teste padrão.

```python
async def test_example(test_user_data):
    assert test_user_data["email"] == "test@example.com"
```

### `authenticated_client`
Cliente HTTP já autenticado com um token JWT válido.

```python
async def test_example(authenticated_client):
    client, token = authenticated_client
    response = await client.get("/user/profile")
    assert response.status_code == 200
```

## Cobertura de testes

### Rotas de Usuário

#### POST /user/register
- ✅ Registro bem-sucedido
- ✅ Email duplicado
- ✅ Email inválido
- ✅ Campos obrigatórios faltando
- ✅ Gênero inválido
- ✅ Nível de atividade inválido
- ✅ Altura negativa
- ✅ Flag remember

#### POST /user/login
- ✅ Login bem-sucedido
- ✅ Email não registrado
- ✅ Senha incorreta
- ✅ Email faltando
- ✅ Senha faltando
- ✅ Credenciais vazias
- ✅ Flag remember
- ✅ Email case-sensitive

#### GET /user/profile
- ✅ Obtenção de perfil com sucesso
- ✅ Sem autenticação
- ✅ Token inválido
- ✅ Token expirado
- ✅ Token malformado
- ✅ Prefixo Bearer faltando
- ✅ Workouts vazios
- ✅ Histórico corporal vazio
- ✅ Dados corretos do usuário

## Boas práticas

1. **Use fixtures** para configuração e dados de teste reutilizáveis
2. **Teste casos positivos e negativos** - não teste apenas o caminho feliz
3. **Isole os testes** - cada teste deve ser independente
4. **Nomeie testes descritivamente** - use `test_nome_do_que_esta_testando`
5. **Use asserts claros** - facilite a identificação de falhas
6. **Limpe dados de teste** - use fixtures com yield para cleanup

## Próximos passos

- [ ] Adicionar testes para rotas de workout
- [ ] Adicionar testes para rotas de exercise
- [ ] Adicionar testes para rotas de set
- [ ] Adicionar testes de integração
- [ ] Configurar CI/CD para executar testes automaticamente
