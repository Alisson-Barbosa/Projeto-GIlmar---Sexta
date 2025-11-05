<?php
session_start();
header('Content-Type: application/json; charset=utf-8');
ini_set('display_errors', 0);
error_reporting(E_ALL);

require_once __DIR__ . '/GeminiClient.php';
$config = require __DIR__ . '/config.php';

try {
    // Lê entrada JSON
    $input = json_decode(file_get_contents('php://input'), true);
    $message = trim($input['message'] ?? '');

    if ($message === '') {
        echo json_encode(['success' => false, 'error' => 'Mensagem vazia.']);
        exit;
    }

    // Inicializa sessão
    if (!isset($_SESSION['messages'])) {
        $_SESSION['messages'] = [];
    }

    $_SESSION['messages'][] = ['role' => 'user', 'text' => $message];

    $client = new GeminiClient(
        $config['gemini']['api_key'],
        $config['gemini']['endpoint']
    );

    $reply = $client->sendMessage($message);

    // Garante que o retorno seja string
    if (!is_string($reply)) {
        $reply = json_encode($reply, JSON_UNESCAPED_UNICODE);
    }

    $_SESSION['messages'][] = ['role' => 'assistant', 'text' => $reply];

    echo json_encode([
        'success' => true,
        'messages' => $_SESSION['messages']
    ], JSON_UNESCAPED_UNICODE);

} catch (Throwable $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ], JSON_UNESCAPED_UNICODE);
}
