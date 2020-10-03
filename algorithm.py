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
            woman = instance.women[next_propose_target_indexes[man.index]]
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
    def calc_optimal_stable_matching(instance):
        '''
        安定マッチングを全列挙し、男性最適安定マッチングと女性最悪安定マッチングを求める。
        男性最適安定マッチング・女性最悪安定マッチングが存在しない場合はエラーとする。

        Parameters
        ----------
        instance : Instance
            安定結婚問題のインスタンス。

        Returns
        -------

        '''
        pass


if __name__ == "__main__":
    random.seed(0)

    # GaleShapleyアルゴリズム実行
    instance = Instance(5)
    gs_output = Algorithm.GaleShapley(instance)
    instance.show()
    gs_output.show()
    assert(SMUtil.is_stable(instance, gs_output))