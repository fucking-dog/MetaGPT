import asyncio

from metagpt.roles.di.data_interpreter import DataInterpreter


async def main(requirement: str = ""):
    di = DataInterpreter()
    await di.run(requirement)


if __name__ == "__main__":
    question = """
    第4题 某个城市有10条东西向的公路和10条南北向的公路，共交于100个路口，小明从某个路口驾车出发，经过每个路口恰一次，最后回到出发点．在经过每个路口时，向右转不需要等待，直行需要等待1分钟，向左转需要等待2分钟．设小明在路口等待总时间的最小可能值是S分钟，则

    (A).S<50
    (B). 50 ≤ S<90
    (C). 90 ＜S＜100
    (D). 100 ≤ S <150
    (E). S> 150.
    """
    question = """
    Tom has a red marble, a green marble, a blue marble, and three identical yellow marbles. How many different groups of two marbles can Tom choose?
    """
    question = """
    证明对于任意正整数n，n^2 是一个偶数当且仅当n是一个偶数。
    """

    requirement = f"""
    Solve this multiple question: {question}, and return the answer from A to E.
    Please note that when you solve this problem, you should not only consider using code to solve the problem, the results obtained by the code may have a certain deviation from the real problem, you need to conduct further realistic analysis of the results of the code.
    """
    # answer: C
    asyncio.run(main(requirement))