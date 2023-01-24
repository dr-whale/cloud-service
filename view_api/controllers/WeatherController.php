<?php

namespace app\controllers;

use yii\web\Controller;
use app\models\Weather;

class WeatherController extends Controller
{
    public function actionIndex()
    {
        $query = Weather::find();

        $weather = $query->orderBy('forecast_date')->all();

        return $this->render('index', ['weather' => $weather]);
    }
}