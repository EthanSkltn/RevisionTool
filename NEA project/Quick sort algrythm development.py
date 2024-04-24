from collections import deque

def run_queue(array):
    if len(array) <= 1:
        return array
    final_array = []
    longest = []
    shortest = []
    pivot = array[-1]
    print(pivot)
    for i in range(len(array) - 1):
        if array[i][0] > pivot[0]:
            longest.append(array[i])
        else:
            shortest.append(array[i])
    if len(longest) > 0:
        longest = run_queue(longest)
    if len(shortest) > 0:
        shortest = run_queue(shortest)
    final_array = longest + [pivot] + shortest
    return final_array
new_array = []

array = [8, 5, 8, 3, 4, 7, 2, 1, 1, 1, 1, 8, 6, 5, 5, 89, 9, 8, 7, 5]
array2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,]
for i in range(len(array)):
    new_array.append([array[i],array2[i]])
print(new_array)
j = run_queue(new_array)
j = deque(j)
print(j)
print(j.popleft())
