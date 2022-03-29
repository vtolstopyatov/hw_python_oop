class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        msg = ('Тип тренировки: ' + self.training_type + '; '
               'Длительность: ' + "{:.3f}".format(self.duration) + ' ч.; '
               'Дистанция: ' + "{:.3f}".format(self.distance) + ' км; '
               'Ср. скорость: ' + "{:.3f}".format(self.speed) + ' км/ч; '
               'Потрачено ккал: ' + "{:.3f}".format(self.calories) + '.')
        return msg
    pass


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    HOUR_IN_MIN = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed = self.get_distance() / self.duration
        return avg_speed
        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        msg_bck = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return msg_bck
        pass


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self):
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        calorie_result = ((coeff_calorie_1 * self.get_mean_speed()
                          - coeff_calorie_2) * self.weight / self.M_IN_KM
                          * self.duration * self.HOUR_IN_MIN)
        return calorie_result
    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        calorie_result = ((coeff_calorie_1 * self.weight
                          + (self.get_mean_speed()**2 // self.height)
                          * coeff_calorie_2 * self.weight)
                          * self.duration * self.HOUR_IN_MIN)
        return calorie_result
    pass


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        calorie_result = ((self.get_mean_speed() + coeff_calorie_1)
                          * coeff_calorie_2 * self.weight)
        return calorie_result
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    package_dict = {'RUN': Running,
                    'SWM': Swimming,
                    'WLK': SportsWalking, }
    new_object = package_dict[workout_type](*data)
    return new_object
    pass


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
