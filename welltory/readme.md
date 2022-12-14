# Тестовое задание на вакансию Data Analyst в Welltory

## Исходные данные

Они представляют собой .csv файл с 4 столбцами:
- time_start_local — начало временного интервала
- time_end_local — конец временного интервала
- time_offset — сдвиг часового пояса в секундах относительно UTC
- steps — количество шагов, которые прошел пользователь во время этого временного интервала

В файле примерно месячные данные одного пользователя Welltory (мы получили его прямое разрешение на публикацию данных). Мы верим, что их будет достаточно для приемлемого решения задачи.

## Общая задача

Придумать алгоритм, который бы находил в данных такого типа прогулки. Понятие «прогулка» формально не определено, но мы представляем себе, что это примерно постоянная ходьба как минимум в течение 5 минут. Алгоритм нужно реализовать на языке python (версии 3.10 или более ранней).

## Ожидаемый результат 

Архив со следующими 4 файлами:
- requirements.txt — перечисление зависимостей
- walkings.py — файл с функцией find_walkings(data: pandas.DataFrame) -> dict, которая возвращает словарь вида: 
{
  “<день в формате yyyy-mm-dd>”: [  # список прогулок в этот день
    {
            “start”: “<начало прогулки в формате yyyy-mm-dd HH:MM:SS>”,
            “end”: “<конец прогулки в формате yyyy-mm-dd HH:MM:SS>”,
            “steps”: <количество шагов во время прогулки типа int>
        },
        …
    ]
}
- walkings.json — файл с результатами запуска функции find_walkings на предложенных данных
- walkings.ipynb — jupyter файл с EDA и описанием того, как вы пришли к решению

## Что мы будем оценивать

Формальную сторону решения: функция find_walkings должна выдавать адекватный ответ на предложенных данных
Полноту исследования данных
Качество оформления ваших рассуждений
