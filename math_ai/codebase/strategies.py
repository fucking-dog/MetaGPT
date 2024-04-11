ALGEBRA_NUMBER_THEORY = """

"""

GEOMOTRY_TOPOLOGY = """


"""

ANALYSYS_EQUATION = """
问题：对实数$r$，用$\\Vert{r}$表示$r$和最近的整数的距离：$\\Vert{r} = \min {\\vert{r-n}:n\\in\\mathbb{Z}}$.
试问是否存在非零实数$s$，满足$\\lim_{n\\to\\infty}\\Vert{(\\sqrt{2}+1)^ns}=0$?
解题规划：
{
    "plan": <[{"desc":"当$s=1$时，将幂级数的有理整数和无理数部分分开，构造新的级数$(\\sqrt{2}+1)^n=x_n+\\sqrt{2}y_n$","phase":"inference"},{"desc":"求幂级数到最近整数的距离，根据放缩法，先求到某一整数的距离$\\vert{x_n+\\sqrt{2}y_n-2x_n}$","phase":"inference"},{"desc":"观察到$(x+\\sqrt{2}y_n)(x-\\sqrt{2}y_n)=x_n^2-2y_n^2=(-1)^n$","phase":"inference"},{"desc":"因此$\\vert{x_n+\\sqrt{2}y_n-2x_n=\\frac{\\vert{2y_n^2-x_n^2}}{\\sqrt{2}y_n+x_n}}\\rightarrow 0$","phase":"inference"}]>,
    "reason": <"reason">
}
"""

COMBINATION_PROBABILITY = """


"""

COMPUTATION = """


"""
def get_strategy_desc(name):
    if name == "ALGEBRA_NUMBER_THEORY":
        return ALGEBRA_NUMBER_THEORY
    elif name == "GEOMOTRY_TOPOLOGY":
        return GEOMOTRY_TOPOLOGY
    elif name == "ANALYSYS_EQUATION":
        return ANALYSYS_EQUATION
    elif name == "COMBINATION_PROBABILITY":
        return COMBINATION_PROBABILITY
    elif name == "COMPUTATION":
        return COMPUTATION
    else:
        return "No Strategy"
    
print(ANALYSYS_EQUATION)