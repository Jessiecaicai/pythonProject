data = [
    ("one", "aaa", "1"),
    ("two", "bbb", "2"),
    ("three", "ccc", "3")
]

big_list = []
for i, (_, _, seq) in enumerate(data):
    big_list.append(seq)

print(big_list)

small_list = list(range(7))
print(small_list)