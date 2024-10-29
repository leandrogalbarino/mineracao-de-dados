import pandas as pd

a = [1, 1, 0, 0, 1, 1, 0, 1]
b = [0, 1, 0, 1, 1, 0, 0, 0]
c = [0, 1, 1, 0, 1, 1, 1, 0]
goal = [1, 0, 1, 0, 1, 1, 1,  1]

df = pd.DataFrame({
    'a': a,
    'b': b,
    'c': c,
    'goal': goal
})

for i, j  in df.iterrows():
    print(f"Linha{i}: {j['a']}, {j['b']}, {j['c']} - Goal: {j['goal']} ")


interseccao = 0
for i in range(8):
    if a[i] == 1 and goal[i] == 1:
        interseccao+= 1
# Suporte de 
sup = interseccao / 8

interseccaoAA = sum(a)
interseccaoBB = sum(goal)


confA = interseccao / interseccaoAA
confB = interseccao / interseccaoBB

lift = sup / ((interseccaoAA/8) * (interseccaoBB/8))
print(f"sup = {sup}")
print(f"confA = {confA}")
print(f"liftAB = {lift}")