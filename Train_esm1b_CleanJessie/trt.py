
all_label_ids = [-1, -1, 2, 5, 3, 2, -1, 2, -1]
masked_index = []
for i,ids in enumerate(all_label_ids):
    if ids != -1:
        masked_index.append(i)

print(masked_index)