# Cyberhack

<p align="center">
  <img src="https://github.com/YuriyAgapov/cyberhack/blob/master/media/cyberhack_preview.gif">
</p>

## Описание
Это мод для Cyberpunk 2077, который распознает на экране монитора миниигру "Взлом протокола" и подсвечивает оптимальный вариант решения головоломки.

## Установка
Для работы мода потребуется установить:
* Python 3.10 (https://www.python.org/downloads/)
* Tesseract-OCR (https://github.com/UB-Mannheim/tesseract/wiki)
* CyberEngineTweaks (https://wiki.redmodding.org/cyber-engine-tweaks/)

Установить переменные окружения:
* CMDS_FILENAME=path to Cyberpunk 2077\bin\x64\plugins\cyber_engine_tweaks\mods\clickmap.txt
* PATH=%PATH%;path to Tesseract-OCR

Содержимое cyberhack\ui поместить в <path to Cyberpunk 2077>\bin\x64\plugins\cyber_engine_tweaks\mods.

Запустить cyberhack_core.py.

Запустить игру.

## Как это работает?
Мод состоит из дву частей, сценария на python, которые решает головоломку и мод для CyberEngineTweaks - cyberhack-layer, которые отображает решение в внутриигровом оверлее.
Каждые 100 миллисекунд сценарий делает скриншет область экрана (~220x71) чтобы определить что началась мини игра. Частотой 
Когда началась минигра, сценарий делает полноэкранный скриншот и пытается распознать на нем матрицу символов и последовательности которые нужно ввести (размер буфера высчитывается по размеру его области).
Как только ему это удалось, он создает файл clickmap.txt, в котором записаны какие области и каким цветом необходимо подсветить.
cyberhack-layer считывает из файла области для подсветки и отображает их.
Помимо решения, отображаются все возможные последовательности (на всякий случай=)).

## Особенности
Курсор мыши мешает распознованию символов, по этому его необходимо уводить из зон распознавания, до тех пор пока не будет отображено решение. Как только решение найдено, сценарий переходит в пассивный режим и не реагирует на курсор.
Если решение не влезает в буфер, то решение отображается крысным цветом.
Сценарий может найти решение, если для этого необходимо ввести "мусорный" первый символ, но не более. Такой символ отображается синим цветом.
