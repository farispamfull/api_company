# api_company

Второй этап отбора на проект от яндекса фестиваль "Любимовка" (пройден)

## Новый функционал

Регистрация и вход проходят исключительно по email и password, обратно приходит токен:

 **Prefix:** api/auth/

 **registration/**

 **login/**

Создатель компании и те, кому он передал права, могут посмотреть всех у кого есть права:
на эту фирмы

**api/v1/company/<company_id>/access**

 * get 


```json
{
    "administrator": {
        "id": 0,
        "username": "string",
        "email": "string"
    },
    "delegate_persons": [
        {
            "id": 0,
            "username": "string",
            "email": "string"
        }
    ]
}
```

Добавить права может только создатель компании: 

 **api/v1/company/<company_id>/access**

* post

```json
{
    "email":"string" 
    
}
```

* delete

**api/v1/company/<company_id>/access/<user_id>**


Небольшое readme:
https://observant-kick-84c.notion.site/readme-ef4197a29f694c239d6ea3a6f484757f

# Тестовое задание

### Необходимо написать справочник-телефонную книгу организаций.

Справочник представляет собой API приложение(DFR) для поиска номеров телефонов и информации об организациях. Визуальное представление не требуется.

* Информация, хранимая об организации: адрес, название, описание и список сотрудников.
* У каждого сотрудника есть ФИО, должность и номера телефонов. 
* Номера телефонов могут быть различных типов: Рабочий, Личный, Факс. Хотя бы один телефон в справочнике должен быть обязательным. 
* Рабочие телефоны могу быть одинаковыми для нескольких сотрудников, но личные — нет. 
* Создать организацию с одинаковым названием нельзя. 
* Внутри одной организации не может быть сотрудников с одинаковыми ФИО, но они могут быть в разных организациях.
* Номера телефонов отображаются в формате +79161234567. Нужно учесть, что номера телефонов могут быть с разными кодами страны.
* Аутентификация реализована через email и пароль.
* Для вывода списка организаций, элементов поиска и сотрудников организации, всегда используем пагинатор. Стандартное количество элементов на всех страница — 10 штук, но пользователь может менять количество элементов.

### Общий интерфейс авторизованного и неавторизованного пользователя:
На главной странице API выводится список организаций в алфавитном порядке. 

 Приложение имеет поиск — одно поле, поиск осуществляется по названию организации, ФИО сотрудника и номеру телефона. В результатах поиска выводится название организации и первые 5 сотрудников, подходящих под условия поиска. Или просто название организации, если в ней нет сотрудников, подходящих под условия поиска. Если какого-то телефона нет, он не показывается. Примеры ответов ниже показывают ожидаемую иерархию данных.

#### Пример 1: строка поиска: Ива
**_Результаты:_**
* ООО Ромашка
    * Иванов Сергей Петрович (Инженер)
      * Факс: +74951234567
    * Басурман Иван Павлович (Бухгалтер)
      * Личный: +79161234567 
      * Факс: +74951234567
* ООО Василек
    * Цветкова Яна Ивановна (Программист)
      * Личный: +79161234567 
      * Факс: +74951234567
* ООО Гремучая ива
* И так далее

#### Пример 2: строка поиска: Металл
**_Результаты:_**
* ООО Заборы из металла
* ОГО Металлические нервы
* ОАО Металлург
* И так далее

Поиск представляет собой API вида `/search?q=Ива`

Со страницы результатов поиска должна быть вся необходимая информация для того, чтобы перейти на страницу организации.

При запросе конкретной организации выводится список сотрудников с их должностями и номерами телефонов, формат аналогичен формату выше.
Доступен поиск по номеру телефона, а также по ФИО и должности сотрудника в рамках организации, также в одном поле.

### Возможности авторизованного пользователя.
#### Обычный авторизованный пользователь может:
* Создавать организации
* Просмотреть список организаций, в которых он может изменять данные сотрудников.
* Добавлять и удалять сотрудников, редактировать их ФИО, должности и номера телефонов.

#### Создатель организации имеет дополнительные права:
* Предоставить по email доступ пользователю к редактированию организации. 
* Просмотреть список пользователей, которым доступно редактирование организации.
* Отозвать права на редактирование.
* Изменять информацию об организации: адрес, название и описание.

### Интерфейс суперпользователя (Django Admin).
Необходимо добавить все модели в джанго-админку, чтобы суперпользователь мог редактировать оттуда любую информацию.

## Разработка
* Создайте пустой репозиторий и работайте в нем, когда будете готовы — пришлите ссылку на репозиторий.
* Рекомендуем разбить проект на маленькие задачи и делать их поочередно, от меньшего к большему.
* Разрабатывать приложение необходимо средствами Django REST Framework.
* Необходимо описать README.md файл с инструкцией по запуску.
* Ключевые моменты: архитектура приложения и качество кода.
* Приветствуются любые дополнения к данному ТЗ, весь дополнительный функционал необходимо описать в README.md


