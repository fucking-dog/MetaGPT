ALGEBRA_NUMBER_THEORY = """
问题：令$n$为正整数。对任一正整数$k$记$0_k$=$\\text{diag}\{0,\\dots,0\}$为$k\\times k$的零矩阵。令
$$
Y=
\\begin{pmatrix}
0_n & A \\\\
A^t & 0_{n+1}
\\end{pmatrix}
$$
为一个$(2n+1)\\times(2n+1)$矩阵，其中$A=(x_{i,j})_{1\\leq i\\leq n,1\\leq j\\leq n+1}$是一个$n\\times(n+1)$实矩阵且$A^t$为$A$的转置矩阵，即$(n+1)\\times n$的矩阵，$(j,i)$处的元素为$x_{i,j}$。
称复数$\\lambda$为$k \\times k$矩阵$X$的一个特征值，如果存在非零列向量$v=(x_1,\\dots,x_k)^t$使得$Xv=\\lambda v$。证明：0是$Y$的特征值且$Y$的其他特征值形如$\\pm\\sqrt{\\lambda}$，其中非负实数$\\lambda$是$AA^t$的特征值。
解题规划：
{
    "plan": <[{"desc":"记$I_n=\\text{diag}\{1,\\dots,1\}$为$n\\times n$恒同矩阵，做初等变换可以证明$\\det(\\lambda I_{2n+1}-Y)=\\lambda\\det(\\lambda^2 I_n-AA^t)$，得证","phase":"di"},{"desc":"验证上述过程是否存在逻辑问题","phase":"logic_validate"}]>
}
"""

GEOMOTRY_TOPOLOGY = """
问题：某个城市有10条东西向的公路和10条南北向的公路，共交于100个路口。小明从某个路口驾车出发，经过每个路口恰好一次，最后回到出发点。在经过每个路口时，向右转不需要等待，直行需要等待1分钟，向左转需要等待2分钟。设小明在路口等待总时间的最小可能值是S分钟，则S的值是多少？
解题规划：
{
    "plan": <[{"desc":"小明行驶的路线是一条不自交的闭折线，将每个路口看成一个顶点，那么其驾驶的路线可以看成一个100边形（有的内角可能是平角，也可能大于平角）。","phase":"inference"},{"desc":"由内角和共识可以知道，这个100边形的所由内角之和为$98\\times 180^\\circ$. 设内角中$90^\\circ$的有$a$个，$270^\\circ$的有$b$个，那么$90a+270b+180(100-a-b)=98\\times 180$，整理可得$a-b=4$","phase":"di"},{"desc":"如果小明在这题啊路上顺时针行驶，那么$90^\\circ$内角对应右转，$180^\\circ$内角对应直行，$270^\\circ$内角对应左转，他在路口等待的总时间为$(100-a-b)+2b=100-(a-b)=96$分钟；如果小明在这题啊路上逆时针行驶，那么$90^\\circ$内角对应左转，$180^\\circ$内角对应直行，$270^\\circ$内角对应右转，他在路口等待的总时间为$(100-a-b)+2a=100+(a-b)=104$分钟"。"phase":"di"},{"desc":"如果小明的起点和终点处的转弯时间不计，等待的总时间还可以减少2分钟，所以$S=94$。","phase":"inference"},{"desc":"验证上述过程是否存在逻辑问题","phase":"logic_validate"}]>
}
"""

ANALYSYS_EQUATION = """
问题：对实数$r$，用$\\Vert{r}$表示$r$和最近的整数的距离：$\\Vert{r} = \min {\\vert{r-n}:n\\in\\mathbb{Z}}$.试问是否存在非零实数$s$，满足$\\lim_{n\\to\\infty}\\Vert{(\\sqrt{2}+1)^ns}=0$?
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
问题：在一个虚拟的世界中，每个居民（设想为没有大小的几何点）依次编号为$1,2,\\dots$. 为了抗击某种疫情，这些居民要求接种某疫苗，并在注射后在现场留观一段时间。现在假设留观的场所是平面上一个半径为$\\frac{1}{4}$的圆周。为了安全，要求第m号居民和第n号居民之间的距离$d_{m,n}$满足$(m+n)d_{m,n}\\leq 1$，这里我们考虑的是圆周上的距离，也就是两点之间的劣弧的弧长，那么这个留观场所最多能容纳多少居民？
解题规划：
{
    "plan": <[{"desc":"对于$n\\leq 2$，若第$1,2,\\dots,n-1$号居民的位置已经被安排好，我们考虑第n号居民不能在哪些位置。","phase":"inference"},{"desc":"对于$1\\leq m\\leq n-1$，由$d_{m,n}\\geq \\frac{1}{m+n}$，我们知道从第m号居民的位置开始，沿顺、逆时针各走$\\frac{1}{m+n}$的距离，所形成的长度为$\\frac{2}{m+n}$的圆弧内部是不可以安排第n号居民的","phase":"inference"},{"desc":"这些圆弧的总长度为$\\frac{2}{n+1}+\\frac{2}{n+2}+\\dots+\\frac{2}{2n-1}<2(\\ln\\frac{n+1}{1}+\\ln\\frac{n+2}{n+1}+\\dots+\\ln\\frac{2n-1}{2n-2})=2\\ln\\frac{2n-1}{n}<2\\ln 2$。","phase":"di"},{"desc":"圆弧的总长度不超过$2\\ln 2$，而整个圆周的长度为$\\frac{1}{4}\\dot 2\\pi=\\frac{\\pi}{2}$，故这些圆弧不能覆盖整个圆周，因此第n号居民总可以选择一个合适的位置，使得他与第$1,2,\\dots,n-1$号居民之间的距离均满足条件。由数学归纳法可知，这个圆周可以容纳任意多个居民。","phase":"inference"},{"desc":"验证上述过程是否存在逻辑问题","phase":"logic_validate"}]>
}
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
    
