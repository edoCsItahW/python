#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-ND
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2023/10/3 13:14
# 当前项目名: python
# 编码模式: utf-8
# 注释:
# -------------------------<Lenovo>----------------------------
print("一元三次方程的基本形式:aX³+bX²+cX+d=0(其中a,b,c,d为常数）")

from fractions import Fraction
import numpy as np
from math import e
from IPython.display import display, Math
from sympy import *
import cmath
import sympy

C_list = ["a", "b", "c", "d"]
nu_arr = np.empty((0, 0))
C_arr = nu_arr
n_list = []
f_list = []
x_list = ["X^2", "X"]

j = 0
for i in C_list:
    j += 1
    inp = input("请输入常数{}的值:\n".format(i))
    nu_arr = np.append(nu_arr, eval(inp))
    if 1.0 == float(eval(inp)) and (j <= 1 or j >= 4):
        n_list.append("")
        f_list.append("")
    elif float(eval(inp)) == 1.0 and 1 < j < 4:
        n_list.append("")
        f_list.append("+")
    elif float(eval(inp)) == 0:
        n_list.append("")
        f_list.append("")
        if j == 2:
            x_list[0] = ""
        elif j == 3:
            x_list[1] = ""
    elif float(eval(inp)) == -1:
        n_list.append("")
        f_list.append("-")
    else:
        n_list.append(inp)
        if float(eval(inp)) > 0:
            f_list.append("+")
        else:
            f_list.append("")
print(f_list, n_list)
eq = "该方程为:{}{}X^3{}{}{}{}{}{}{}{}=0\n" \
    .format(f_list[0], n_list[0],
            f_list[1], n_list[1], x_list[0],
            f_list[2], n_list[2], x_list[1],
            f_list[3], n_list[3])

display(Math(fr"{eq}"))


def fs(x):
    return Fraction(x).limit_denominator()


a, b, c, d = nu_arr[0], nu_arr[1], nu_arr[2], nu_arr[3]
sigma1, sigma2, sigma3 = - b / a, c / a, - d / a

display(Math(r"由韦达定理:\\\begin{cases} "
             fr"x_1+x_2+x_3=-\frac{{b}}{{a}}=\sigma_1={fs(sigma1)} \\"
             fr"x_1x_2+x_1x_3+x_2x_3=\frac{{c}}{{a}}=\sigma_2={fs(sigma2)} \\"
             fr"x_1x_2x_3=-\frac{{d}}{{a}}=\sigma_3={fs(sigma3)}"
             r"\end{cases} \\"
             r"(这是由于(\mathbf{x}-x_1)(\mathbf{x}-x_2)(\mathbf{x}-x_3)="
             r"x^3 -(x_1 +x_2 +x_3 )x^2 +(x_1 x_2 +x_1 x_2 +x_2 x_3 )x-x_1 x_2 x_3)"))

display(Math(r"\begin{aligned}令: x_1+\omega x_2+\omega^2 x_3 &=X \\"
             r"x_1+\omega^2 x_2+\omega x_3 &=Y \\"
             r"(其中\omega^3 &=1)) \end{aligned}\\"
             r"为求解\omega我们将1变换为e^{2\pi i}(因为由欧拉公式e^{2\pi i}=cos(2\pi) +sin(2\pi)i =1),"
             r"则\omega =e^{\frac{1}{3} 2\pi \mathbf{k}}(k为常数) \\"
             r"\begin{aligned} \begin{cases}"
             r"当\mathbf{k} &=0时 \quad \omega =1 \\"
             r"当\mathbf{k} &=1时 \quad \omega ="
             r"e^{\frac{2\pi}{3}}="
             r"cos(\frac{2\pi}{3}) +sin(\frac{2\pi}{3})i ="
             r"-\frac{1}{2}+\frac{\sqrt{3}}{2}i \\"
             r"当\mathbf{k} &=2时 \quad \omega ="
             r"e^{\frac{4\pi}{3}}="
             r"cos(\frac{4\pi}{3}) +sin(\frac{4\pi}{3})i ="
             r"-\frac{1}{2}-\frac{\sqrt{3}}{2}i \\ "
             r"(注:\omega的三个解组成了一个循环集合,当k取大于等于3的整数时,解将重复, \\ "
             r"因此只考虑k = 0、1和2的情况就可以覆盖所有可能的解)\end{cases} \end{aligned}"))

A = 2 * sigma1 ** 3 - 9 * sigma1 * sigma2 + 27 * sigma3
B = (sigma1 ** 2 - 3 * sigma2) ** 3
A_f = fs(2 * sigma1 ** 3 - 9 * sigma1 * sigma2 + 27 * sigma3)
B_f = fs((sigma1 ** 2 - 3 * sigma2) ** 3)

display(Math(r"\begin{aligned}则&(x_1+\omega x_2+\omega^2 x_3)^3 +(x_1+\omega^2 x_2+\omega x_3)^3 "
             fr"=X^3 +Y^3 =2{{\sigma_1}}^3 -9\sigma_1 \sigma_2 +27\sigma_3 = {A_f}\\"
             r"&(x_1+\omega x_2+\omega^2 x_3)^3 (x_1+\omega^2 x_2+\omega x_3)^3 "
             fr"=X^3 Y^3 =({{\sigma_1}}^2 -3\sigma_2)^3 = {B_f}\end{{aligned}}"))

M1 = "{" + str(A_f) + "+\sqrt{" + str(A_f ** 2 - 4 * B_f) + "}}"
M2 = "{" + str(A_f) + "-\sqrt{" + str(A_f ** 2 - 4 * B_f) + "}}"

display(Math(r"联立\left\{\begin{aligned} "
             r"&X^3 +Y^3 \\"
             r"&X^3 Y^3 "
             r" \end{aligned}\right."
             r"\quad解得\left\{\begin{aligned}"
             fr"&X=\sqrt[3]{{\frac{M1}{{2}}}} \\"
             fr"&Y=\sqrt[3]{{\frac{M2}{{2}}}}"
             r"\end{aligned}\right."))

M_1 = "{A+\sqrt{4B-A^2}i}"
M_2 = "{A-\sqrt{4B-A^2}i}"

display(Math(r"为演示这里将$$A=X^3 +Y^3,B=X^3 Y^3$$(为下式计算,这里将\sqrt{-1}代为虚数i) \\"
             r"则\left\{\begin{aligned}"
             fr"&X=\sqrt[3]{{\frac{M_1}{{2}}}} \\"
             fr"&Y=\sqrt[3]{{\frac{M_2}{{2}}}}"
             r"\end{aligned}\right."))



def fracsq(A, B):
    if B <= 0:
        return A / (2 * (-B) ** 0.5)
    else:
        return A / (2 * B ** 0.5)


display(Math(r"为将$$X,Y$$转化为三角函数，且符合三角恒等式sin^2 +cos^2 =1,我们将$$X$$转换为如下形式:\\"
             r"以X为例:X="
             r"\sqrt[6]{B} \sqrt[3]{\frac{A}{2\sqrt{B}} +\frac{\sqrt{4B-A^2}i}{2\sqrt{B}}} \\"
             r"(使用待定系数,即(\frac{A}{2C})^2 +(\frac{\sqrt{4B-A^2}}{2C})^2 =1,则C=\sqrt{B})"))

display(Math(r"如此我们令\left\{\begin{aligned}"
             r"&cos\alpha =\frac{A}{2\sqrt{B}} \\"
             r"&sin\alpha =\frac{\sqrt{4B-A^2}}{2\sqrt{B}}i "
             r"\end{aligned}\right."))

display(Math(r"即相当于:X=\sqrt[6]{B} \sqrt[3]{cos\alpha +sin\alpha i}"
             r"(其中:\alpha =arccos(\frac{A}{2\sqrt{B}}))\\"
             r"\\ 由欧拉公式:e^{ix} =cosx+isinx \\"
             r"则\begin{aligned} "
             r"&X=\sqrt[6]{B} e^{\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})i}\\"
             r"&Y=\sqrt[6]{B} e^{-\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})i} \end{aligned} \\"
             r"接下来使用线性代数求解根的方程组 \\"
             r"\begin{cases}"
             r"x_1+\omega x_2+\omega^2 x_3 &=X \\"
             r"x_1+\omega^2 x_2+\omega x_3 &=Y \\"
             r"x_1 +x_2 +x_3 &=\sigma_1 \end{cases} \\"
             r"设系数矩阵A =\begin{pmatrix}"
             r"1 & \omega & \omega^2 \\"
             r"1 & \omega^2 & \omega \\"
             r"1 & 1 & 1 \end{pmatrix} \quad "
             r"X=\begin{pmatrix}"
             r"x_1 \\"
             r"x_2 \\"
             r"x_3 \end{pmatrix} \quad"
             r" B =\begin{pmatrix}"
             r"X \\"
             r"Y \\"
             r"\sigma_1 \end{pmatrix} \\"
             r"由AX=B,求解X=A^{-1}B \\"
             r"先求其A的逆矩阵A^{-1} \\"
             r"矩阵求逆我们先求A中所有元素a_{ij}的余子式M_{ij} \\"
             r"例如M_{11}=\begin{pmatrix}"
             r"\require{cancel} \cancel{1} & \cancel{\omega} & \cancel{\omega^2} \\"
             r"\cancel{1} & \omega^2 & \omega \\"
             r"\cancel{1} & 1 & 1 \end{pmatrix}"
             r"=\omega(\omega -1) \\"
             r"则M_{12} =1-\omega,M_{13} =1-\omega^2,M_{21} =... \\"
             r"接着求每个M_{ij}对应的代数余子式\tilde{A}_{ij},"
             r"且\tilde{A}_{ij} =(-1)^{i+j}M_{ij} \\"
             r"那么\tilde{A}_{11} =M_{ij},\tilde{A}_{12} =-M_{12},\tilde{A}_{13} =... \\"
             r"现将每个\tilde{A}_{ij}放到对应的行列上构成A的伴随矩阵A^* \\"
             r"即A^* =\begin{pmatrix}"
             r"\omega(\omega -1) & \omega -1 & -(\omega +1)(\omega -1) \\"
             r"\omega(\omega -1) & -(\omega +1)(\omega -1) & \omega -1 \\"
             r"\omega(\omega -1) & \omega(\omega -1) & \omega(\omega -1) \end{pmatrix} \\"
             r"则由A^{-1} =\frac{1}{det(A)}(A^*)^\top,"
             r"其中A的行列式det(A)=3\omega^2-\omega^4-2\omega=3\omega(\omega -1) \\"
             r"即A^{-1} =\frac{1}{3\omega(\omega -1)}\begin{pmatrix}"
             r"\omega(\omega -1) & \omega(\omega -1) & \omega(\omega -1) \\"
             r"\omega -1 & -(\omega +1)(\omega -1) & \omega(\omega -1) \\"
             r"-(\omega +1)(\omega -1) & \omega -1 & \omega(\omega -1) \end{pmatrix} ="
             r"\begin{bmatrix} "
             r"\frac{1}{3} & \frac{1}{3} & \frac{1}{3} \\"
             r"\frac{1}{3\omega} & -\frac{\omega +1}{3\omega} & \frac{1}{3} \\"
             r"-\frac{\omega +1}{3\omega} & \frac{1}{3\omega} & \frac{1}{3} \end{bmatrix} \\"
             r"那么X=A^{-1}B=\begin{bmatrix} "
             r"\frac{1}{3} & \frac{1}{3} & \frac{1}{3} \\"
             r"\frac{1}{3\omega} & -\frac{\omega +1}{3\omega} & \frac{1}{3} \\"
             r"-\frac{\omega +1}{3\omega} & \frac{1}{3\omega} & \frac{1}{3} \end{bmatrix}"
             r"\begin{pmatrix}"
             r"X \\"
             r"Y \\"
             r"\sigma_1 \end{pmatrix} \\"
             r"即\begin{pmatrix}"
             r"x_1 \\"
             r"x_2 \\"
             r"x_3 \end{pmatrix} =\begin{pmatrix}"
             r"\frac{1}{3}(\sigma_1 +X+Y) \\"
             r"\frac{1}{3} \left\{ \sigma_1 +\frac{1}{\omega} [X-(\omega +1)Y] \right\} \\"
             r"\frac{1}{3} \left\{ \sigma_1 +\frac{1}{\omega} [Y-(\omega +1)X] \right\} \end{pmatrix}"))

display(Math(r"则原方程解x_1 =\frac{1}{3} (\sigma_1 +X+Y)="
             r"\frac{1}{3} \sigma_1 +\frac{1}{3} \sqrt[6]{B}"
             r"(e^{\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})i} +e^{-\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})i}) \\"
             r"与x_1不同的是我们将\omega =-\frac{1}{2}+\frac{\sqrt{3}}{2}i代入\frac{1}{\omega} [X-(\omega +1)Y]后"
             r"为 \\-[(\frac{1}{2}+\frac{\sqrt{3}}{2}i)X+(\frac{1}{2}-\frac{\sqrt{3}}{2}i)Y],"
             r"即-[e^{\frac{\pi}{3}i}X+e^{-\frac{\pi}{3}i}Y]\\"
             r"x_2 =\frac{1}{3} \left\{ \sigma_1 +\frac{1}{\omega} [X-(\omega +1)Y] \right\} "
             r"=\frac{1}{3} \sigma_1 -\frac{1}{3} \sqrt[6]{B}"
             r"(e^{\frac{\pi}{3} +\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})i} +"
             r"e^{-[\frac{\pi}{3} +\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})]i}) \\"
             r"X_3同理"))

display(Math(r"为凑成欧拉公式的余弦\frac{e^{ix} +e^{-ix}}{2} =cos(x)的形式，将x_1中提出2 \\"
             r"即\begin{aligned} x_1 &=\frac{1}{3} \sigma_1 +\frac{2}{3} \sqrt[6]{B}"
             r"(\frac{e^{\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})i} "
             r"\quad +e^{-\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})i}}{2}) \\"
             r"&=\frac{1}{3} \sigma_1 +\frac{2}{3} \sqrt[6]{B} cos(\frac{1}{3} arccos(\frac{A}{2\sqrt{B}})) \\"
             r"x_2 &=\frac{1}{3} \sigma_1 -\frac{2}{3} \sqrt[6]{B} "
             r"cos(\frac{\pi}{3} +\frac{1}{3} arccos(\frac{A}{2\sqrt{B}}) \\"
             r"x_3 &=\frac{1}{3} \sigma_1 -\frac{2}{3} \sqrt[6]{B} "
             r"cos(-\frac{\pi}{3} +\frac{1}{3} arccos(\frac{A}{2\sqrt{B}}) \end{aligned}"))


def res(nu):
    if nu == 0:
        if B <= 0:
            return (1 / 3) * sigma1 + (2 / 3) * (B ** (1 / 6)) * \
                cmath.cos(nu + (1 / 3) * ((cmath.pi / 2) - 1j * cmath.log(fracsq(A, B) + sqrt(fracsq(A, B) ** 2 - 1))))
        else:
            return (1 / 3) * sigma1 + (2 / 3) * (B ** (1 / 6)) * cmath.cos(nu + (1 / 3) * cmath.acos(fracsq(A, B)))
    else:
        return (1 / 3) * sigma1 + (- 2 / 3) * (B ** (1 / 6)) * cmath.cos(nu + (1 / 3) * cmath.acos(fracsq(A, B)))


result1 = res(0)
result2 = res(cmath.pi / 3)
result3 = res(- cmath.pi / 3)
result = [result1, result2, result3]

try:
    def pd(result):
        eps = 1e-10
        if abs(result) < eps:
            return 0
        elif isinstance(result, float):
            return result.evalf()
        else:
            return result


    print(f"\nx1={pd(result1)}\nx2={pd(result2)}\nx3={pd(result3)}")
except TypeError:
    print(f"\nx1={result1}\nx2={result2}\nx3={result3}")

finally:
    for i in result:
        eps = 1e-10  # 定义一个足够小的阈值
        if abs(a * i ** 3 + b * i ** 2 + c * i + d) < eps:
            print("小于计算机舍入误差即可视为0")
        else:
            print(a * i ** 3 + b * i ** 2 + c * i + d)
