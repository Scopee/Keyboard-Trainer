# Приложение "Клавиатурный тренажёр"
Версия 1.0  
Автор: Худяков Степан

## Описание 
Приложение позволяет улучшить скорость и точность набора текстов на клавиатуре

## Консольная версия
Справка по запуску ```./trainer.py --help``` или ```./trainer.py -h```  
Пример запуска ```./trainer.py``` или ```./trainer.py -d DIRECTORY```, где ```DIRECTORY``` - путь до директории с вашими текстами

## Добавление текстов
Для того чтобы добавить текст, необходимо положить файл в формате txt в папку texts или указать путь до директории с текстами

## Добавление тэгов
После написание текста вы можете добавить к 
нему тег для того, чтобы затем выбирать не из случайных текстов, а из текстов с тегам
Также вы можете использовать утилиту ```tag_editor.py``` для редактирования тегов. 
Пример запуска: ```./tag_editor.py``` или ```./tag_editor.py -d DIRECTORY```, 
где ```DIRECTORY``` это путь до директории с текстами
