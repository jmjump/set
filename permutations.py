
# n is the number of items in the set
# k is the number of items to choose
def find_permutations(n, k):
    # The first time through, it's 0, 1, 2, ... k-1
    permutation = [i for i in range(k)]

    while True:
        yield permutation

        # return False when done
        def find_next_permutation(permutation, n, k):
            for i in range(k):
                #print(f"{i=}")
                j = k - i - 1 #
                #print(f"{j=}")
                #print(f"{permutation[j]=}")
                # is this index at the end?
                if permutation[j] < n - i - 1:
                    permutation[j] += 1

                    # set the remaining indicies
                    for ii in range(k-j-1):
                        permutation[j+ii+1] = permutation[j] + ii + 1
                    return True
            return False

        if not find_next_permutation(permutation, n, k):
            return

def find_set_permutations(set, k):
    for permutation in find_permutations(len(set), k):
        yield [set[permutation[i]] for i in range(k)]

