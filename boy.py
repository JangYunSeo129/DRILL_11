from pico2d import *

#이벤트정의
RD, LD, RU, LU, TIMER, AD = range(6)
# == RD, LD, RU, LU = 0,1,2,3
key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYDOWN, SDLK_a): AD
}

class IDLE:
    @staticmethod
    def enter(self, event): #상태들어갈때행하는액션
        print('enter idle')
        self.dir = 0
        self.timer = 1000
        pass

    @staticmethod
    def exit(self): #상태나올때행하는액션
        print('exit idle')
        pass

    @staticmethod
    def do(self): #상태에있을때 지속적으로행하는액션
        self.frame = (self.frame + 1) % 8
        self.timer -= 1
        if self.timer == 0:
            self.add_event(TIMER)
        pass

    @staticmethod
    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)


class RUN:
    @staticmethod
    def enter(self, event):
        print('enter run')
        if event == RD:
            self.dir += 1
        if event == LD:
            self.dir -= 1
        if event == RU:
            self.dir -= 1
        if event == LU:
            self.dir += 1
        pass

    @staticmethod
    def exit(self):
        print('exit run')
        self.face_dir = self.dir
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir
        self.x = clamp(0, self.x, 800)
        pass

    @staticmethod
    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)
        elif self.dir == 1:
            self.image.clip_draw(self.frame*100, 100, 100, 100, self.x, self.y)


class SLEEP:
    @staticmethod
    def enter(self, event): #상태들어갈때행하는액션
        print('enter sleep')
        pass

    @staticmethod
    def exit(self): #상태나올때행하는액션
        print('exit sleep')
        pass

    @staticmethod
    def do(self): #상태에있을때 지속적으로행하는액션
        self.frame = (self.frame + 1) % 8
        pass

    @staticmethod
    def draw(self):
        if self.face_dir == -1:
            self.image.clip_composite_draw(self.frame * 100, 200, 100, 100, -3.141592/2, '', self.x + 25, self.y - 25, 100, 100)
        else:
            self.image.clip_composite_draw(self.frame * 100, 300, 100, 100, 3.141592/2, '', self.x - 25, self.y - 25, 100, 100)


class AUTO_RUN:
    @staticmethod
    def enter(self, event):
        print('enter autorun')
        self.dir = self.face_dir

    @staticmethod
    def exit(self):
        print('exit autorun')
        self.face_dir = self.dir
        self.dir = 0
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir
        if self.dir < 0 and self.x < 100:
            self.dir = 1
        elif self.dir > 0 and self.x > 700:
            self.dir = -1
        self.x = clamp(0, self.x, 800)
        pass

    @staticmethod
    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y + 25, 200, 200)
        elif self.dir == 1:
            self.image.clip_draw(self.frame*100, 100, 100, 100, self.x, self.y + 25, 200, 200)



#상태변환기술
next_state = {
    SLEEP: {RU: RUN, LU: RUN, RD: RUN, LD: RUN, TIMER: SLEEP},
    IDLE: {RU: RUN, LU: RUN, RD: RUN, LD: RUN, TIMER: SLEEP, AD: AUTO_RUN},
    RUN : {RU: IDLE, LU: IDLE, RD: IDLE, LD: IDLE, AD: AUTO_RUN},
    AUTO_RUN:{AD: IDLE, RU: RUN, LU: RUN, RD: RUN, LD: RUN} #굿아이디어 - 런에서 하나더누르면 idle로
}


class Boy:

    def add_event(self, event):
        self.q.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        # if event.type == SDL_KEYDOWN:
        #     match event.key:
        #         case pico2d.SDLK_LEFT:
        #             boy.dir -= 1
        #         case pico2d.SDLK_RIGHT:
        #             boy.dir += 1
        # elif event.type == SDL_KEYUP:
        #     match event.key:
        #         case pico2d.SDLK_LEFT:
        #             boy.dir += 1
        #             boy.face_dir = -1
        #         case pico2d.SDLK_RIGHT:
        #             boy.dir -= 1
        #             boy.face_dir = 1

    def __init__(self):
        self.x, self.y = 0, 90
        self.frame = 0
        self.dir, self.face_dir = 0, 1
        self.image = load_image('animation_sheet.png')

        self.q = [] #이벤트큐초기화
        self.cur_state = IDLE
        self.cur_state.enter(self, None)


    def update(self):
        self.cur_state.do(self)
        # 이벤트확인해서 있으면 이벤트변환
        if self.q: #큐에 이벤트가있으면(이벤트가발생하면)
            event = self.q.pop()
            self.cur_state.exit(self)
            self.cur_state = next_state[self.cur_state][event]
            self.cur_state.enter(self, event)

        # self.frame = (self.frame + 1) % 8
        # self.x += self.dir * 1
        # self.x = clamp(0, self.x, 800)

    def draw(self):
        self.cur_state.draw(self)
        # if self.dir == -1:
        #     self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)
        # elif self.dir == 1:
        #     self.image.clip_draw(self.frame*100, 100, 100, 100, self.x, self.y)
        # else:
        #     if self.face_dir == 1:
        #         self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        #     else:
        #         self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
