ALGEBRA_NUMBER_THEORY = """

"""

GEOMOTRY_TOPOLOGY = """


"""

ANALYSYS_EQUATION = """
问题：对实数$r$，用$\\Vert{r}$表示$r$和最近的整数的距离：$\\Vert{r} = \min {\\vert{r-n}:n\\in\\mathbb{Z}}$.
试问是否存在非零实数$s$，满足$\\lim_{n\\to\\infty}\\Vert{(\\sqrt{2}+1)^ns}=0$?
解题规划：
{
    "plan": <[{"desc":"取特殊值简化思考，当$s=1$时，求证$\\lim_{n\\to\\infty}\\Vert{(\\sqrt{2}+1)^n}=0$", "phase":"inference"},{"desc":"将幂级数的有理整数和无理数部分分开，构造新的级数$(\\sqrt{2}+1)^n=x_n+\\sqrt{2}y_n$","phase":"inference"},{"desc":"","phase":""}]>,
    "reason": <"reason">
}
"""

COMBINATION_PROBABILITY = """


"""

COMPUTATION = """


"""


print(ANALYSYS_EQUATION)