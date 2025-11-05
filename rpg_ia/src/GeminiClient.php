<?php
namespace App\Service;

class GeminiClient
{
    private $apiKey;
    private $endpoint;

    public function __construct(array $cfg = [])
    {
        $this->apiKey = $cfg['api_key'] ?? null;
        $this->endpoint = $cfg['endpoint'] ?? null;
        $this->accessToken = $cfg['access_token'] ?? null;
    }

    public function sendMessage(string $message): string
    {
        // modo simulado
        if (empty($this->apiKey) && empty($this->endpoint) && empty($this->accessToken)) {
            return "Mestre (simulado): " . substr($message, 0, 800);
        }

        $url = $this->endpoint;
        if (!empty($this->apiKey)) {
            $url .= (strpos($url, '?') === false ? '?' : '&') . 'key=' . urlencode($this->apiKey);
        }

        $payload = json_encode(['input' => $message]);

        $headers = [
            'Accept: application/json',
            'Content-Type: application/json',
        ];
        if (!empty($this->accessToken)) {
            $headers[] = 'Authorization: Bearer ' . $this->accessToken;
        }

        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
        curl_setopt($ch, CURLOPT_TIMEOUT, 30);

        $resp = curl_exec($ch);
        $err = curl_error($ch);
        $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($resp === false || $err) {
            return "Erro na requisição: " . ($err ?: 'sem resposta');
        }

        // se veio HTML (404 do provedor) devolve mensagem clara para debugging
        if (stripos($resp, '<!doctype') !== false || stripos($resp, '<html') !== false) {
            return "Erro: endpoint retornou HTML (HTTP code: {$code}). Verifique a URL/rota do endpoint e se a autenticação está correta.";
        }

        $data = json_decode($resp, true);
        if (is_array($data)) {
            if (isset($data['output'])) return (string)$data['output'];
            if (isset($data['response'])) return (string)$data['response'];
            if (isset($data['choices'][0]['text'])) return (string)$data['choices'][0]['text'];
            if (isset($data['candidates'][0]['content'][0]['text'])) return (string)$data['candidates'][0]['content'][0]['text'];
            if (isset($data['message']['content'])) return (string)$data['message']['content'];
            if (isset($data['error'])) return "API error: " . json_encode($data['error']);
        }

        return (string)$resp;
    }
}