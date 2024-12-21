import pytest
from hashmap.hashmap import SpecialHashMap

class TestSpecialHashMap:
    @pytest.fixture()
    def special_hash_map(self):
        map = SpecialHashMap()

        map["value1"] = 1
        map["value2"] = 2
        map["value3"] = 3
        map["1"] = 10
        map["2"] = 20
        map["3"] = 30
        map["1, 5"] = 100
        map["5, 5"] = 200
        map["10, 5"] = 300

        return map

    @pytest.fixture()
    def special_hash_map_second(self):
        map = SpecialHashMap()

        map["value1"] = 1
        map["value2"] = 2
        map["value3"] = 3
        map["1"] = 10
        map["2"] = 20
        map["3"] = 30
        map["(1, 5)"] = 100
        map["(5, 5)"] = 200
        map["(10, 5)"] = 300
        map["(1, 5, 3)"] = 400
        map["(5, 5, 4)"] = 500
        map["(10, 5, 5)"] = 600

        return map

    def test_get_item(self, special_hash_map):
        map = special_hash_map

        assert map["value1"] == 1

    def test_iloc(self, special_hash_map):
        map = special_hash_map

        assert map.iloc[0] == 10
        assert map.iloc[2] == 300
        assert map.iloc[5] == 200
        assert map.iloc[8] == 3

    def test_iloc_ind_error(self, special_hash_map):
        map = special_hash_map

        with pytest.raises(IndexError):
            map.iloc[190]

    def test_iloc_ind_not_int(self, special_hash_map):
        map = special_hash_map

        with pytest.raises(TypeError):
            map.iloc[1.0]

    def test_iloc_ind_is_negative(self, special_hash_map):
        map = special_hash_map

        with pytest.raises(IndexError):
            map.iloc[-1]

    def test_ploc(self, special_hash_map_second):
        map_sc = special_hash_map_second

        assert map_sc.ploc[">=1"] == '{1=10, 2=20, 3=30}'
        assert map_sc.ploc["<3"] == '{1=10, 2=20}'
        assert map_sc.ploc[">0, >0"] == '{(1,  5)=100, (5,  5)=200, (10,  5)=300}'
        assert map_sc.ploc[">=10, >0"] == '{(10,  5)=300}'
        assert map_sc.ploc["<5, >=5, >=3"] == '{(1,  5,  3)=400}'
        assert map_sc.ploc["<>5"] == '{1=10, 2=20, 3=30}'
        assert map_sc.ploc["==2"] == '{2=20}'
        assert map_sc.ploc["<=1, <=5"] == '{(1,  5)=100}'