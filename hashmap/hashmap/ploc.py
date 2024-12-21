import re

class PlocDict:
    def __init__(self, parent):
        self.parent = parent

    def __getitem__(self, conditions):
        res = self.__get_right_items(conditions)
        vals = {}
        for i in res:
            vals[f"{i[0]}"] = i[1]
        formatted_result = '{' + ', '.join(f'{key}={value}' for key, value in vals.items()) + '}'
        return formatted_result

    def __conditions_split(self, conditions):
        conditions = [c.strip() for c in conditions.split(',')]
        conditions = [c for c in conditions if c]
        return conditions

    def __get_right_items(self, conditions):
        if ',' in conditions:
            conditions = self.__conditions_split(conditions)
            conditions = self.__condition_values(conditions)
        else:
            condition = []
            condition.append(conditions)
            conditions = self.__condition_values(condition)

        results = []
        for key, value in self.parent.items():
            if '(' in key or ')' in key:
                key = key.replace('(', '').replace(')', '')

            if ',' in key:
                keys = key.split(',')

                if len(keys) == len(conditions):
                    match_found = True
                    for i, key in enumerate(keys):
                        if not self.__find_values(key, conditions, i):
                            match_found = False
                            break
                    if match_found:
                        res = "(" + str(keys) + ")"
                        res = res.replace('[', '').replace(']', '').replace("'", '')
                        results.append((res, value))

            else:
                if len(key) == len(conditions):
                    match_found = True
                    if not any(char.isalpha() for char in key):
                        if not self.__find_values(key, conditions):
                            match_found = False
                        if match_found:
                            results.append((key, value))

        return results

    def __condition_values(self, conditions):
        res = []

        if len(conditions) > 1:
            for condition in conditions:
                match = re.match(r"([<>]=?|==|<>)(-?\d+(\.\d+)?)", condition)
                if match:
                    condition_op = match.group(1)
                    condition_val = float(match.group(2))

                res.append([condition_op, condition_val])

        else:
            match = re.match(r"([<>]=?|==|<>)(-?\d+(\.\d+)?)", conditions[0])
            if match:
                condition_op = match.group(1)
                condition_val = float(match.group(2))

                res.append([condition_op, condition_val])

        return res

    def __find_values(self, key, condition, i=0):
        condition_op = condition[i][0]
        condition_val = condition[i][1]
        flag = True
        flag = self.__check_condition(key, condition_op, condition_val)

        return flag

    def __check_condition(self, key, condition_op, condition_val):
        if condition_op == '>':
            return float(key) > condition_val
        elif condition_op == '>=':
            return float(key) >= condition_val
        elif condition_op == '<':
            return float(key) < condition_val
        elif condition_op == '<=':
            return float(key) <= condition_val
        elif condition_op == '==':
            return float(key) == condition_val
        elif condition_op == '<>':
            return float(key) != condition_val