import random


class Person:
    '''
    安定結婚問題に参加する個人（男性/女性）を表すクラス。
    '''
    def __init__(self, n, i):
        '''
        選好リストをランダムに初期化する。

        Parameters
        ----------
        n : int
            安定結婚問題に参加する異性の数。
        i : int
            自身のインデクス。
        '''
        self.preference_list = [i for i in range(n)]
        self.index = i
        random.shuffle(self.preference_list)

    def prefers(self, p1, p2):
        '''
        異性p1とp2どちらを好む（選好リストで上位）かを判定する。

        Parameters
        ----------
        p1, p2 : Person
            異性オブジェクト。

        Returns
        -------
            p1をp2より好む場合True。
            p1とp2が同一の異性である場合はFalse。
        '''
        return self.preference_list.index(p1.index) < self.preference_list.index(p2.index)


class Instance:
    '''
    安定結婚問題のインスタンスを表すクラス。
    '''
    def __init__(self, n):
        '''
        安定結婚問題のインスタンスをランダムに生成する。

        Parameters
        ----------
        n : int
            安定結婚問題に参加する男性（女性）の数
        '''
        self.size = n
        self.men = [Person(n, i) for i in range(n)]
        self.women = [Person(n, i) for i in range(n)]

    def show(self):
        '''
        自身の情報をプリントする。
        '''
        print("men")
        for man in self.men:
            print(" " + str(man.index) + " : " + str(man.preference_list))
        print("women")
        for woman in self.women:
            print(" " + str(woman.index) + " : " + str(woman.preference_list))


class Matching():
    '''
    マッチングを表すクラス。
    '''
    def __init__(self):
        self.pairs = []

    def add_pair(self, man, woman):
        '''
        男女ペアを追加する。

        Parameters
        ----------
        man : Person
            男性オブジェクト。
        woman : Person
            女性オブジェクト。
        '''
        self.pairs.append((man, woman))

    def remove_pair(self, man, woman):
        '''
        男女ペアを削除する。
        指定された男女ペアが存在しない場合の動作は未保証。

        Parameters
        ----------
        man : Person
            男性オブジェクト。
        women : Person
            女性オブジェクト。
        '''
        self.pairs.remove((man, woman))

    def search_husband(self, woman):
        '''
        該当のマッチング中のwomanのマッチング相手を返す。

        Parameters
        ----------
        woman : Person
            女性オブジェクト。

        Returns
        -------
            womanとマッチしている男性オブジェクト。
            マッチング中にwomanが含まれない場合はNoneを返す。
        '''
        for pair in self.pairs:
            if woman.index == pair[1].index:
                return pair[0]
        return None

    def search_wife(self, man):
        '''
        該当のマッチング中のmanのマッチング相手を返す。

        Parameters
        ----------
        man : Person
            男性オブジェクト。

        Returns
        -------
            manとマッチしている女性オブジェクト。
            マッチング中にmanが含まれない場合はNoneを返す。
        '''
        for pair in self.pairs:
            if man.index == pair[0].index:
                return pair[1]
        return None

    def show(self):
        pair_list = [(pair[0].index, pair[1].index) for pair in self.pairs]
        pair_list.sort()
        for pair in pair_list:
            print("(" + str(pair[0]) + ", " + str(pair[1]) + ")", end=" ")
        print()

if __name__ == "__main__":
    random.seed(0)

    # インスタンス生成
    instance = Instance(10)
    instance.show()

    # 選好順序の判定メソッド
    man0 = instance.men[0]
    man1 = instance.men[1]
    woman0 = instance.women[0]
    assert(woman0.prefers(man0, man1))

    # マッチング作成
    woman3 = instance.women[3]
    matching = Matching()
    matching.add_pair(man1, woman0)
    matching.add_pair(man0, woman3)
    matching.show()  # => (1, 0), (0, 3)
    matching.remove_pair(man1, woman0)
    matching.show()  # => (0, 3)
