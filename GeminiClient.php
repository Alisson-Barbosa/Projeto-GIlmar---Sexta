<?php

class GeminiClient {
    private string $apiKey;
    private string $endpoint;

    // 🧙‍♂️ Prompt fixo (personalidade do Mestre)
    private string $rpgPrompt = "
Você é o Mestre de uma campanha de RPG de fantasia medieval.
Narre de forma envolvente, com descrições curtas e misteriosas.
Sempre apresente 2 a 3 escolhas para o grupo ao final de cada resposta.
";

    // 💾 Histórico da aventura
    private array $history = [];

    // 🌟 Introdução automática (quando o jogo começa)
    private string $introMessage = "
🌒 A noite cai sobre o vilarejo de Eldorim...
Dentro da Taverna do Corvo Cinzento, viajantes de todo o reino se reúnem.
Uma tempestade ruge lá fora. A porta se abre, e um mensageiro ensanguentado cai no chão, sussurrando:
'...eles... acordaram nas ruínas do castelo... o Sol Negro retornou...'

O taverneiro empalidece e tranca as janelas.
O destino do grupo começa aqui.

1️⃣ Seguir o homem até as ruínas.
2️⃣ Investigar a lenda do Sol Negro.
3️⃣ Ficar na taverna e observar os outros clientes.

O que vocês decidem fazer?
";

    public function __construct(string $apiKey, string $endpoint) {
        $this->apiKey = $apiKey;
        $this->endpoint = $endpoint;
    }

    // 🧩 Reinicia a aventura
    public function resetHistory(): void {
        $this->history = [];
    }

    // 🚀 Inicia automaticamente com o prompt de introdução
    public function startAdventure(): string {
        $this->resetHistory();
        $this->history[] = "Mestre: " . trim($this->introMessage);
        return trim($this->introMessage);
    }

    public function sendMessage(string $message): string {
        if (empty($this->apiKey)) {
            return "(Modo local) [Mestre de RPG] \"$message\" — resposta simulada.";
        }

        $url = rtrim($this->endpoint, '/') . '?key=' . urlencode($this->apiKey);

        $this->history[] = "Jogador: $message";
        $fullContext = $this->rpgPrompt . "\n\n" . implode("\n", $this->history);

        $payload = [
            'contents' => [
                [
                    'parts' => [
                        ['text' => $fullContext]
                    ]
                ]
            ]
        ];

        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
            CURLOPT_POSTFIELDS => json_encode($payload),
            CURLOPT_TIMEOUT => 20
        ]);

        $response = curl_exec($ch);
        $error = curl_error($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($error) throw new Exception("Erro cURL: $error");
        $data = json_decode($response, true);

        if (!isset($data['candidates'][0]['content']['parts'][0]['text'])) {
            throw new Exception("Resposta inesperada da API Gemini.");
        }

        $reply = $data['candidates'][0]['content']['parts'][0]['text'];
        $this->history[] = "Mestre: $reply";

        return $reply;
    }
}
