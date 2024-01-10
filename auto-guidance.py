import cv2
import RPi.GPIO as GPIO
import time

# Настройка GPIO для двигателей
GPIO.setmode(GPIO.BCM)
# Установите номера GPIO для двигателей
STEP_X_PIN = 17
DIR_X_PIN = 18
STEP_Y_PIN = 22
DIR_Y_PIN = 23

# Инициализация GPIO
GPIO.setup(STEP_X_PIN, GPIO.OUT)
GPIO.setup(DIR_X_PIN, GPIO.OUT)
GPIO.setup(STEP_Y_PIN, GPIO.OUT)
GPIO.setup(DIR_Y_PIN, GPIO.OUT)

# Функции для управления двигателями
def move_x(direction, steps):
    # Установка направления движения по оси X
    GPIO.output(DIR_X_PIN, direction)

    # Генерация шагов по оси X
    for _ in range(steps):
        GPIO.output(STEP_X_PIN, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(STEP_X_PIN, GPIO.LOW)
        time.sleep(0.01)

def move_y(direction, steps):
    # Установка направления движения по оси Y
    GPIO.output(DIR_Y_PIN, direction)

    # Генерация шагов по оси Y
    for _ in range(steps):
        GPIO.output(STEP_Y_PIN, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(STEP_Y_PIN, GPIO.LOW)
        time.sleep(0.01)

# Открытие камеры
cap = cv2.VideoCapture(0)

try:
    while True:
        # Захват кадра с камеры
        ret, frame = cap.read()
        if not ret:
            break

        # Преобразование изображения в оттенки серого
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Настройка фильтров или алгоритмов для обнаружения мишени с использованием OpenCV

        # Получение координат центра мишени (в данном случае, просто пример)
        target_x, target_y = 320, 240

        # Расчет разницы между текущим положением и целевым
        diff_x = target_x - current_x_position
        diff_y = target_y - current_y_position

        # Перемещение по осям X и Y
        move_x(1 if diff_x > 0 else 0, abs(diff_x))
        move_y(1 if diff_y > 0 else 0, abs(diff_y))

        # Обновление текущего положения
        current_x_position = target_x
        current_y_position = target_y

        # Отображение изображения с меткой центра мишени
        cv2.circle(frame, (target_x, target_y), 10, (0, 255, 0), -1)
        cv2.imshow('Target Tracking', frame)

        # Выход из цикла при нажатии клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Освобождение ресурсов и выход из программы
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
