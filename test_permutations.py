from permutations import find_permutations, find_set_permutations

for permutation in find_permutations(6, 3):
    print(permutation)

set = ['a', 'e', 'i', 'o', 'u', 'y']
for permutation in find_set_permutations(set, 3):
    print(permutation)
