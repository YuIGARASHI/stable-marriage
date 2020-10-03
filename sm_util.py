import itertools
import math
import random
from model import Instance, Matching, Person


class SMUtil:
    @staticmethod
    def create_all_matching(instance):
        '''
        インスタンス中の全通りのマッチングを生成して返す。
        O(n!)の計算量（空間・時間）を必要とするため注意。

        Parameters
        ----------
        instance : Instance
            安定結婚問題のインスタンス。

        Returns
        -------
            全通りのマッチングを詰めたリスト。
        '''
        matching_list = []
        for men in itertools.permutations(instance.men):
            matching = Matching()
            for i, man in enumerate(men):
                woman = instance.women[i]
                matching.add_pair(man, woman)
            matching_list.append(matching)
        return matching_list

    @staticmethod
    def is_stable(instance, matching):
        '''
        対象のマッチングが安定かどうか判定する。
        ナイーブな実装のためO(n^2)の計算量を必要とする。

        Parameters
        ----------
        instance : Instance
            安定結婚問題のインスタンスオブジェクト。
        matching : Matching
            マッチングオブジェクト。

        Returns
        -------
        is_stable : bool
            安定であればTrue。
        pair : (Person, Person)
            マッチングが非安定であればブロッキングペア。
            安定であれば無効値。
        '''
        for man in instance.men:
            for woman in instance.women:
                # 男性側に駆け落ちするインセンティブが存在
                man_dissatisfaction = man.prefers(woman, matching.search_wife(man))
                # 女性側に駆け落ちするインセンティブが存在
                woman_dissatisfaction = woman.prefers(man, matching.search_husband(woman))
                if man_dissatisfaction and woman_dissatisfaction:
                    return False, (man, woman)
        return True, (Person(0, -1), Person(0, -1))


if __name__ == "__main__":
    random.seed(3)

    # create_all_matching のテスト
    instance_size = 8
    instance = Instance(instance_size)
    matching_list = SMUtil.create_all_matching(instance)
    assert(len(matching_list) == math.factorial(instance_size))
    print("show Matchings")
    for i, matching in enumerate(matching_list):
        matching.show()
        if i > 10:
            break

    # is_stable のテスト
    print("show Instance")
    instance.show()
    is_stable, blocking_pair = SMUtil.is_stable(instance, matching_list[0])
    assert(is_stable is False)
    print(str(blocking_pair[0].index) + ", " + str(blocking_pair[1].index))  # => 1, 2
    stable_matching_count = 0
    for matching in matching_list:
        is_stable, blocking_pair = SMUtil.is_stable(instance, matching)
        if is_stable:
            stable_matching_count += 1
    assert(stable_matching_count == 4)