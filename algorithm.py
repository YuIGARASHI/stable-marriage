import random
from model import Instance, Matching, Person
from sm_util import SMUtil

class Algorithm:
    @staticmethod
    def GaleShapley(instance):
        '''
        GaleShapleyアルゴリズムを実行する。

        Parameters
        ----------
        instance : Instance
            安定結婚問題のインスタンス。

        Returns
        -------
        stable_matching : Matching
            男性最良安定マッチング。
        '''
        # 各男性が次にpreference_listの何番目の女性にプロポーズするか管理するリスト
        next_propose_target_indexes = [0] * instance.size
        # 独身男性のリスト
        single_men = [man.index for man in instance.men]
        # 暫定マッチング
        temp_matching = Matching()
        while single_men:
            man_index = single_men.pop(0)
            man = instance.men[man_index]
            woman_index = man.preference_list[next_propose_target_indexes[man.index]]
            woman = instance.women[woman_index]
            next_propose_target_indexes[man.index] += 1  # 同じ女性には2度とプロポーズしない
            current_husband = temp_matching.search_husband(woman)
            if not current_husband:
                # 女性が独身であれば無条件でマッチングに追加
                temp_matching.add_pair(man, woman)
                continue
            if woman.prefers(man, current_husband):
                # 現在マッチしている男性よりプロポーズしてきた男性を好む場合はのりかえ
                temp_matching.add_pair(man, woman)
                temp_matching.remove_pair(current_husband, woman)
                single_men.append(current_husband.index)
            else:
                single_men.append(man.index)
        stable_matching = temp_matching
        return stable_matching


    @staticmethod
    def calc_man_best_wife_pair(instance):
        '''
        各男性について、安定マッチングでマッチしうる女性のうち最も好みの女性を求める。

        Parameters
        ----------
        instance : Instance
            安定結婚問題のインスタンス。

        Returns
        -------
            該当女性とのペアのリスト。
        '''
        all_matching = SMUtil.create_all_matching(instance)
        best_wife_list = [Person(0, -1)] * instance.size  # 無効値で初期化
        for matching in all_matching:
            is_stable, _ = SMUtil.is_stable(instance, matching)
            if not is_stable:
                continue
            for pair in matching.pairs:
                man = pair[0]
                woman = pair[1]
                if best_wife_list[man.index].index == -1:
                    best_wife_list[man.index] = woman
                    continue
                if man.prefers(woman, best_wife_list[man.index]):
                    best_wife_list[man.index] = woman
        best_pair_list = [(man_index, woman.index) for man_index, woman in enumerate(best_wife_list) ]
        best_pair_list.sort()
        return best_pair_list


    @staticmethod
    def calc_woman_worst_husband_pair(instance):
        '''
        各女性について、安定マッチングでマッチしうる男性のうち最も好みでない男性を求める。

        Parameters
        ----------
        instance : Instance
            安定結婚問題のインスタンス。

        Returns
        -------
            該当男性とのペアのリスト。
        '''
        all_matching = SMUtil.create_all_matching(instance)
        worst_husband_list = [Person(0, -1)] * instance.size  # 無効値で初期化
        for matching in all_matching:
            is_stable, _ = SMUtil.is_stable(instance, matching)
            if not is_stable:
                continue
            for pair in matching.pairs:
                man = pair[0]
                woman = pair[1]
                if worst_husband_list[woman.index].index == -1:
                    worst_husband_list[woman.index] = man
                    continue
                if woman.prefers(worst_husband_list[woman.index], man):
                    worst_husband_list[woman.index] = man
        worst_pair_list = [(man.index, woman_index) for woman_index, man in enumerate(worst_husband_list)]
        worst_pair_list.sort()
        return worst_pair_list

if __name__ == "__main__":
    random.seed(0)

    # GaleShapleyアルゴリズム実行
    instance = Instance(7)
    gs_output = Algorithm.GaleShapley(instance)
    instance.show()
    print("Gale-Shapley出力")
    gs_output.show()
    assert(SMUtil.is_stable(instance, gs_output))

    # 全探索で男性最良ペア、女性最悪ペアを計算
    man_best_pair_list = Algorithm.calc_man_best_wife_pair(instance)
    print("男性最良ペア集合")
    for pair in man_best_pair_list:
        print("(" + str(pair[0]) + ", " + str(pair[1]) + ")", end=" ")
    print()
    woman_worst_pair_list = Algorithm.calc_woman_worst_husband_pair(instance)
    print("女性最悪ペア集合")
    for pair in woman_worst_pair_list:
        print("(" + str(pair[0]) + ", " + str(pair[1]) + ")", end=" ")