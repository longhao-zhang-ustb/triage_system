class Triage():

    @staticmethod
    def getSTART(walk, air_flue, breathe, pulse, blink, speak, motor):
        """获取Start评分
        :param walk: true or false
        :param air_flue: "-1" "0" "1"
        :param breathe: int 呼吸频率
        :param pulse: int 脉搏
        :param blink: 睁眼动作
        :param speak: 语言反应
        :param motor: 运动反应
        """
        if walk:
            return "绿色"
        else:
            if air_flue == "0" or air_flue == 0:
                # 开放气道后无呼吸
                return "黑色"
            elif air_flue == "1" or air_flue == 1:
                # 开放气道后有呼吸
                return "红色"
            # 有呼吸，评估呼吸频率
            elif breathe > 30:
                return "红色"
            else:
                if pulse < 40:
                    # 无脉搏
                    return "红色"
                else:
                    # 有脉搏，接着判断神志状况
                    if blink == "不睁眼" and speak == "不能言语" and motor == "不能活动":
                        # 神志无反应
                        return "红色"
                    else:
                        # 神志有反应
                        return "黄色"

    @staticmethod
    def getJumpSTART(walk, air_flue, breathe, pulse, blink, speak, motor):
        """获取JumpStart评分
        :param walk: true or false 能否行走
        :param air_flue: "-1" "0" "1"
        :param breathe: int 呼吸频率
        :param pulse: int 脉搏
        :param blink: 睁眼动作
        :param speak: 语言反应
        :param motor: 运动反应
        """
        if walk:
            return "绿色"
        else:
            if air_flue == "0" or air_flue == 0:
                # 开放气道无呼吸
                if pulse < 50:
                    # 无明显脉搏
                    return "黑色"
                else:
                    return "红色"
            elif air_flue == "1" or air_flue == 1:
                # 开放气道有呼吸
                return "红色"
            elif breathe < 15 or breathe > 45:
                return "红色"
            else:
                # 呼吸频率15~45次/分
                if pulse < 50:
                    # 无明显脉搏
                    return "红色"
                else:
                    # 有明显脉搏，进行神经系统评估
                    # if mind.endsWith("刺痛能定位") or mind.endsWith("不能活动"):
                    #     # 对伤害性刺激无反应或痛觉刺激反应微弱
                    #     return "红色"
                    # else:
                    #     return "黄色"
                    if blink == "不睁眼" or blink == "不能睁眼" or motor == "不能活动" or motor == "不能运动" or motor == "刺痛后肢体能过度伸展" or motor == "刺痛后肢体能屈曲":
                        # 对伤害性刺激无反应或痛觉刺激反应微弱
                        return "红色"
                    else:
                        # 清醒、对语言刺激有反应或痛觉刺激退缩
                        return "黄色"
    @staticmethod
    def getSelection(pressure, pulse, breathe, through, mind, describe):
        """获取类选Selection评分, true表示危重伤员，应立即送创伤中心或大医院
        :param pressure: int 收缩压
        :param pulse: int 脉搏
        :param breathe: int 呼吸频率
        :param through: true or false 是否有胸腹穿透伤
        :param mind: 神志状况
        :param describe: 伤情描述
        """
        if pressure < 90 and pulse < 120 and (breathe < 12 or breathe > 30):
            return True
        elif through:
            return True
        # elif mind.split('、')[1] == "回答不切题" or mind.split('、')[1] == "答非所问" or mind.split("、")[1] == "不能回答":
        elif mind == "模糊" or mind == "言语不能理解":
            return True
        # elif describe == "高空坠落":
        #     # Todo
        #     # 腕或踝以上部位的创伤性断肢
        #     # 连枷胸
        #     # 有2出或2处以上的上骨骨折
        #     # 从4.572m以上高度坠落
        #     return True
        else:
            return False

    @staticmethod
    def getPrehospital(pressure, pulse, breathe, mind, through):
        """获取院前指数 PHI
        0-3为轻伤员
        4-5为重伤员
        6及以上为危重伤员
        :param pressure: int 收缩压
        :param pulse: int 脉搏
        :param breathe: int 呼吸频率
        :param mind: 意识状态
        :param through: true or false 是否有胸腹穿透伤
        """
        score = 0
        # 收缩压
        if pressure > 100:
            score += 0
        elif pressure >= 86:
            score += 1
        elif pressure >= 75:
            score += 2
        else:
            score += 3
        # 脉搏
        if 51 <= pulse <= 119:
            score += 0
        else:
            score += 1
        # 呼吸
        if 14 <= breathe <= 28:
            score += 0
        elif breathe > 30:
            score += 3
        else:
            score += 5
        # 意识状态
        if mind == "正常":
            score += 0
        elif mind == "模糊" or mind == "烦躁":
            score += 3
        else:
            score += 5
        # 腹部穿透伤
        if through:
            score += 4
        else:
            score += 0
        return score

    @staticmethod
    def getGCS(blink, speak, motor):
        """获取格拉斯哥评分 GCS
        :param blink: 眨眼反应
        :param speak: 言语反应
        :param motor: 运动反应
        """
        score = 0
        # 睁眼反应
        if blink == "不睁眼" or blink == "不能睁眼":
            score += 1
        elif blink == "刺痛睁眼":
            score += 2
        elif blink == "呼唤睁眼":
            score += 3
        else:
            score += 4
        # 语言反应
        if speak == "不能发言" or speak == "不能言语":
            score += 1
        elif speak == "只能发音" or speak == "只能发言":
            score += 2
        elif speak == "答非所问" or speak == "乱讲乱说":
            score += 3
        elif speak == "回答不切题" or speak == "回答错误":
            score += 4
        else:
            score += 5
        # 运动反应
        if motor == "不能活动" or motor == "不能运动":
            score += 1
        elif motor == "刺痛肢体伸展" or motor == "刺痛后肢体能过度伸展":
            score += 2
        elif motor == "刺痛肢体屈曲" or motor == "刺痛后肢体能屈曲":
            score += 3
        elif motor == "刺痛能躲避":
            score += 4
        elif motor == "刺痛能定位":
            score += 5
        else:
            score += 6
        return score

    @staticmethod
    def getTrauma(breathe, pressure, capillary):
        """获取创伤计分 TS
        1-3生理紊乱大，死亡率高
        4-13生理紊乱显著，失治易于死亡，抢救价值大
        14-16生理紊乱小，存活率高
        :param breathe: int 呼吸频率
        :param pressure: int 收缩压
        :param capillary: 毛细血管充盈 0-无 1-迟滞 2-正常
        """
        score = 0
        # 呼吸频率
        if breathe == 0:
            score += 0
        elif breathe < 10:
            score += 1
        elif breathe <= 24:
            score += 4
        elif breathe <= 35:
            score += 3
        else:
            score += 2
        # 收缩压
        if pressure == 0:
            score += 0
        elif pressure < 50:
            score += 1
        elif pressure <= 60:
            score += 2
        elif pressure <= 90:
            score += 3
        else:
            score += 4
        # 毛细血管
        if capillary == 0 or capillary == "0":
            score += 0
        elif capillary == 1 or capillary == "1":
            score += 1
        else:
            score += 2
        return score

    @staticmethod
    def getCRAMS(capillary, pressure, breathe, through, motor, speak):
        """获取CRAMS评分
        9-10为轻度伤
        7-8为重度伤
        <=6为危重症伤
        # :param circulate: 循环
        :param capillary: 毛细血管充盈 0-无 1-迟滞 2-正常
        :param pressure: int 收缩压
        :param breathe: int 呼吸频率
        :param through: true or false 是否有胸腹穿透伤
        :param motor: 运动反应
        :param speak: 言语反应
        """
        score = 0
        # 循环
        if capillary == 0 or capillary == "0" or pressure < 84:
            score += 0
        elif capillary == 1 or capillary == "1" or 85 <= pressure <= 100:
            score += 1
        elif capillary == 2 or capillary == "2" or pressure > 100:
            score += 2
        # 呼吸
        if breathe < 14:
            # 无自主呼吸
            score += 0
        elif breathe <= 28:
            # 正常
            score += 2
        else:
            # 费力、浅或呼吸频率>35次/min
            score += 1
        # 胸腹穿透伤
        if through:
            score += 0
        else:
            score += 2
        # 运动反应
        if motor == "不能活动" or motor == "不能运动":
            score += 0
        elif motor == "按吩咐动作":
            score += 2
        else:
            # 只对疼痛刺激有反应
            score += 1
        # 言语反应
        if speak == "回答切题" or speak == "回答正确":
            # 正常
            score += 2
        elif speak == "回答不切题" or speak == "回答错误" or speak == "乱讲乱说":
            # 言语错乱
            score += 1
        else:
            # 不能言语或无法理解
            score += 0
        return score

    @staticmethod
    def getSimpleTrauma(breathe, pressure, blink, speak, motor):
        """获取简易创伤计分 simple_trame
        5分以下（含5分）为危重伤伤员
        6-9分为重伤伤员
        10-11分为中度伤员
        12分为轻伤伤员
        :param breathe: int 呼吸
        :param pressure: int 收缩压
        :param blink: 睁眼动作
        :param speak: 语言反应
        :param motor: 运动反应
        """
        score = 0
        # 呼吸频率
        if 10 <= breathe <= 29:
            score += 4
        elif breathe > 29:
            score += 3
        elif breathe >= 6:
            score += 2
        elif score >= 1:
            score += 1
        else:
            score += 0
        # 收缩压
        if pressure > 89:
            score += 4
        elif pressure >= 76:
            score += 3
        elif pressure >= 50:
            score += 2
        elif pressure >= 1:
            score += 1
        else:
            score += 0
        # 神志等级
        grade = 0
        # 神志-睁眼动作
        if blink == "不睁眼":
            grade += 1
        elif blink == "刺痛睁眼":
            grade += 2
        elif blink == "呼唤睁眼":
            grade += 3
        elif blink == "自动睁眼":
            grade += 4
        # 神志-言语反应
        if speak == "不能言语":
            grade += 1
        elif speak == "只能发言":
            grade += 2
        elif speak == "答非所问":
            grade += 3
        elif speak == "回答不切题":
            grade += 4
        elif speak == "回答切题":
            grade += 5
        # 神志-运动反应
        if motor == "不能活动":
            grade += 1
        elif motor == "刺痛后肢体能过度伸展":
            grade += 2
        elif motor == "刺痛后肢体能屈曲":
            grade += 3
        elif motor == "刺痛能躲避":
            grade += 4
        elif motor == "刺痛能定位":
            grade += 5
        elif motor == "按吩咐动作":
            grade += 6
        # 神志等级
        if 13 <= grade <= 15:
            score += 4
        elif 9 <= grade <= 12:
            score += 3
        elif 6 <= grade <= 8:
            score += 2
        elif 4 <= grade <= 5:
            score += 1
        else:
            score += 0
        return score
    @staticmethod
    def getPrompt(triageRes):
        """返回伤员提示信息
        建议常规处置
        建议优先处置
        建议紧急处置
        建议期待处置 """
        if triageRes == '绿色':
            return '建议常规处置'
        elif triageRes == '黄色':
            return '建议优先处置'
        elif triageRes == '红色':
            return '建议紧急处置'
        elif triageRes == '黑色':
            return '建议期待处置'

        if triageRes.startswith('轻'):  # 轻伤
            return '建议常规处置'
        elif triageRes.startswith('中'):  # 中度伤
            return '建议优先处置'
        elif triageRes.startswith('重'):  # 重伤
            return '建议紧急处置'
        elif triageRes.startswith('危'):  # 危重伤
            return '建议期待处置'

        return '暂无'


