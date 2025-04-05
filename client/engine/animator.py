import json
import random
import glm
import math


class Animation:
    def __init__(self, keyframes, easing="linear"):
        self.easing = easing
        self.keyframes = sorted(filter(lambda x: not callable(x[1]), keyframes), key=lambda k: k[0])
        self.keyfuncs = list(filter(lambda x: callable(x[1]), keyframes))
        self.current_time = 0.0

        self.func = Animation.animation(self.easing)
        self.active = False

    def update(self):
        if not self.active:
            return
        self.current_time += 1/60

        for func in self.keyfuncs:
            if func[0] == int(self.current_time):
                func[1]()

        if self.current_time > self.keyframes[-1][0]:
            self.active = False

    def get_value(self):
        if not self.active:
            return self.keyframes[0][1]
        
        for i in range(len(self.keyframes) - 1):
            t1, v1 = self.keyframes[i]
            t2, v2 = self.keyframes[i + 1]
            
            if t1 <= self.current_time <= t2:
                alpha = (self.current_time - t1) / (t2 - t1)
                return glm.mix(v1, v2, self.func(alpha))
        
        return self.keyframes[-1][1]
    
    def reset(self):
        self.current_time = 0.0
        self.func = Animation.animation(self.easing)

    @staticmethod
    def animation(easing):
        funcs = {
            # Лінійна
            "linear": lambda alpha: alpha,

            # Квадратичні
            "ease_in_quad": lambda alpha: alpha ** 2,
            "ease_out_quad": lambda alpha: 1 - (1 - alpha) ** 2,
            "ease_in_out_quad": lambda alpha: 2 * alpha ** 2 if alpha < 0.5 else 1 - (-2 * alpha + 2) ** 2 / 2,

            # Кубічні
            "ease_in_cubic": lambda alpha: alpha ** 3,
            "ease_out_cubic": lambda alpha: 1 - (1 - alpha) ** 3,
            "ease_in_out_cubic": lambda alpha: 4 * alpha ** 3 if alpha < 0.5 else 1 - (-2 * alpha + 2) ** 3 / 2,

            # Синусоїдальні
            "ease_in_sine": lambda alpha: 1 - math.cos((alpha * math.pi) / 2),
            "ease_out_sine": lambda alpha: math.sin((alpha * math.pi) / 2),
            "ease_in_out_sine": lambda alpha: -(math.cos(math.pi * alpha) - 1) / 2,

            # Експоненційні
            "ease_in_expo": lambda alpha: 0 if alpha == 0 else 2 ** (10 * (alpha - 1)),
            "ease_out_expo": lambda alpha: 1 if alpha == 1 else 1 - 2 ** (-10 * alpha),
            "ease_in_out_expo": lambda alpha: (
                0 if alpha == 0 else 1 if alpha == 1 else
                2 ** (10 * (alpha * 2 - 1) - 1) / 2 if alpha < 0.5 else
                (2 - 2 ** (-10 * (alpha * 2 - 1))) / 2
            ),

            # Кругові (circular)
            "ease_in_circ": lambda alpha: 1 - math.sqrt(1 - alpha ** 2),
            "ease_out_circ": lambda alpha: math.sqrt(1 - (alpha - 1) ** 2),
            "ease_in_out_circ": lambda alpha: (
                (1 - math.sqrt(1 - (2 * alpha) ** 2)) / 2 if alpha < 0.5 else
                (math.sqrt(1 - (-2 * alpha + 2) ** 2) + 1) / 2
            ),

            # Пружні (elastic)
            "ease_in_elastic": lambda alpha: (
                0 if alpha == 0 else 1 if alpha == 1 else
                -2 ** (10 * (alpha - 1)) * math.sin((alpha - 1.1) * 5 * math.pi)
            ),
            "ease_out_elastic": lambda alpha: (
                0 if alpha == 0 else 1 if alpha == 1 else
                2 ** (-10 * alpha) * math.sin((alpha - 0.1) * 5 * math.pi) + 1
            ),
            "ease_in_out_elastic": lambda alpha: (
                0 if alpha == 0 else 1 if alpha == 1 else
                (-2 ** (10 * (2 * alpha - 1)) * math.sin((2 * alpha - 1.1) * 5 * math.pi)) / 2 if alpha < 0.5 else
                (2 ** (-10 * (2 * alpha - 1)) * math.sin((2 * alpha - 1.1) * 5 * math.pi)) / 2 + 1
            ),

            # Стрибкові (bounce)
            "ease_in_bounce": lambda alpha: 1 - funcs["ease_out_bounce"](1 - alpha),
            "ease_out_bounce": lambda alpha: (
                7.5625 * alpha * alpha if alpha < 1 / 2.75 else
                7.5625 * (alpha - 1.5 / 2.75) ** 2 + 0.75 if alpha < 2 / 2.75 else
                7.5625 * (alpha - 2.25 / 2.75) ** 2 + 0.9375 if alpha < 2.5 / 2.75 else
                7.5625 * (alpha - 2.625 / 2.75) ** 2 + 0.984375
            ),
            "ease_in_out_bounce": lambda alpha: (
                (1 - funcs["ease_out_bounce"](1 - 2 * alpha)) / 2 if alpha < 0.5 else
                (1 + funcs["ease_out_bounce"](2 * alpha - 1)) / 2
            ),

            # Перевищення (back)
            "ease_in_back": lambda alpha: 2.70158 * alpha ** 3 - 1.70158 * alpha ** 2,
            "ease_out_back": lambda alpha: 1 + 2.70158 * (alpha - 1) ** 3 + 1.70158 * (alpha - 1) ** 2,
            "ease_in_out_back": lambda alpha: (
                ((2 * alpha) ** 2 * ((2.5949 + 1) * 2 * alpha - 2.5949)) / 2 if alpha < 0.5 else
                (((2 * alpha - 2) ** 2 * ((2.5949 + 1) * (alpha * 2 - 2) + 2.5949)) + 2) / 2
            ),
        }

        if easing == "random":
            obj = random.choice(list(funcs.items()))
            return obj[1]

        return funcs[easing]
