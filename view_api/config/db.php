<?php

return [
    'class' => 'yii\db\Connection',
    'dsn' => 'mysql:host='.env('DB_HOST', 'localhost').';dbname='.env('DB_NAME'),
    'username' => env('DB_USER', 'root'),
    'password' => env('DB_PASSWORD', 'mynewpassword'),
    'charset' => 'utf8',

    // Schema cache options (for production environment)
    //'enableSchemaCache' => true,
    //'schemaCacheDuration' => 60,
    //'schemaCache' => 'cache',
];
