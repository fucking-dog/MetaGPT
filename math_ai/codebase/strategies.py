ALGEBRA_NUMBER_THEORY = """

"""

GEOMOTRY_TOPOLOGY = """


"""

ANALYSYS_EQUATION = """
问题：对实数$r$，用$\\Vert{r}$表示$r$和最近的整数的距离：$\\Vert{r} = \min {\\vert{r-n}:n\\in\\mathbb{Z}}$.
试问是否存在非零实数$s$，满足$\\lim_{n\\to\\infty}\\Vert{(\\sqrt{2}+1)^ns}=0$?
解题规划：
{
    "plan": <[{"desc":"当$s=1$时，将幂级数的有理整数和无理数部分分开，构造新的级数$(\\sqrt{2}+1)^n=x_n+\\sqrt{2}y_n$","phase":"inference"},{"desc":"求幂级数到最近整数的距离，根据放缩法，先求到某一整数的距离$\\vert{x_n+\\sqrt{2}y_n-2x_n}$","phase":"inference"},{"desc":"观察到$(x+\\sqrt{2}y_n)(x-\\sqrt{2}y_n)=x_n^2-2y_n^2=(-1)^n$","phase":"inference"},{"desc":"因此$\\vert{x_n+\\sqrt{2}y_n-2x_n=\\frac{\\vert{2y_n^2-x_n^2}}{\\sqrt{2}y_n+x_n}}\\rightarrow 0$","phase":"inference"},{"desc":"验证上述过程是否存在逻辑问题","phase":"logic_validate"}]>
}
"""

COMBINATION_PROBABILITY = """
问题：一位快递员在二维格点平面上坐标为$(n,0)$处取到了快递。他所工作的快递站则在原点$(0,0)$处。此后，快递员每一步做步长为$1$的简单随机游动。不妨认为正整数$n$远大于$1$。令$P_{1,n}$为该快递员在走了恰好$\\lfoor n^{1.5}\\rfloor$步时，距离快递站的直线距离大于$\\frac{n}{2}$的概率，试证明$\\lim_{n\\to+\\infty}P_{1,n}=1$。
解题规划：
{
    "plan": <[{"desc":"考虑事件A为快递员此时距取件点的距离大于等于$\\frac{n}{2}$，那么快递员在至少一个坐标方向上移动的距离至少为$\\frac{n}{4}$,不妨设为y轴方向","phase":"inference"},{"desc":"设该快递员在第k步时在y轴方向的移动距离可以被看作是独立同分布的随机变量的求和：$Y_k=X_1+X_2+\\dots+X_k$","phase":"inference"},{"desc":"由于$P(X_i=0)=\\frac{1}{2},P(X_i=\\pm 1)=\\frac{1}{4}$,所以$E(X_i)=0,var(X_i)=\\frac{1}{2}$","phase":"inference"},{"desc":"由切比雪夫不等式可以得到$P(A)\\leq 2P(\\vert{Y_{\\lfloor n^{1.5}\\rfloor}}\\geq \\frac{n}{4})\\leq 2\\times\\frac{n^{1.5}}{2n^2/16}=16n^{-0.5}\\ll 1$","phase":"di"},{"desc":"验证上述过程是否存在逻辑问题","phase":"logic_validate"}]>
}
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
    
