<?php
session_start();
session_unset();
session_destroy();
// Ajuste se necessário; para acessar via XAMPP use /RPG_IA/public/
header('Location: /RPG_IA/public/');
exit;