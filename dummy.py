# class Star: #클래스역할: 함수 또는 변수를 그룹이룸으로 묶는다
#     x = 100
#     def change():
#         x = 200
#         print('x is', x)
#
# print(Star.x) #Star클래스x는 클래스변수
# Star.change() #클래스함수호출
# print(Star.x)
# star = Star() #객체생성용이아니여도 객체는 만들어지긴함
# star.change()

# class Player:
#     def __init__(self):
#         self.x = 100
#     def where(self):
#         print(self.x)
#
# player = Player()
# player.where()
#
# Player.where(player)
# player.where() #==Player.where(player)


table = {
    'SLEEP' : {'HIT'    : 'WAKE'},
    'WAKE'  : {'TIMER10': 'SLEEP'}
}

cur_state = 'SLEEP'
event = 'HIT'
next_state = table[cur_state][event]
print(table[cur_state]['HIT'])
print(table['WAKE']['TIMER10'])
