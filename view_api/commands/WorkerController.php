<?php

namespace app\commands;

use app\models\Weather;
use Enqueue\AmqpLib\AmqpConnectionFactory;
use Interop\Amqp\AmqpQueue;
use yii\console\Controller;

class WorkerController extends Controller
{

    protected $amqpConfig;

    public function init()
    {
        parent::init();
        $this->amqpConfig = [
            'host' => env('RABBIT_HOST', 'localhost'),
            'port' => env('RABBIT_PORT', 5672),
            'user' => env('RABBIT_USER', 'guest'),
            'pass' => env('RABBIT_PASSWORD', 'guest'),
        ];
    }

    protected $connection = null;
    protected $consumer = null;
    protected $context = null;

    public function rabbitConnect()
    {
        $this->connection = new AmqpConnectionFactory($this->amqpConfig);
        $this->context = $this->connection->createContext();
        $this->context->setQos(0, 1, false);

        $queue = $this->context->createQueue('weather');
        $queue->addFlag(AmqpQueue::FLAG_DURABLE);

        $this->context->declareQueue($queue);

        echo ' [*] Waiting for messages. To exit press CTRL+C', "\n";

        return $this->consumer = $this->context->createConsumer($queue);
    }

    public function rabbitDisconnect()
    {
        $this->context->close();
    }

    public function actionRun()
    {
        $this->rabbitConnect();
        try {
            while (true) {
                if ($message = $this->consumer->receive()) {
                    $result = json_decode($message->getBody(), true);
                    $weather = new Weather();
                    $weather->request_date = date('Y-m-d H:i:s');
                    $weather->forecast_date = date('Y-m-d', strtotime($result['forecast_date']));
                    $weather->temperature = $result['temperature'];
                    $weather->condition = $result['condition'];
                    $weather->save();
                    $this->consumer->acknowledge($message);
                }
            }
        } catch (\Exception $e) {
            echo $e->getMessage();
        }
        $this->rabbitDisconnect();
    }
}