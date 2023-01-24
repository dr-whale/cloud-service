<?php

use yii\db\Migration;

/**
 * Handles the creation of table `{{%new}}`.
 */
class m230113_145554_create_new_table extends Migration
{
    /**
     * {@inheritdoc}
     */
    public function safeUp()
    {
        $this->createTable('weather', [
            'request_date' => $this->timestamp(),
            'forecast_date' => $this->timestamp(),
            'temperature' => $this->string(30),
            'condition' => $this->string(30),
        ]);
    }

    /**
     * {@inheritdoc}
     */
    public function safeDown()
    {
        $this->dropTable('{{%new}}');
    }
}
