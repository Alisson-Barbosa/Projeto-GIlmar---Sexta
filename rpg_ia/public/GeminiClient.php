<?php

class GeminiClient {
    private string $apiKey;
    private string $endpoint;

    public function __construct(string $apiKey, string $endpoint) {
        $this->apiKey = $apiKey;
        $this->endpoint = $endpoint;
    }

    public function sendMessage(string $message): string {
        // Modo local (sem API Key configurada)
        if (empty($this->apiKey)) {
            return "(Modo local) Você disse: \"$message\". Aqui seria a resposta do modelo Gemini.";
        }

        $url = rtrim($this->endpoint, '/') . '?key=' . urlencode($this->apiKey);

        $payload = [
            'contents' => [
                [
                    'parts' => [
                        ['text' => $message]
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

        // Falha de rede ou erro de cURL
        if ($error) {
            throw new Exception("Erro na requisição cURL: $error");
        }

        // Verifica se a resposta é válida
        $data = json_decode($response, true);

        // Loga resposta crua se houver problema de JSON
        if ($data === null) {
            file_put_contents(__DIR__ . '/debug_gemini.log', "Resposta inválida da API:\n$response\n");
            throw new Exception("A API retornou uma resposta inválida (não é JSON). Veja 'debug_gemini.log'.");
        }

        // Tratamento de erro da API Gemini
        if (isset($data['error'])) {
            $msg = $data['error']['message'] ?? 'Erro desconhecido da API Gemini.';
            $code = $data['error']['code'] ?? $httpCode;
            file_put_contents(__DIR__ . '/debug_gemini.log', "Erro da API ($code): $msg\nResposta:\n$response\n");
            throw new Exception("Erro da API Gemini ($code): $msg");
        }

        // Verifica se o conteúdo esperado existe
        if (!isset($data['candidates'][0]['content']['parts'][0]['text'])) {
            file_put_contents(__DIR__ . '/debug_gemini.log', "Resposta inesperada:\n$response\n");
            throw new Exception("Resposta inesperada da API Gemini. Veja 'debug_gemini.log'.");
        }

        // Retorna texto gerado
        return $data['candidates'][0]['content']['parts'][0]['text'];
    }
}
