# Chat Criptografado com RSA em Python

Este projeto implementa uma aplicação de chat bidirecional em tempo real utilizando *sockets* TCP e criptografia assimétrica RSA implementada nativamente sem bibliotecas externas.

---

## Estrutura do Projeto

O projeto é composto por três arquivos Python principais:

* **`rsa_core.py`**: Módulo central de criptografia com algoritmos matemáticos e utilitários do RSA.
  * `is_prime_number(n)`: Testa se um número inteiro é primo.
  * `generate_prime(min_value, max_value)`: Gera números primos aleatórios dentro do intervalo especificado por amostragem de rejeição (*Monte Carlo*).
  * `mdc(a, b)`: Calcula o Máximo Divisor Comum entre dois inteiros através do Algoritmo de Euclides.
  * `mod_inverse(a, m)`: Obtém o inverso multiplicativo modular.
  * `generate_rsa_key_pair()`: Gera um par de chaves RSA (pública e privada) a partir de primos entre $5000$ e $10000$, garantindo que o módulo $n > \text{0xFFFFFF}$.
  * `encrypt(key, msg)`: Codifica a mensagem em UTF-8, divide em blocos de 3 bytes e cifra cada bloco com a fórmula $c = m^e \pmod n$.
  * `decrypt(key, msg)`: Decifra os blocos com $m = c^d \pmod n$ e os reconverte para a *string* UTF-8 original.
  * `key_to_string(key)` / `string_to_key(key)`: Realiza a serialização das chaves no formato `"e,n"` ou `"d,n"` para envio na rede.

* **`chat_server.py`**: Implementação do servidor de chat.
  * Cria o *socket* TCP configurado no endereço `127.0.0.0` e porta `3334`.
  * Gera seu par de chaves RSA e realiza a troca de chaves públicas com o cliente conectado.
  * Executa uma *thread* assíncrona (`receive_message`) para receber, decifrar e exibir mensagens do cliente.
  * Lê o terminal do usuário, cifra a mensagem digitada com a chave pública do cliente e realiza o envio.

* **`chat_client.py`**: Implementação do cliente de chat.
  * Conecta ao servidor TCP no endereço `127.0.0.0` e porta `3334`.
  * Gera seu par de chaves RSA e efetua o *handshake* de chaves públicas com o servidor.
  * Utiliza uma *thread* assíncrona em segundo plano para receber e decifrar as mensagens do servidor.
  * Lê a entrada do usuário, cifra os dados com a chave pública do servidor e envia.

---

## Requisitos

* Python 3.10 ou superior.
* Apenas módulos da biblioteca padrão do Python (`socket`, `threading`, `random`) são utilizados.

---

## Como Executar

Siga os passos abaixo em dois terminais distintos para rodar a aplicação:

### 1. Iniciar o Servidor
No primeiro terminal, execute o script do servidor:

```bash
python chat_server.py
```

O servidor iniciará, gerará suas chaves e ficará aguardando a conexão de um cliente na porta `3334`.

### 2. Iniciar o Cliente
No segundo terminal, execute o script do cliente:

```bash
python chat_client.py
```

Após a conexão ser estabelecida, ambos os lados realizarão a troca das chaves públicas automaticamente.

### 3. Enviar Mensagens
* Digite sua mensagem no terminal do cliente ou do servidor e pressione `Enter`.
* O destinatário exibirá tanto a mensagem criptografada recebida pela rede quanto a mensagem decifrada em texto limpo.
* Para encerrar a sessão em qualquer uma das pontas, digite `quit` e pressione `Enter`.

---

## Fluxo de Criptografia e Mensagens

1. **Handshake de Chaves**:
   * O cliente envia sua chave pública para o servidor no formato `"e,n"`.
   * O servidor responde enviando sua chave pública no mesmo formato.
2. **Cifragem e Transmissão**:
   * O remetente converte o texto em blocos de bytes, aplica a exponenciação modular com a chave pública do receptor e envia os inteiros cifrados separados por espaço.
3. **Decifragem**:
   * O receptor pega a cadeia de inteiros cifrados, aplica sua chave privada e reconstrói o texto UTF-8 original na *thread* de escuta em segundo plano.