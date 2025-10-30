# API Portal

Este projeto é uma API em Python que monitora o status de streamers da Twitch e atualiza automaticamente o status de online/offline no Firestore.

## Funcionalidades

- **Monitoramento de Streamers**: Verifica periodicamente se os canais da Twitch estão online.
- **Integração com Firebase**: Armazena e atualiza dados dos streamers no Firestore.
- **Automatização**: Executa em loop contínuo, verificando o status a cada 5 minutos.

## Pré-requisitos

- Python 3.x
- Conta na Twitch (para obter Client ID e Secret)
- Projeto Firebase com Firestore habilitado
- Chave de serviço do Firebase (JSON)

## Configuração

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/produtoraindi768-afk/api-portalv.git
   cd api-portalv
   ```

2. **Instale as dependências**:
   ```bash
   pip install requests firebase-admin
   ```

3. **Configure as variáveis de ambiente**:
   - `TWITCH_CLIENT_ID`: Seu Client ID da Twitch
   - `TWITCH_CLIENT_SECRET`: Seu Client Secret da Twitch

   Você pode definir essas variáveis no seu sistema ou usar um arquivo `.env` com a biblioteca `python-dotenv`.

4. **Arquivo de chave do Firebase**:
   - O arquivo de chave de serviço do Firebase deve estar localizado em: `/etc/secrets/dashboard-f0217-firebase-adminsdk-fbsvc-afee65e5ba.json`
   - Certifique-se de que o arquivo está acessível e tem as permissões corretas.

## Como usar

Execute o script principal:
```bash
python api-portal.py
```

O script irá:
1. Conectar ao Firebase
2. Obter um token de acesso da Twitch
3. Verificar o status de todos os streamers na coleção "streamers" do Firestore
4. Atualizar o campo `isOnline` para cada streamer
5. Aguardar 5 minutos e repetir o processo

## Estrutura do Firestore

A coleção `streamers` deve conter documentos com pelo menos os seguintes campos:
- `streamUrl`: URL do canal da Twitch (ex: "https://twitch.tv/nome_do_canal")
- `isOnline`: Campo booleano que será atualizado automaticamente

## Contribuição

Sinta-se à vontade para contribuir com melhorias ou correções. Abra uma issue ou envie um pull request.

## Licença

Este projeto está sob a licença MIT.