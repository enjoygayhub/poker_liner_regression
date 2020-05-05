from collections import Counter
import random
import csv
from itertools import chain,combinations


class Analyse:
    all_cards = set((x, y) for x in range(4) for y in range(13))

    def flop_hs(self, card_5):
        rest_cards=self.all_cards-set(card_5)
        behand = tie = ahead = 0
        our_rank = self.rank(card_5)
        for opponent in combinations(rest_cards, 2):
            oppo_rank = self.rank(card_5[2:]+list(opponent))
            if oppo_rank > our_rank:
                behand += 1
            elif oppo_rank < our_rank:
                ahead += 1
            else:
                tie += 1
        HS = round((ahead+tie/2)/(ahead+tie+behand), 3)
        return HS

    def flop_ppot(self,card_5):
        rest_cards=self.all_cards-set(card_5)
        hp=[[0]*3 for _ in range(3)]
        our_rank = self.rank(card_5)
        for _ in range(200):
            oppo_cards = random.sample(rest_cards, 2)
            oppo_rank = self.rank(card_5[2:]+oppo_cards)
            if oppo_rank > our_rank:
                index = 2
            elif oppo_rank < our_rank:
                index = 0
            else:
                index = 1
            leftcards=rest_cards-set(oppo_cards)
            for _ in range(100):
                community_cards_2 = random.sample(leftcards,2)
                ourbest = self.best_rank(card_5+community_cards_2)
                oppobest = self.best_rank(card_5[2:]+oppo_cards+community_cards_2)
                if ourbest > oppobest:
                    hp[index][0]+=1
                elif ourbest < oppobest:
                    hp[index][2]+=1
                else:
                    hp[index][1]+=1
        ppot = (hp[2][0] + hp[2][1]/2 + hp[1][0]/2) / (sum(hp[2]) + sum(hp[1])/2+1)
        return round(ppot, 3)

    def turn_hs(self, card_6):
        rest_cards=self.all_cards-set(card_6)
        behand = tie = ahead = 0
        our_rank = self.best_rank(card_6)
        for opponent in combinations(rest_cards, 2):
            oppo_rank = self.best_rank(card_6[2:]+list(opponent))
            if oppo_rank > our_rank:
                behand += 1
            elif oppo_rank < our_rank:
                ahead += 1
            else:
                tie += 1
        HS = round((ahead+tie/2)/(ahead+tie+behand), 3)
        return HS

    def turn_ppot(self,card_6):
        rest_cards=self.all_cards-set(card_6)
        hp=[[0]*3 for _ in range(3)]
        our_rank = self.best_rank(card_6)
        for opponent in combinations(rest_cards, 2):

            oppo_rank = self.best_rank(card_6[2:]+list(opponent))
            if oppo_rank > our_rank:
                index = 2
            elif oppo_rank < our_rank:
                index = 0
            else:
                index = 1
            leftcards=rest_cards-set(opponent)
            for community_cards_1 in leftcards:

                ourbest = self.best_rank(card_6+[community_cards_1])
                oppobest = self.best_rank(card_6[2:]+list(opponent)+[community_cards_1])
                if ourbest > oppobest:
                    hp[index][0]+=1
                elif ourbest < oppobest:
                    hp[index][2]+=1
                else:
                    hp[index][1]+=1
        ppot = (hp[2][0] + hp[2][1]/2 + hp[1][0]/2) / (sum(hp[2]) + sum(hp[1])/2+1)
        return round(ppot, 3)

    def rank(self, cards5):  # 判断5张牌的牌型
        cards = list(chain(*cards5))
        flower_counter = Counter(cards[::2])  # 花色计数器
        _, max_number_of_flowers = flower_counter.most_common(1)[0]  # 记录卡牌花色最多的数量
        all_num = sorted(cards[1::2], reverse=True)
        number_counter = Counter(all_num)   # 牌值计数器
        most_four = number_counter.most_common(4)   # 牌值出现频率
        if max_number_of_flowers == 5:     # 同花顺
            if all_num[0]-all_num[-1] == 4:
                return [8, all_num[0]]
            elif all_num == [12, 3, 2, 1, 0]:    # 同花顺12345
                return [8, all_num[1]]
            else:
                return [5]+all_num     # 同花
        elif most_four[0][1] == 4:    # 4条
            return [7, most_four[0][0], most_four[1][0]]
        elif most_four[0][1] == 3:
            if most_four[1][1] == 2:   # 葫芦
                return [6, most_four[0][0], most_four[1][0]]
            else:
                return [3, most_four[0][0], most_four[1][0], most_four[2][0]]  # 3条
        elif most_four[0][1] == 2:
            if most_four[1][1] == 2:
                return [2, most_four[0][0], most_four[1][0], most_four[2][0]]    # 2 对
            else:
                return [1, most_four[0][0], most_four[1][0], most_four[2][0], most_four[3][0]]    # 一对
        elif all_num[0]-all_num[-1] == 4:       # 顺子
            return [4, all_num[0]]
        elif all_num == [12, 3, 2, 1, 0]:    # 顺12345
            return [4, all_num[1]]
        else:
            return [0]+all_num   # 高牌

    def best_rank(self, cards):
        return max(map(self.rank, combinations(cards,5)))


if __name__ == '__main__':  # 生成所需类型的数据集
    e = Analyse()
    result = []
    count=0
    while True:
        cards5 = random.sample(e.all_cards, 5)
        val=e.rank(cards5)
        if val[0]==0:  # 0为高牌，1一对，2两对，3三条，收集数据
            count+=1
            print(cards5)
            hs=e.flop_hs(cards5)

            ppot=e.flop_ppot(cards5)

            ehs=round(hs+(1-hs)*ppot,3)

            data=list(chain(*cards5))
            data.append(ehs)
            result.append(data)
        if count==1000:
            break
    with open('flop0.csv', 'a', newline='') as t_file:
        csv_writer = csv.writer(t_file)
        for l in result:
            csv_writer.writerow(l)


