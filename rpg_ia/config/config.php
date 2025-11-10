<?php

$CONFIG = [
    'gemini' => [
        'api_key' => getenv('GEMINI_API_KEY') ?: '',
        'endpoint' => getenv('GEMINI_ENDPOINT') ?: '',
    ],
];

$local = __DIR__ . '/local.php';
if (file_exists($local)) {
    $c = include $local;
    if (is_array($c)) {
        $CONFIG = array_replace_recursive($CONFIG, $c);
    }
}
return $CONFIG;