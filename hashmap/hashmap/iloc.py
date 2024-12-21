class IlocDict:
    def __init__(self, parent):
        self.parent = parent

    def __getitem__(self, keyNum):
        dict_sorted = self.parent.toSortedSet()
        keys_and_nums = {}

        for i, key in enumerate(dict_sorted):
            keys_and_nums[f"{i}"] = key

        if not isinstance(keyNum, int):
            raise TypeError("Индекс должен быть целым числом")
        if keyNum > len(dict_sorted):
            raise IndexError("Ваш индекс превышает размер данного словаря")
        if keyNum < 0:
            raise IndexError("Индекс не может быть отрицательным")

        return self.parent[keys_and_nums[f"{keyNum}"]]