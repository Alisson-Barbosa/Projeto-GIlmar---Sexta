# 🧙‍♂️ Mestre de RPG — Fantasia Medieval (PHP + Gemini API)

Um projeto em **PHP** que transforma a inteligência artificial **Gemini** em um **Mestre de RPG de fantasia medieval**.  
O jogador interage com a IA em tempo real, que narra aventuras, descreve cenários e oferece escolhas imersivas.

---

## 🚀 Funcionalidades

- 🎭 A IA assume o papel de Mestre de RPG.
- 🧩 Mantém o histórico da campanha (memória de contexto).
- 💬 Interface simples para enviar e receber mensagens.
- 🪶 Narrativas curtas, misteriosas e cinematográficas.

---

## 🗂️ Estrutura do Projeto

```
📁 Campanha Automática/
│
├── GeminiClient.php       # Classe principal de conexão com a API Gemini
├── start.php              # Inicia a sessão e define o prompt inicial
├── send.php               # Envia mensagens do jogador e retorna respostas da IA
├── config.php             # Contém a API Key e endpoint
├── index.html             # Interface do jogador (frontend)
└── README.md              # Este arquivo 😄
```

---

## ⚙️ Configuração

### 1. Clonar o repositório
```bash
git clone --branch producao --single-branch https://github.com/Alisson-Barbosa/Projeto-GIlmar---Sexta.git
cd mestre-rpg
```

### 2. Configurar o arquivo `config.php`
Crie o arquivo `config.php` com sua **API Key do Gemini**:

```php
<?php
return [
    'api_key' => 'SUA_CHAVE_AQUI',
    'endpoint' => 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'
];
```
---

## 🧠 Como funciona

1. Ao iniciar a campanha, o sistema envia um **prompt base**:
   > “Você é o Mestre de uma campanha de RPG de fantasia medieval. Narre de forma envolvente..."

2. Cada mensagem do jogador é enviada ao modelo junto com o histórico da sessão.
3. A IA responde como o Mestre, mantendo a coerência da história e oferecendo escolhas narrativas.
4. O histórico é salvo em `$_SESSION`, garantindo continuidade da aventura.

---

## 💬 Exemplo de Interação

**Jogador:**  
> Entro na taverna e observo o ambiente.

**Mestre (IA):**  
> O cheiro de cerveja velha e lenha queimada domina o ar. Um homem encapuzado te observa do canto.  
>  
> 🔹 1. Abordá-lo.  
> 🔹 2. Ignorá-lo e pedir uma bebida.  
> 🔹 3. Procurar outro lugar para sentar.

---

## 🧩 Personalização

Você pode editar o **prompt base** no arquivo `GeminiClient.php`:
```php
private string $rpgPrompt = "
Você é o Mestre de uma campanha de RPG de fantasia medieval.
Narre de forma envolvente, com descrições curtas, misteriosas e cinematográficas.
Sempre ofereça de 2 a 3 escolhas interessantes ao final.
Mantenha a coerência da história anterior.
";
```

---

## 🧪 Teste localmente

Inicie um servidor PHP local:
```bash
php -S localhost:8000
```

Depois, acesse em seu navegador:
```
http://localhost:8000
```

---

## 🛠️ Tecnologias

- **PHP 8+**
- **cURL**
- **JSON**
- **API Gemini (Google AI)**
- **HTML + JS (frontend)**

---

## 🧝‍♀️ Colaboradores

- **Enrico de Almeida** 
- **Kawa Kinoshita**
- **Alisson Barbosa**
- **Leandro Henrique**
- **Matheus Luz**


---

## 📜 Licença

Este projeto é distribuído sob a licença **MIT**.  
Sinta-se livre para usar, modificar e expandir.

---

> _“O som da lareira estala, o vento sussurra lá fora... e o destino de sua aventura começa aqui.”_