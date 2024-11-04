# Домашние задание №2 (Архитектура кода)
## Постановка задачи
У нас есть онлайн аптека, которая позволяет покупать разные товары:

| **тип товара**                                                                                  | **необходимый уровень доступа**                                                                                                  |
|-------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| безрецептурные (в том числе простые товары вроде воды, которые к препаратам отношения не имеют) | доступны всем                                                                                                                    |
| рецептурные                                                                                     | доступны любому врачу, либо пользователю у которого есть рецепт                                                                  |
| специальные                                                                                     | доступны только для врачей конкретных специальностей (например, товары для анестезиологов можно продавать только анестизиологам) |

**Необходимо создать отдельный сервис проверки корзины.**

Перед валидацией необходимо определить категорию товара. Исходя из категории определить как его проверять.

Решение нужно реализовывать таким образом, что бы при добавлении нового вида товаров потребовалось сделать минимум модификаций в уже существующем коде.
Для этого нужно описать стратегии валидации товаров:
* проверка рецептурных товаров 
* проверка специальных товаров
* проверка простых товаров
### Исходные данные
Схема базы данных нарисована в [pharmacy_er.png](pharmacy_er.png), :warning: **настоятельно рекомендую начать с ее изучения** :warning:.
#### Пользователи
Пользователи относятся к двум категориям (Они лежат в разных таблицах с разными схемами):
1. обычные пользователи
2. врачи

Задача получения пользователя сводится к тому, что бы попытаться найти его в 1 источнике, если не вышло попытаться найти в другом источнике. Ищем либо пока не найдем, либо пока не проверим все источники. 

При разработке кода стоит учитывать потенциальное увеличение числа источников данных и типов пользователей.

_Определить кем является пользователь нужно реализуя какую то архитектурную хитрость и обосновать ее выбор - любую на свое усмотрение или не использовать вовсе но обосновать почему этого делать не стоит._

#### Товары
* Товары хранятся в разных таблицах 
  * определить где искать товар можно по типу (special/common/receipt)
* Рецепты для пользователей лежат в отдельной таблице.
* Список рецептов по пользователям реализован через промежуточную таблицу, связывающую рецептурные товары и пользователей. 
* В таблице специальных товаров описано к какой сфере они относятся (например, товары, доступные к покупке только хирургам).

Название категорий товаров:

| категория          | название |
|--------------------|----------|
| Безрецептурные     | common   |
| Специальные товары | special  |
| Рецептурные        | receipt  |

### Input
На вход приходит запрос типа GET, который содержит:

| имя параметра | тип                                    | комментарий                                                                   |
|---------------|----------------------------------------|-------------------------------------------------------------------------------|
| user_id       | Integer                                | id врача или пользователя (он сквозной, т.е уникальный в рамках всей системы) |
| item_id       | список строковых значений вида type_id | type - строковое описание типа товара, id - числовой идентификатор товара     |

:warning: При парсинге категории товара - приводить ее к нижнему регистру и возвращать в нижнем регистре.
### Гарантии
1. Гарантированно
    * валидность структуры товара - гарантируется
    * user_id - гарантированно int
2. Не гарантированно
    * валидность типа и идентификатора (может прилететь товар вида ab12_qwerty)
    * наличие user_id в базе
### Output
Список позиций по которым есть проблемы.
#### Структура ответа
200 OK
[{“item_id”: string, “problem”: string}]
##### itemId
Формат такой же как на входе, в нижнем регистре. 

* Если прилетел Common_123 - вернуть common_123
* Если с товаром все окей и с пользователем все окей - не нужно возвращать, в ответ вписываем только проблемные товары и их причины
##### problem
Для каждого вида ошибки использовать свой код ошибки в ответе.

| Ошибка                                                                             |    Код ответа  (problem)    |
|------------------------------------------------------------------------------------|:---------------------------:|
| Ошибка парсинга категории товара - категория не найдена, в этом случае id не важен |       WRONG_CATEGORY        |
| Ошибка парсинга id товара   (категория спарсилась правильно - но id кривой)        |    INCORRECT_ITEM_ID        |
| Товар не найден (тип пользователя не важен)                                        |       ITEM_NOT_FOUND        |
| Пользователь не найден, товар можно продать                                        |           NO_USER           |
| Пользователь не найден, товар рецептурный                                          |     NO_USER_NO_RECEIPT      |
| Пользователь не найден, товар специальный                                          |    NO_USER_SPECIAL_ITEM     |
| Пользователь найден, товар рецептурный, у пользователя нет рецепта                 |         NO_RECEIPT          |
| Пользователь найден, товар спец. назначения                                        |       ITEM_IS_SPECIAL       |
| Пользователь врач, товар специальный, но не совпал по сфере работы врача           | ITEM_SPECIAL_WRONG_SPECIFIC |

### Тесты
Написание тестов приветствуется и поощряется.
### Пример
#### Пример запроса
http://localhost:8080/check?user_id=123&item_id=special_26&item_id=common_25
#### Пример item_id
special_123
* special - тип 
* 123 - id

## Запуск приложения

### Требования

Необходимо, чтобы были установлены следующие компоненты:

- `Docker` и `docker-compose`
- `Python 3.12`
- `Poetry`

```commandline
poetry install
poetry shell
```
#### Cоздание таблицы в докере и заполнение данными.
````commandline
make db
````
Запуск приложения
````commandline
make run
````


Запуск тестов
````commandline
make test
````

