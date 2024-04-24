import math

difficulty=5
questions_answered = 3
percent = 69
length_array = 6



increase = 2.0
difficulty,questions_answered,percent,length_array
if percent < 70:
    increase = -(increase)
    if length_array < 3:
        try:
            increase = increase*(1-(percent/100))
            print("1")
        except:
            increase = increase*0.8
            print("2")

print(increase/((math.log(questions_answered))+0.5))
increase = increase/((math.log(questions_answered))+0.7)
new_difficulty = difficulty + increase
if new_difficulty > 7:
    new_difficulty = 7
if new_difficulty < 0:
    new_difficulty = 0

print(new_difficulty)