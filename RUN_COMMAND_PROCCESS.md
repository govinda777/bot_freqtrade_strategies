
# Run Command Process

Essa documentação tem como objetivo mostrar que o Freqtrade apenas iniciará uma Execução caso aconteça uma transação no Smart Contract.

## 🔐 Visão Geral do Fluxo Seguro

### 1. **Cliente envia transação ao Smart Contract**
- Inclui:
  - Valor (ETH ou token)
  - Mensagem criptografada com a **chave pública do contrato** (ou da API backend que lê o contrato)

---

### 2. **Mensagem criptografada com a chave pública**
A mensagem (por exemplo: `"buy BTCUSDT 50%"`) é criptografada fora do blockchain:

```js
// Supondo que o smart contract tenha uma chave pública associada
const EthCrypto = require('eth-crypto');

const publicKey = '0x04abc123...'; // Chave pública do Smart Contract / Backend

const encrypted = await EthCrypto.encryptWithPublicKey(
  publicKey,
  "buy BTCUSDT 50%"
);

const encryptedString = EthCrypto.cipher.stringify(encrypted);

// Esse encryptedString será enviado como parâmetro na transação
```

---

### 3. **Smart Contract recebe o valor + mensagem criptografada**
O contrato apenas armazena (ou emite evento) com o conteúdo criptografado.

```solidity
event EncryptedCommand(address indexed from, string encryptedMessage);

function deposit(string calldata encryptedMessage) external payable {
    require(msg.value > 0, "Need to send value");
    emit EncryptedCommand(msg.sender, encryptedMessage);
}
```

---

### 4. **API backend escuta o evento ou consulta o contrato**
A API, rodando com a **chave privada correspondente**, pega a mensagem e descriptografa:

```js
const privateKey = '...'; // Chave privada que corresponde à pública usada na criptografia
const parsed = EthCrypto.cipher.parse(encryptedString);

const decrypted = await EthCrypto.decryptWithPrivateKey(privateKey, parsed);
console.log("Mensagem:", decrypted); // => "buy BTCUSDT 50%"
```

---

### 5. **API executa comando no Freqtrade**
A API processa a instrução recebida e faz o POST para o Freqtrade.

```js
const result = await axios.post("http://localhost:8080/api/v1/execute", {
  command: decrypted
});
```

---

### 6. **Resposta da Freqtrade define o destino da transação**
- Se sucesso:
  - Chama `accept()` no contrato (libera os fundos).
- Se erro:
  - Chama `rollback()` no contrato (devolve ao remetente).

---

## 🧠 Pontos Técnicos e Estratégicos

### ✅ Vantagens:
- Segurança: só a API com a chave privada pode ler os comandos.
- Flexibilidade: a lógica real está off-chain, mas o trigger e os fundos são on-chain.
- Transparência: todos veem que houve uma transação, mas **não sabem o conteúdo**.

---

### ⚠️ Cuidados:
- A **chave privada NUNCA** pode ser exposta (idealmente armazenada com HSM ou sistema seguro como AWS KMS).
- Mensagens longas precisam de compressão ou split (limite de `gas` para `calldata`).
- O contrato só deve armazenar o mínimo possível (ideal: emitir eventos).
