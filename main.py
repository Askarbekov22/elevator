class Elevator(object):

    def __init__(self, max_capacity=5):
        # Текущий этаж, на котором находится лифт
        self.cur_floor = 0.
        # DOT = Направление движения. Может быть «Вверх» или «Вниз».
        self.DOT = "Up"
        # Люди в лифте
        self.passengers_in_elevator_list = []
        # Устанавливает время начала на ноль
        self.cur_time = 0
        # Устанавливает максимальную вместимость лифта
        self.max_capacity = max_capacity
        # Подсчитывает количество людей, достигших пункта назначения
        self.happy_people = 0
        # Список всех людей, которые находятся в симуляции
        self.all_passenger_list = []
        # Пассажиры, которые ждут
        self.queue_list = []
        # сколько времени занимает событие... если установить значение 4, этот шаг займет на 4 секунды больше
        self.action_time = 0
        # в прошлый раз он проверил список пассажиров, чтобы увидеть, есть ли новые кнопки
        self.last_check = 0
        # Это чтобы узнать, какой верхний этаж
        self.top_floor = 0

    # Это выполняется один раз перед началом моделирования, чтобы установить время
    def set_cur_time(self, cur_time):
        self.cur_time = cur_time

    # Это выполняется один раз перед тем, как симуляция начнет создавать «список всех пассажиров»
    def set_all_passenger_list(self, all_passenger_list):
        self.all_passenger_list = all_passenger_list

    # Это выполняется один раз перед тем, как симуляция начнет создавать пустой "список пассажиров в лифте"
    def set_passengers_in_elevator_list(self):
        self.passengers_in_elevator_list = [None for i in range(len(self.all_passenger_list))]

    # Это выполняется один раз, прежде чем симуляция начнет устанавливать верхний_этаж, взятый из класса здания.
    def set_top_floor(self, top_floor):
        self.top_floor = top_floor

    #Это используется для совершения действия, например, когда кто-то заходит в лифт, требуется больше времени
    def update_time(self):
        return self.action_time

    # Это перемещает лифт на 0,25 этажа вверх в указанном направлении (подъем на один этаж занимает 2 секунды)
    def move(self, direction):
        if direction == "Up":
            self.cur_floor += 0.25
        else:
            self.cur_floor += -0.25

    # Метод, меняющий направление лифта
    def change_direction(self):
        if self.DOT == "Up":
            self.DOT = "Down"
        else:
            self.DOT = "Up"

    # Метод добавления пассажиров в лифт. Он принимает список пассажиров в качестве входных данных, и пассажиры, которые ждали больше всего, входят первыми, либо до тех пор, пока на этом этаже не останется людей, либо пока не будет достигнута максимальная вместимость лифта.
    def new_passenger(self, new_passengers_list):

        #динамический список, содержащий личности людей, ожидающих снаружи лифта и желающих войти
        identities_list_still_waiting = [i.identity for i in new_passengers_list]

        #статический список, содержащий личности всех людей, которые хотели попасть в лифт в начале
        identities_list_all_passengers = [i.identity for i in new_passengers_list]

        num_passengers_got_on = 0  # how many people got into the elevator
        identities_list_people_who_got_on = []  # a list of identities of the passengers that got on

        # Добавление новых пассажиров, пока еще есть пассажиры, желающие попасть и в лифте еще есть свободное место:
        while len(new_passengers_list) > num_passengers_got_on and len(
                [x for x in self.passengers_in_elevator_list if x is not None]) < self.max_capacity:
            num_passengers_got_on += 1  # one more person gets in the elevator

            #содержит личность входящего пассажира - пассажира с наименьшей идентификацией (ждал больше всего)
            id_passenger_gets_on = min(identities_list_still_waiting)

            #содержит индекс человека, который входит в identities_list_all_passengers
            index_of_passenger_in_identities_list_all_passengers = identities_list_all_passengers.index(
                id_passenger_gets_on)

            #содержит индекс человека, который входит в identities_list_still_waiting
            index_of_passenger_in_identities_list_still_waiting = identities_list_still_waiting.index(
                id_passenger_gets_on)

            #добавьте этого человека в лифт
            self.passengers_in_elevator_list[id_passenger_gets_on] = new_passengers_list[
                index_of_passenger_in_identities_list_all_passengers]

            #установите время встречи этого человека
            self.passengers_in_elevator_list[id_passenger_gets_on].set_pickup_time(self.cur_time)

            #добавить личность этого человека в список личностей пассажиров, которые должны попасть
            identities_list_people_who_got_on.append(id_passenger_gets_on)

            #удалить этого человека из identities_list_still_waiting
            del identities_list_still_waiting[index_of_passenger_in_identities_list_still_waiting]

        #удалить вставших пассажиров из списка queue_list
        indeces_to_delete_from_queue_list = []  # the indeces within the queue_list with the people who got on
        for element_in_queue_list in self.queue_list:

            #если идентификатор элемента в списке очереди есть и в списке идентификаторов вступивших:
            if element_in_queue_list[2] in identities_list_people_who_got_on:
                # добавляем этот индекс в indeces_to_delete_from_queue_list
                indeces_to_delete_from_queue_list.append(self.queue_list.index(element_in_queue_list))

        for index_to_delete_from_queue_list in range(len(indeces_to_delete_from_queue_list) - 1, -1, -1):
            #удаляем эти элементы из queue_list (удаляя в обратном порядке, чтобы не испортить индексацию)
            del self.queue_list[indeces_to_delete_from_queue_list[index_to_delete_from_queue_list]]

        # вывести предупреждение, если какой-то пассажир не может войти, потому что лифт был полон
        if len(new_passengers_list) > num_passengers_got_on:
            print(
            "Лифт ПОЛНЫЙ!!! Некоторые пассажиры не смогли войти!")

    # Метод, используемый пассажирами для выхода из лифта на желаемом этаже. Он принимает на вход список пассажиров, которые хотят выйти, и удаляет их из лифта.
    def passenger_exit(self, exit_passengers_list):

        #Места назначения всех пассажиров, которые должны выйти на этом этаже, должны быть на этом же этаже
        exit_destinations = [i.destination for i in exit_passengers_list]
        if exit_destinations != [self.cur_floor for i in range(len(exit_passengers_list))]:
            print(
            "Внимание!!! Некоторые пассажиры не хотят выходить на этом этаже!!!")
        else:
            for exit_passenger in exit_passengers_list:
                self.passengers_in_elevator_list[exit_passenger.identity].set_time_exited(
                    self.cur_time)  # set the time of drop off
            for exit_passenger in exit_passengers_list:
                self.passengers_in_elevator_list[
                    exit_passenger.identity] = None  # remove them from passengers_in_elevator_list

            #Эти люди теперь счастливы - они достигли желаемого пункта назначения
            self.happy_people += len(exit_passengers_list)

    # Этот метод используется для обновления «last_check», который используется для проверки того, нажимали ли люди кнопку лифта с момента последней проверки. Это важно, потому что некоторые действия (люди заходят в лифт) требуют времени, и если лифт проверяет только нажатия кнопок в текущий момент времени, он пропустит те действия, которые произошли между последней проверкой и текущим временем.
    def update_last_check(self):
        self.last_check = self.cur_time

    def simulation(self):
        # Каждый раз происходит небольшая логистика
        # Во-первых, он восстанавливает время действия по умолчанию
        global goal
        self.action_time = 0

        # Затем он обновляет список кнопок из списка действий, добавляя все действия с момента последней проверки
        for passenger in self.all_passenger_list:
            if passenger.time_appeared > self.last_check and passenger.time_appeared <= self.cur_time:
                self.queue_list.append([passenger.pickup_floor, passenger.direction, passenger.identity])
        self.update_last_check()

        # Тогда есть пара сценариев, в которых лифт может оказаться

        # Первый сценарий: в лифте нет людей и никто не ждет лифт,
        # и лифт ждет
        if len(self.queue_list) == 0 and self.passengers_in_elevator_list == [None for i in range(len(
                self.passengers_in_elevator_list))]:
            return "The elevator is waiting"

        #Следующее, если в лифте нет людей, но есть люди, ожидающие лифта.
        # В этом случае лифт движется к самому крайнему ожидающему его по ходу движения человеку.

        elif self.passengers_in_elevator_list == [None for i in range(len(self.passengers_in_elevator_list))]:
            if self.DOT == "Up":
                temp_goal = max(item[0] for item in self.queue_list)
                if temp_goal > self.cur_floor:
                    goal = temp_goal
                elif temp_goal < self.cur_floor:
                    self.change_direction()
                    goal = min(item[0] for item in self.queue_list)
                else:
                    goal = self.cur_floor
            elif self.DOT == "Down":
                temp_goal = min(item[0] for item in self.queue_list)
                if temp_goal < self.cur_floor:
                    goal = temp_goal
                elif temp_goal > self.cur_floor:
                    self.change_direction()
                    goal = max(item[0] for item in self.queue_list)
                else:
                    goal = self.cur_floor

        #Третий случай - в лифте люди. Лифт ставит своей целью максимально
        # экстремальное направление от людей в лифте.
        else:
            if self.DOT == "Up":
                goal = max(
                    passenger.destination for passenger in [i for i in self.passengers_in_elevator_list if i != None])
            else:  # self.DOT == "Down"
                goal = min(
                    passenger.destination for passenger in [i for i in self.passengers_in_elevator_list if i != None])

        #Это определяет, как лифт движется к своей цели
        print(
        "цель =", goal)
        if goal > self.cur_floor and self.DOT == "Up":
            self.move("Up")
        elif goal > self.cur_floor and self.DOT == "Down":
            self.DOT = "Up"
            self.move("Up")
        elif goal < self.cur_floor and self.DOT == "Down":
            self.move("Down")
        elif goal < self.cur_floor and self.DOT == "Up":
            self.DOT = "Down"
            self.move("Down")
        elif goal == self.cur_floor:
            self.change_direction()

        #Если человек находится в лифте на своем этаже, он должен выйти
        getting_off = []
        for i in range(0, len(self.passengers_in_elevator_list)):
            if self.passengers_in_elevator_list[i] != None:
                if self.cur_floor == self.passengers_in_elevator_list[i].destination:
                    getting_off.append(self.passengers_in_elevator_list[i])
                    # self.passengers_in_elevator_list[i] = Нет
                    # Двери лифта открываются и закрываются за 4 секунды. В это время люди входят и выходят, поэтому, если один пассажир входит или выходит, действие займет 4 секунды.
                    self.action_time = 4
        print(
        "выходят", [i.identity for i in getting_off])
        self.passenger_exit(getting_off)

        #Если человек находится на том же уровне, что и лифт, и он движется в направлении его движения, он должен войти
        getting_on = []
        for i in range(0, len(self.queue_list)):
            if (self.cur_floor == self.queue_list[i][0] and self.DOT == self.queue_list[i][1]):
                getting_on.append(self.all_passenger_list[self.queue_list[i][2]])
                self.action_time = 4
        self.new_passenger(getting_on)

        print(
        "Список очереди", self.queue_list)
        print(
        "Текущий этаж =", self.cur_floor)
        print(
        "Пассажир в лифте=", [i.identity for i in self.passengers_in_elevator_list if i != None])
        print(
        "Счастливые люди) =", self.happy_people)

    def simulation_2(self):
        self.action_time = 0
        """ Пример стратегии. Начинается снизу, движется вверх, движется вниз, подбирая людей, когда идет их ТОЧКА """
        for passenger in self.all_passenger_list:
            if passenger.time_appeared > self.last_check and passenger.time_appeared <= self.cur_time:
                self.queue_list.append([passenger.pickup_floor, passenger.direction, passenger.identity])
        self.update_last_check()

        # Двигайтесь в правильном направлении, сначала вверх, затем вниз

        if self.DOT == "Up" and self.cur_floor != self.top_floor:
            self.move("Up")
        elif self.DOT == "Down" and self.cur_floor != 0:
            self.move("Down")
        elif self.DOT == "Up" and self.cur_floor == self.top_floor:
            self.change_direction()
        elif self.DOT == "Down" and self.cur_floor == 0:
            self.change_direction()

        getting_off = []
        for i in range(0, len(self.passengers_in_elevator_list)):
            if self.passengers_in_elevator_list[i] != None:
                if self.cur_floor == self.passengers_in_elevator_list[i].destination:
                    getting_off.append(self.passengers_in_elevator_list[i])
                    # self.passengers_in_elevator_list[i] = None
                    self.action_time = 4
        self.passenger_exit(getting_off)

        getting_on = []
        for i in range(0, len(self.queue_list)):
            if (self.cur_floor == self.queue_list[i][0] and self.DOT == self.queue_list[i][1]):
                getting_on.append(self.all_passenger_list[self.queue_list[i][2]])
                self.action_time = 4
        self.new_passenger(getting_on)

        print(
        "выходят", [i.identity for i in getting_off])
        print(
        "Список очереди", self.queue_list)
        print(
        "Текущий этаж=", self.cur_floor)
        print(
        "Пассажиры в лифте =", [i.identity for i in self.passengers_in_elevator_list if i != None])
        print(
        "Счастливые люди=", self.happy_people)


from random import randint


class Passenger(object):
    #пассажиры имеют основные атрибуты того, сколько времени это заняло, где они находятся, куда они хотят пойти, и удостоверение личности
    def __init__(self, time_appeared=0., destination=1, pickup_floor=0, identity=0):
        self.pickup_floor = pickup_floor
        self.time_appeared = time_appeared
        self.time_exited = 0.
        self.destination = destination
        self.pickup_time = 0.
        self.identity = identity
        self.direction = "Up" if (self.destination - self.pickup_floor) > 0 else "Down"

    def set_time_exited(self, time_exited):
        self.time_exited = time_exited

    def set_pickup_time(self, pickup_time):
        self.pickup_time = pickup_time

    def get_pickup_time(self):
        return self.pickup_time

    def get_time_exited(self):
        return self.time_exited

    def get_time_appeared(self):
        return self.time_appeared

    def get_destination(self):
        return self.destination


class Building(object):
    # В каждом здании есть распределение людей, которые будут отобраны для создания пассажиров, а также
    # общее количество пассажиров и количество этажей
    def __init__(self, distribution_of_people, total_num_passengers):
        self.distribution_of_people = distribution_of_people
        self.floors = len(distribution_of_people)
        self.total_num_passengers = total_num_passengers

    def get_floors(self):
        return self.floors

    def get_distribution(self):
        return self.distribution_of_people

    def get_total_num_passengers(self):
        return self.total_num_passengers

    # ______ NEW CELL ____


import random
import numpy as np

result_5 = []

random.seed(1)
np.random.seed(1)

# Чтобы смоделировать 10 раз, мы создаем внешний цикл while
counter = 0
sims_10 = []

while counter < 10:

    # Создание Здания, которое называется Дома (название нашей резиденции в Хайдарабаде).
    # distribution_of_people говорит нам, что вероятность того, что человек поедет на 0-й этаж или с него, будет в 6 раз выше, чем на любой другой этаж. Кроме того, существует одинаковая вероятность того, что человек поедет на/с i-го этажа по сравнению с j-м этажом, когда i и j положительны.
    At_Home = Building(
        distribution_of_people=[220, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                                10], total_num_passengers=20)

    num_floors = At_Home.get_floors()
    distribution = At_Home.get_distribution()
    num_passengers = At_Home.get_total_num_passengers()

    #Нормализовать распределение. Теперь он содержит вероятности.
    distribution = [float(distribution[i]) / sum(distribution) for i in range(len(distribution))]

    # Пример мест выдачи в соответствии с распределением
    pickup_locations = np.random.choice(range(num_floors), num_passengers, p=distribution)

    #Чтобы сэмплировать пункты назначения, мы должны убедиться, что мы удаляем этаж выдачи из пространства возможностей, но при этом сохраняем свойства распределения.
    destinations = []
    for index_passenger in range(num_passengers):
        #Это будет новое распределение после того, как мы удалим элемент, соответствующий полу посадки пассажира.
        distribution_without_passenger = [a for a in distribution]

        #Это будет новый диапазон возможных этажей после того, как мы удалим этаж посадки пассажира
        range_without_passenger = list(range(num_floors))

        #Удаление этажа пикапа
        del range_without_passenger[pickup_locations[index_passenger]]

        #Удаление элемента в раздаче, соответствующего этажу выдачи
        del distribution_without_passenger[pickup_locations[index_passenger]]

        #Нормализация распределения, чтобы оно снова содержало вероятности
        distribution_without_passenger = [float(distribution_without_passenger[i]) / sum(distribution_without_passenger)
                                          for i in range(len(distribution_without_passenger))]

        #Выбираем желаемое направление из новой линейки этажей и нового распределения
        destinations.append(np.random.choice(range_without_passenger, 1, p=distribution_without_passenger)[0])

    # delays — это список, который сообщает нам, сколько времени проходит между прибытием двух последовательных пассажиров.
    # Мы хотим, чтобы задержки были распределены таким образом, чтобы небольшая часть задержек была равна нулю.

    # Во-первых, мы вводим среднюю задержку, которую хотим:
    average_delay = 40.0


    # Мы выбираем задержки из распределения Пуассона, центр которого в десять раз превышает среднюю задержку.
    # Затем мы удаляем из результата девятикратную среднюю задержку, эффективно сдвигая распределение Пуассона влево.
    #В результате часть раздачи попадает в отрицательные числа. Любые выборки из этой части считаются нулевыми.
    delays = np.random.poisson(lam=10 * average_delay, size=num_passengers - 1)
    delays = [(i - 9 * average_delay) * ((i - 9 * average_delay) > 0) for i in delays]

    #Первый человек всегда приходит на третьей секунде с начала симуляции
    times_of_arrival = [3.]

    #Добавление времени прибытия всех пассажиров в список
    for i in range(num_passengers - 1):
        times_of_arrival.append(times_of_arrival[i] + delays[i])

    #Создание списка пассажиров на основе времени их прибытия, этажа посадки и этажа назначения. У каждого пассажира есть идентификатор, который присваивается в соответствии с порядком прибытия. Таким образом, пассажиры с меньшими удостоверениями личности прибыли раньше.
    passenger_list = []
    for i in range(num_passengers):
        passenger_list.append(
            Passenger(time_appeared=times_of_arrival[i], destination=destinations[i], pickup_floor=pickup_locations[i],
                      identity=i))

    #Установка текущего времени
    cur_time = 0.

    #Создание лифта
    elevator = Elevator()
    elevator.set_all_passenger_list(passenger_list)
    elevator.set_passengers_in_elevator_list()
    elevator.set_top_floor(num_floors - 1)

    # Печать деталей симуляции
    print(
    "Время появления:", [i.time_appeared for i in passenger_list])
    print(
    "Подобран с этажа:", [i.pickup_floor for i in passenger_list])
    print(
    "Направления:", [i.destination for i in passenger_list])
    print(
    "IDs:", [i.identity for i in passenger_list])

    #Это основной цикл while для симуляции (если симуляция запущена только один раз, это единственный необходимый цикл while)
    while num_passengers != elevator.happy_people:
        #Показать текущее время до лифта
        elevator.set_cur_time(cur_time)

        #Вызов метода моделирования. Он работает с .simulation() или .simulation_2().
        elevator.simulation_2()

        # Обновление текущего времени на основе того, что произошло в этом раунде симуляции
        cur_time += elevator.update_time()

        # Полсекунды проходят в каждом раунде, несмотря ни на что
        cur_time += 0.5

        #Распечатка текущего времени
        print(
        "Текущее время:", cur_time)

    counter += 1
    sims_10.append(passenger_list)

results_5 = sims_10



# This can be run to get a summary of results for a run of the simulation
import numpy as np


#Это можно запустить, чтобы получить сводку результатов запуска симуляции
def results(lis, name):
    print(
    "Среднее время от", name, sum(lis) / float(len(lis)))
    print(
    "Максимальное время от»", name, max(lis))
    print(
    "медиану времени от", name, np.median(np.array(lis)))
    print(
    "__________\n")



# Это основная функция результатов, она принимает список длиной 100 и выводит соответствующие результаты
# Мы запускаем эту функцию для 8 списков из 100, содержащихся в списке результатов.

def print_results(simulation_10_list, label):
    pushing_to_arrival = []
    wait_for_elevator = []
    wait_in_elevator = []

    for j in range(0, len(simulation_10_list)):
        for i in simulation_10_list[j]:
            wait_for_elevator.append(i.get_pickup_time() - i.get_time_appeared())
            wait_in_elevator.append(i.get_time_exited() - i.get_pickup_time())
            pushing_to_arrival.append(i.get_time_exited() - i.get_time_appeared())

    print(
    label)
    print(
    "Показатели эффективности:")
    print(
    "__________\n")


    results(wait_for_elevator, "начали подниматься в лифте:")
    results(wait_in_elevator, "вход в лифт до места назначения:")
    results(pushing_to_arrival, "нажатие кнопки, чтобы добраться до пункта назначения:")

