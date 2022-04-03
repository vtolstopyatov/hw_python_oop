from dataclasses import dataclass
from typing import ClassVar, Tuple, List, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        msg = (f'Тип тренировки: {self.training_type}; '
               f'Длительность: {"{:.3f}".format(self.duration)} ч.; '
               f'Дистанция: {"{:.3f}".format(self.distance)} км; '
               f'Ср. скорость: {"{:.3f}".format(self.speed)} км/ч; '
               f'Потрачено ккал: {"{:.3f}".format(self.calories)}.')
        return msg


@dataclass
class Training:
    """Базовый класс тренировки."""

    M_IN_KM: ClassVar[float] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    HOUR_IN_MIN: ClassVar[float] = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed = self.get_distance() / self.duration
        return avg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Определите get_spent_calories'
                                  f' в {self.__class__.__name__}.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        msg_bck = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return msg_bck


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self):
        coeff_calorie_1: float = 18
        coeff_calorie_2: float = 20
        calorie_result = ((coeff_calorie_1 * self.get_mean_speed()
                          - coeff_calorie_2) * self.weight / self.M_IN_KM
                          * self.duration * self.HOUR_IN_MIN)
        return calorie_result


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float

    def get_spent_calories(self):
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        calorie_result = ((coeff_calorie_1 * self.weight
                          + (self.get_mean_speed()**2 // self.height)
                          * coeff_calorie_2 * self.weight)
                          * self.duration * self.HOUR_IN_MIN)
        return calorie_result


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38

    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: float = 2
        calorie_result = ((self.get_mean_speed() + coeff_calorie_1)
                          * coeff_calorie_2 * self.weight)
        return calorie_result


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    package_dict: Dict[str, Type[Training]] = {'RUN': Running,
                                               'SWM': Swimming,
                                               'WLK': SportsWalking, }
    new_object = package_dict[workout_type](*data)
    return new_object


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List[Tuple[str, List[float]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
