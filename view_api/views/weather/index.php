<?php
use yii\helpers\Html;
?>

<h1>Forecasts</h1>
<ul>
<?php foreach ($weather as $value): ?>
    <li>
        Request date: <?= $value->request_date ?><br>
        Forecast date: <?= $value->forecast_date ?><br>
        Temperature: <?= $value->temperature ?><br>
        Condition: <?= $value->condition ?>
    </li>
<?php endforeach; ?>
</ul>
