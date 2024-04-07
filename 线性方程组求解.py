import numpy as np
from IPython.display import display, Math
from fractions import Fraction

while 1:
    try:
        ch = input("请选择方程组的未知量个数\nA.两个(ar随机)\tB.三个(br随机)\tC.余子式查看\tD.退出\n:")
        if ch == "A" or ch == "a" or ch == "ar":
            display(Math(r"其标准形式应为\begin{aligned} \begin{cases}"
                         r"& a_{11} X_1 +a_{22} X_2 & =b_1 \\"
                         r"& a_{12} X_1 +a_{21} X_2 & =b_2 "
                         r"\end{cases} \end{aligned} "))

            C_list = ["a11", "a12",
                      "a21", "a22",
                      "b1", "b2"]

            N_list = []

            if ch == "ar":
                N_list = np.random.randint(0, 20, size=(6,))
            else:
                for i in C_list:
                    N_list.append(float(input(f"请输入{i}的值\n:")))
            display(Math(r"该方程组为\begin{aligned} \begin{cases}"
                         fr"& {N_list[0]} x_1 +{N_list[1]} x_2 & ={N_list[4]} \\"
                         fr"& {N_list[2]} x_1 +{N_list[3]} x_2 & ={N_list[5]} "
                         r"\end{cases} \end{aligned} \\"))

            display(Math(r"设系数矩阵A=\begin{pmatrix} "
                         r"a_{11} & a_{12} \\"
                         r"a_{21} & a_{22} \\"
                         r"\end{pmatrix} =\begin{pmatrix}"
                         fr"{N_list[0]} & {N_list[1]} \\"
                         fr"{N_list[2]} & {N_list[3]}"
                         r"\end{pmatrix}"
                         r"\quad X^T =(x_1 ,x_2) "
                         r"\quad B^T =(b_1 ,b_2) \\"))

            display(Math(r"则有\bbox[yellow]{AX=B},现求解\bbox[yellow]{X=A^{-1}B} \\ \\"
                         r"首先我们求A的逆矩阵，即A^{-1} \\ \\"
                         r"在这之前，我们先求矩阵A中各元的余子式M_{ij} \\"
                         r"列如:M_{11} =\begin{pmatrix} "
                         r"\require{cancel} \cancel{a_{11}} & \cancel{a_{12}} \\"
                         r"\cancel{a_{21}} & a_{22} \end{pmatrix} \\"
                         r"则 M_{11}=a_{22},M_{12}=a_{21},M_{21}=a_{12},M_{22}=a_{11} \\"))
            al = N_list[0] * N_list[3] - N_list[1] * N_list[2]


            def sa(al):
                sal = "{" + str(al) + "}"
                return sal


            def de(nu):
                return nu * (1 / al)


            def det(aij, aij1, b1, b2):
                return aij * b1 + aij1 * b2


            def fenshu(x):
                return Fraction(x).limit_denominator()


            display(Math(r"接着我们求这四项的代数余子式\bbox[yellow]{\tilde{A}_{ij}=(-1)^{i+j} M_{ij}} \\"
                         r"\tilde{A}_{11}=(-1)^{1+1}M_{11}=M_{11} \\"
                         r"则\tilde{A}_{11}=M_{11},\tilde{A}_{12}=-M_{12},"
                         r"\tilde{A}_{21}=-M_{21},\tilde{A}_{22}=M_{22} \\ \\"
                         r"现求其伴随矩阵A^* \\"
                         r"A^* =\begin{pmatrix}"
                         r"\tilde{A}_{11} & \tilde{A}_{12} \\"
                         r"\tilde{A}_{21} & \tilde{A}_{22} "
                         r"\end{pmatrix} =\begin{pmatrix}"
                         r"M_{11} & -M_{12} \\"
                         r"-M_{21} & M_{22} "
                         r"\end{pmatrix} \\"
                         r"则{A^*}^T =\begin{pmatrix}"
                         r"M_{11} & -M_{21} \\"
                         r"-M_{12} & M_{22} "
                         r"\end{pmatrix} \\ \\"
                         r"最后求矩阵的逆\bbox[yellow]{A^{-1} =\frac{1}{\left| A\right|}{A^*}^T} \\"
                         r"其中|A|=det(A)="
                         fr"a_{{11}}a_{{22}}-a_{{21}}a_{{21}}={sa(al)} \\"
                         fr"则A^{{-1}} =\frac{{1}}{sa(al)}\begin{{pmatrix}}"
                         fr"{N_list[3]} & {- N_list[1]} \\"
                         fr"{- N_list[2]} & {N_list[0]} "
                         r"\end{pmatrix} "
                         r"=\begin{pmatrix} "
                         fr"{fenshu(de(N_list[3]))} & {fenshu(de(- N_list[1]))} \\"
                         fr"{fenshu(de(- N_list[2]))} & {fenshu(de(N_list[0]))} "
                         r"\end{pmatrix} \\"
                         r"代入\bbox[yellow]{x=A^{-1}B} \\"
                         r"即x=\begin{bmatrix} "
                         fr"{fenshu(de(N_list[3]))} & {fenshu(de(- N_list[1]))} \\"
                         fr"{fenshu(de(- N_list[2]))} & {fenshu(de(N_list[0]))}"
                         r"\end{bmatrix} \begin{bmatrix}"
                         fr"{N_list[4]} \\"
                         fr"{N_list[5]}"
                         r"\end{bmatrix} "
                         r"=\begin{bmatrix}"
                         fr"{fenshu(det(de(N_list[3]), de(- N_list[1]), N_list[4], N_list[5]))} \\"
                         fr"{fenshu(det(de(- N_list[2]), de(N_list[0]), N_list[4], N_list[5]))}"
                         r"\end{bmatrix} \\"
                         fr"那么x_1 ={fenshu(det(de(N_list[3]), de(- N_list[1]), N_list[4], N_list[5]))},"
                         fr"x_2 ={fenshu(det(de(- N_list[2]), de(N_list[0]), N_list[4], N_list[5]))}"))

        elif ch == "B" or ch == "b" or ch == "br":
            display(Math(r"其标准形式应为\begin{aligned} \begin{cases}"
                         r"& a_{11} x_1 +a_{22} x_2 +a_{33} x_3 & =b_1 \\"
                         r"& a_{12} x_1 +a_{23} x_2 +a_{31} x_3 & =b_2 \\"
                         r"& a_{21} x_1 +a_{32} x_2 +a_{13} x_3 & =b_3"
                         r"\end{cases} \end{aligned}"))

            C_list = ['a11', 'a12', 'a13',
                      'a21', 'a22', 'a23',
                      'a31', 'a32', 'a33',
                      'b1', 'b2', 'b3']

            N_list = []

            if ch == "br":
                N_list = np.random.randint(0, 20, size=(12,))
            else:
                for i in C_list:
                    N_list.append(float(input(f"请输入{i}的值\n:")))

            N_list1 = N_list
            N_list1 = np.reshape(N_list1, (4, 3))
            N_list1, B_list = np.vsplit(N_list1, [3])

            detA = int(np.linalg.det(N_list1))

            display(Math(r"该方程组为\begin{aligned} \begin{cases}"
                         fr"{N_list[0]} x_1 +{N_list[1]} x_2 +{N_list[2]}x_3 & ={N_list[9]} \\"
                         fr"{N_list[3]} x_1 +{N_list[4]} x_2 +{N_list[5]}x_3 & ={N_list[10]} \\"
                         fr"{N_list[6]} x_1 +{N_list[7]} x_2 +{N_list[8]}x_3 & ={N_list[11]}"
                         r"\end{cases} \end{aligned} \\"))

            display(Math(r"设系数矩阵A=\begin{pmatrix} "
                         r"a_{11} & a_{12} & a_{13} \\"
                         r"a_{21} & a_{22} & a_{23} \\"
                         r"a_{31} & a_{32} & a_{33} \\"
                         r"\end{pmatrix} =\begin{bmatrix}"
                         fr"{N_list[0]} & {N_list[1]} & {N_list[2]} \\"
                         fr"{N_list[3]} & {N_list[4]} & {N_list[5]} \\"
                         fr"{N_list[6]} & {N_list[7]} & {N_list[8]}"
                         r"\end{bmatrix}"
                         r"\quad X^\top =(x_1 ,x_2 ,x_3) "
                         r"\quad B^\top =(b_1 ,b_2 ,b_3) \\"))


            def sdet(nu, arr):
                list = []
                for i in range(0, 9):
                    if i // 3 != nu // 3 and i % 3 != nu % 3:
                        list.append(i)
                return arr[list[0]] * arr[list[3]] - arr[list[1]] * arr[list[2]]


            M_ij = []

            for i in range(0, 9):
                M_ij.append(sdet(i, N_list))

            display(Math(r"则有\bbox[yellow]{A \mathbf{X}=B},现求解\bbox[yellow]{\mathbf{X}=A^{-1}B} \\ \\"
                         r"首先我们求A的逆矩阵，即A^{-1} \\ \\"
                         r"在这之前，我们先求矩阵A中各元的余子式M_{ij} \\"
                         r"列如:M_{11} =\begin{pmatrix} "
                         r"\require{cancel} \cancel{a_{11}} & \cancel{a_{12}} & \cancel{a_{13}}\\"
                         r"\cancel{a_{21}} & a_{22} & a_{23} \\"
                         r"\cancel{a_{31}} & a_{32} & a_{33} "
                         r"\end{pmatrix} = \begin{pmatrix} "
                         r"a_{22} & a_{23} \\"
                         r"a_{32} & a_{33} \end{pmatrix}"
                         r"=a_{22} a_{33} -a_{23} a_{32} \\"
                         fr"则 M_{{11}}={M_ij[0]},M_{{12}} ={M_ij[1]} ... \\"))

            tilM_ij = []
            ctiM_ij = []
            film_ij = []

            for i in range(0, 9):
                tilM_ij.append(M_ij[i] * ((-1) ** (((i // 3) + 1) + ((i % 3) + 1))))

            for i in range(0, 9):
                ctiM_ij.append(tilM_ij[i] * (1 / detA))
                film_ij.append(Fraction(ctiM_ij[i]).limit_denominator())


            def c(arr, arr2, nu):
                return arr[nu] * arr2[0, 0] + arr[nu + 3] * arr2[0, 1] + arr[nu + 6] * arr2[0, 2]


            StrdetA = "{" + str(detA) + "}"
            display(Math(r"接着我们求这四项的代数余子式\bbox[yellow]{\tilde{A}_{ij}=(-1)^{i+j} M_{ij}} \\"
                         fr"\tilde{{A}}_{{11}}=(-1)^{{1+1}}M_{{11}}=M_{{11}}={M_ij[0]} \\"
                         fr"则\tilde{{A}}_{{11}}=M_{{11}}={M_ij[0]},\tilde{{A}}_{{12}}=-M_{{12}}={tilM_ij[1]},... \\"
                         r"现求其伴随矩阵A^* \\"
                         r"A^* =\begin{pmatrix}"
                         r"\tilde{A}_{11} & \tilde{A}_{12} & \tilde{A}_{13} \\"
                         r"\tilde{A}_{21} & \tilde{A}_{22} & \tilde{A}_{23} \\"
                         r"\tilde{A}_{31} & \tilde{A}_{32} & \tilde{A}_{33}"
                         r"\end{pmatrix} =\begin{pmatrix}"
                         r"M_{11} & -M_{12} & M_{13} \\"
                         r"-M_{21} & M_{22} & -M_{23} \\"
                         r"M_{31} & -M_{32} & M_{33}"
                         r"\end{pmatrix} \\"
                         r"则(A^*)^\top =\begin{bmatrix} "
                         fr"{tilM_ij[0]} & {tilM_ij[3]} & {tilM_ij[6]} \\"
                         fr"{tilM_ij[1]} & {tilM_ij[4]} & {tilM_ij[7]} \\"
                         fr"{tilM_ij[2]} & {tilM_ij[5]} & {tilM_ij[8]} "
                         r"\end{bmatrix} \\ \\"
                         r"现在根据\bbox[yellow]{A^{-1}=\frac{1}{det(A)} (A^{*})^\top}求矩阵的逆A^{-1} \\"
                         fr"A^{{-1}} =\frac{{1}}{StrdetA} \begin{{bmatrix}} "
                         fr"{tilM_ij[0]} & {tilM_ij[3]} & {tilM_ij[6]} \\"
                         fr"{tilM_ij[1]} & {tilM_ij[4]} & {tilM_ij[7]} \\"
                         fr"{tilM_ij[2]} & {tilM_ij[5]} & {tilM_ij[8]} "
                         r"\end{bmatrix} =\begin{bmatrix} "
                         fr"{film_ij[0]} & {film_ij[3]} & {film_ij[6]} \\"
                         fr"{film_ij[1]} & {film_ij[4]} & {film_ij[7]} \\"
                         fr"{film_ij[2]} & {film_ij[5]} & {film_ij[8]} "
                         r"\end{bmatrix} \\ \\"
                         r"最后代入\bbox[yellow]{\mathbf{x}=A^{-1}B}求解 \\"
                         r"即x=\begin{pmatrix}"
                         r"x_1 \\x_2 \\ x_3 \end{pmatrix}=\begin{bmatrix} "
                         fr"{film_ij[0]} & {film_ij[3]} & {film_ij[6]} \\"
                         fr"{film_ij[1]} & {film_ij[4]} & {film_ij[7]} \\"
                         fr"{film_ij[2]} & {film_ij[5]} & {film_ij[8]} "
                         r"\end{bmatrix} \begin{bmatrix}"
                         fr"{B_list[0, 0]} \\"
                         fr"{B_list[0, 1]} \\"
                         fr"{B_list[0, 2]} "
                         r"\end{bmatrix} =\begin{bmatrix}"
                         fr"{Fraction(c(ctiM_ij, B_list, 0)).limit_denominator()} \\"
                         fr"{Fraction(c(ctiM_ij, B_list, 1)).limit_denominator()} \\"
                         fr"{Fraction(c(ctiM_ij, B_list, 2)).limit_denominator()}"
                         r"\end{bmatrix} \\"
                         r"求得\begin{aligned} \begin{cases}"
                         fr"x_1 &={Fraction(c(ctiM_ij, B_list, 0)).limit_denominator()} \\"
                         fr"x_2 &={Fraction(c(ctiM_ij, B_list, 1)).limit_denominator()} \\"
                         fr"x_3 &={Fraction(c(ctiM_ij, B_list, 2)).limit_denominator()} "
                         r"\end{cases} \end{aligned}"))

        elif ch == "D" or ch == "d":
            break

        else:
            show_list = []
            h, l = int(input("输入查看Mij的余子式参数\n输入行数(1-3):")), int(input("输入列数(1-3):"))
            shl = "{" + str(h) + str(l) + "}"
            for i in range(0, 9):
                if i // 3 != h - 1 and i % 3 != l - 1:
                    show_list.append(i)
                else:
                    show_list.append(f"\cancel{i}")
            display(Math(fr"M_{shl}=\require{{cancel}} \begin{{pmatrix}}"
                         fr"{show_list[0]} & {show_list[1]} & {show_list[2]} \\"
                         fr"{show_list[3]} & {show_list[4]} & {show_list[5]} \\"
                         fr"{show_list[6]} & {show_list[7]} & {show_list[8]} "
                         r"\end{pmatrix}"))
    except ZeroDivisionError:
        print("出现错误:\"奇异矩阵或零矩阵导致的除零问题\"")
        continue
