import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from dataclasses import dataclass
from typing import Dict, Any
import json
import logging

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 可滚动框架类
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
       
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
       
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
       
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
       
        canvas.configure(yscrollcommand=scrollbar.set)
       
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

# 数据模型定义
@dataclass
class MotorParameters:
    Un: float  # 额定电压 (V)
    In: float  # 额定电流 (A)
    nn: float  # 额定转速 (r/min)
    p: int     # 极对数
    Da: float  # 电枢直径 (cm)
    La: float  # 电枢长度 (cm)
    delta: float  # 气隙长度 (cm)
    t_work: float  # 工作温度 (°C)
    mu_r: float  # 相对回复磁导率 mu_r

@dataclass
class PMDCParameters(MotorParameters):
    material_key: str
    material_desc: str
    lambda_est: float
    hm: float  # 永磁体厚度 (cm)
    lm: float  # 永磁体轴向长度 (mm)
    magnet_type: str
    h_pole_shoe: float  # 极靴高度 (cm)
    Q: int    # 槽数
    a: int    # 并联支路对数
    Nt: int   # 并绕根数
    u: int    # 每槽元件数
    W_c: int  # 换向原件匝数
    slot_values: Dict[str, float]  # 槽参数
    Br: float  # 永磁体剩磁大小 Br (T)
    Hc: float  # 矫顽力 Hc (kA/m)
    alpha_tem: float  # 温度系数
    H_j1: float  # 电枢轭磁场强度 H_j1 (A/m)
    Br_work: float =0.0  # 工作时剩磁密度 (T)
    Hc_work: float= 0.0  # 工作时矫顽力 (kA/m)
    Di2: float =0.0 # 转子冲片内径 (cm)
    A_m: float =0.0 # 永磁体每极磁通的截面积 (cm²)
    slot_type: str = ""  # 槽类型
    alpha_i: float = 0.0  # 极弧系数
    sita_1: float = 0.0  # 漏磁系数
    sita_prime_2: float = 0.0  # 漏磁系数

@dataclass
class PMSMParameters(MotorParameters):
    material_key: str
    material_desc: str
    hm: float
    lm: float
    h_pole_shoe: float
    Q: int
    a: int
    Nt: int
    u: int
    slot_values: Dict[str, float]
    Br: float
    Hc: float
    alpha_tem: float
    mu_r: float
    Br_work: float = 0.0
    Hc_work: float= 0.0
    D1: float = 0.0
    Di1: float= 0.0
    Di2: float = 0.0
    A_m: float = 0.0
    slot_type: str = ""
    alpha_i: float = 0.0
    sita_1: float = 0.0
    sita_prime_2: float = 0.0
    # 新增字段
    y: float = 0.0              # 节距 y
    Ht1: float = 0.0            # 齿部磁场强度 Ht1
    Ht2: float = 0.0            # 齿部磁场强度 Ht2
    Hj1: float = 0.0            # 轭部磁场强度 Hj1
    Hj2: float = 0.0            # 轭部磁场强度 Hj2
    connection_type: str = "Y"
    efficiency: float = 100.0
    power_factor: float = 1.0

@dataclass
class DiscPMDCParameters(MotorParameters):
    material_key: str
    material_desc: str
    lambda_est: float
    hm: float
    lm: float
    magnet_type: str
    h_pole_shoe: float
    Q: int
    a: int
    Nt: int
    u: int
    W_c: int
    slot_values: Dict[str, float]
    Br: float
    Hc: float
    alpha_tem: float
    mu_r: float
    Br_work: float = 0.0
    Hc_work: float = 0.0
    Di2: float = 0.0
    A_m: float = 0.0
    slot_type: str = ""
    alpha_i: float = 0.0
    sita_1: float = 0.0
    sita_prime_2: float = 0.0

# 计算器类
class PMDCCalculator:
    def __init__(self, params: PMDCParameters):
        self.params = params
        self.results = {}
       
    def calculate_L_ef(self, magnet_type): #电枢计算长度
        if magnet_type == "钕铁硼":
            return self.params.La + 2 * self.params.delta/10
        elif magnet_type == "铁氧体":
            return self.params.La + ((self.params.lm - self.params.La) / (self.params.hm + self.params.delta/10)) * (self.params.hm + self.params.delta/10)

    def calculate_bt2(self, b_t21, b_t22): #计算齿宽
        if b_t21 > b_t22:
            return (2* b_t21 + b_t22) / 3  # cm
        if b_t21 <= b_t22:
            return (b_t22+ 2* b_t21) / 3

    def calculate_A_s(self, slot_type, slot):
        if slot_type == '梨形槽':
            return (math.pi / 2) * (slot['r21']**2 + slot['r23']**2) + slot['h22'] * (slot['r21'] + slot['r21']) - slot['C_i'] * (math.pi * (slot['r21'] + slot['r22']) + 2 * slot['h22'])
        elif slot_type == "半梨形槽":
            return (math.pi / 4) * (slot['r22']**2 + slot['r23']**2) + slot['h2'] / 2 * (slot['d1'] + 2 * slot['r22']) + slot['r23'] * slot['d3'] - slot['C_i'] * (math.pi * slot['r22'] + 2 * slot['h22'] + math.sqrt((slot['d2'] - slot['b02'])**2 + 4 * slot['h22']**2))
        elif slot_type == "圆形槽":
            return math.pi * slot['r21']**2 - 2 * slot['C_i'] * math.pi * slot['r21']
        elif slot_type == "矩形槽":
            return (slot['b02'] + slot['d2']) / 2 * slot['h2'] + slot['h22'] * slot['d2'] - slot['C_i'] * (slot['d2'] + 2 * slot['h22'] + math.sqrt((slot['d2'] - slot['b02'])**2 + 4 * slot['h22']**2))
        elif slot_type == "斜肩圆底槽":
            return (math.pi / 2) * slot['r22']**2 + slot['h22'] * (slot['d1'] + 2 * slot['r22']) / 2 - slot['C_i'] * (math.pi * slot['r22'] + 2 * slot['h22'] + math.sqrt((slot['d1'] - slot['b02'])**2 + 4 * slot['h22']**2))
        else:
            raise ValueError("不支持的槽类型")

    def calculate_winding_resistance(self, N):
        if self.params.p == 1:
            Ke = 1.35
            return 0.1785*10**(-3)* N * (self.params.Da*Ke + self.params.La)/(4* self.params.a**2 )
        if self.params.p == 2:
            Ke = 1.1
            return 0.1785*10**(-3)* N * (self.params.Da*Ke + self.params.La)/(4* self.params.a**2 )
        if self.params.p > 2:
            Ke = 0.8
            return 0.1785*10**(-3)* N * (self.params.Da*Ke + self.params.La)/(4* self.params.a**2 )
        
    def calculate_Stator_yoke_magnetic_flux(self):
        sita_0 = (self.params.sita_1+self.params.sita_prime_2/self.calculate_L_ef(self.params.magnet_type))*1.09
        return sita_0
       
    def calculate(self, expected_Phi_delta: float = None):
        p = self.params.p
        Da = self.params.Da
        La = self.params.La
        delta = self.params.delta
        lm = self.params.lm
        hm = self.params.hm
        Q = self.params.Q
        a = self.params.a
        Nt = self.params.Nt
        u = self.params.u
        W_c = self.params.W_c
        Un = self.params.Un
        In = self.params.In
        nn = self.params.nn
        t_work = self.params.t_work
        magnet_type = self.params.magnet_type
        material_desc = self.params.material_desc
       
        Br_work =  self.params.Br* (1+ (t_work-20)*self.params.alpha_tem)
        Hc_work = self.params.Hc* (1+ (t_work-20)*self.params.alpha_tem)
       
        slot = self.params.slot_values
        # 计算极距 (tau)
        tau = (math.pi * Da) / (2 * p)  # 单位 cm
       
        # 计算气隙磁密
        B_prime_delta = 0.725 * self.params.Br_work
       
        # 计算电枢有效长度
        L_ef = self.calculate_L_ef(magnet_type)
       
        # 基本计算
        t2 = (math.pi * Da) / Q  # cm
        Phi_delta = self.params.alpha_i * tau * L_ef * B_prime_delta * 1e-4  # Wb
        E = Un * math.sqrt(3) / 2  # V
        f = nn * p / 60  # Hz
        kw = 0.95
        N_prime = (60 * E * a) / (nn * Phi_delta * p)  # 导体总数
        N_prime_s = N_prime / Q  # 每槽导体数
        W_s = abs(N_prime_s / (2 * u))
        Ns = 2 * W_s * u
        N = Q * Ns
        K = u * Q
        A_load = (N * In) / (2 * math.pi * a * Da)
       
        # 计算槽参数
        try:
            b_t21 = math.pi * (Da - 2 * slot['h02'] - 2 * slot['h2']) / Q - slot['d1']
            b_t22 = math.pi * (Da - 2 * slot['ht2'] / 10 + 2 * slot['r22']) / Q - 2 * slot['r22']
        except KeyError as e:
            raise KeyError(f"槽参数缺失: {e}")
       
        bt2 = self.calculate_bt2(b_t21, b_t22)
       
        # 计算槽净面积 A_s
        slot_type = self.params.slot_type
        A_s = self.calculate_A_s(slot_type, slot)
       
        # 计算槽满率 S_f
        S_f = (Nt * Ns) / A_s * 100  # %
       
        # 计算绕组电阻 Ra
        Ra = self.calculate_winding_resistance(N)
       
        # 计算电枢轭有效高 h_j21
        h_j2 = (Da - 2 * slot['ht2'] / 10 - self.params.Di2) / 2  # cm
        h_j21 = h_j2 + self.params.Di2 / 8  # cm
       
        # 计算气隙系数和气隙磁密
        try:
            ratio = slot['b02'] / (hm + delta / 10)
            sita_s = (2 / math.pi) * (math.atan(0.5 * ratio) - (1 / ratio) -
                                      (1 / ratio) * math.log(1 + (ratio ** 2) / 2))
        except ZeroDivisionError:
            raise ZeroDivisionError("槽口宽度 b02 或 (hm + delta/10) 为零，无法计算 sita_s。")
       
        K_deltam = t2 / (t2 - sita_s * slot['b02'])
        ratio_hmdelta = (10 * hm) / delta
        K_delta = K_deltam + (K_deltam - 1) * ratio_hmdelta
           
        # 计算电枢齿磁密 B_t2
        F_delta = 1.6 * K_delta * delta * B_prime_delta * 1e3
        B_t2 = (t2 * L_ef * B_prime_delta) / (bt2 * La * 0.95)
       
        # 获取用户输入的 H_j1
        H_j1 = self.params.H_j1  # 从参数中获取 H_j1 (A/cm)
       
        # 计算
        F_j1 = math.pi * (Da - slot['r21']) / (2 * p) * H_j1
        Sigma_F = F_delta + F_j1  # 磁动势总和
       
        # 负载工作点计算
        Caplambda_delta = Phi_delta / Sigma_F if Sigma_F != 0 else 0
        Caplambda_b = (self.params.Br_work * self.params.A_m) / (self.params.Hc_work * 2 * hm) * 1e-5  # 磁导基值
        lambda_delta = Caplambda_delta / Caplambda_b if Caplambda_b != 0 else 0  # 主磁导标值
        lambda_n = 1.09 * (self.params.sita_1 + (self.params.sita_prime_2 / L_ef + 1) - 1) * lambda_delta if lambda_delta !=0 else 0
       
        F_a = 0.02 * A_load
        denom = (10 * 1.09 * (self.params.sita_1 + (self.params.sita_prime_2 / L_ef + 1) - 1) * self.params.Hc_work * 2 * hm)
        f_prime_a = 2 * F_a / denom if denom != 0 else 0
        bm_N = lambda_n * (1 - f_prime_a) / (1 + lambda_n) if (1 + lambda_n) !=0 else 0
        hm_N = (lambda_n * f_prime_a + 1) / (1 + lambda_n) if (1 + lambda_n) !=0 else 0
        realPhi_delta = bm_N * self.params.Br_work * self.params.A_m / (1.09 * (self.params.sita_1 + (self.params.sita_prime_2 / L_ef + 1) -1) * 1e4) if (1.09 * (self.params.sita_1 + (self.params.sita_prime_2 / L_ef + 1) -1) * 1e4) !=0 else 0
       
        # 迭代调整 Phi_delta
        tolerance = 0.5
        max_iterations = 500
        iteration = 0
       
        while iteration < max_iterations:
            logging.debug(f"Iteration {iteration}: Phi_delta={Phi_delta}, realPhi_delta={realPhi_delta}")
            if expected_Phi_delta is not None:
                if abs(expected_Phi_delta - Phi_delta) < tolerance:
                    break
            else:
                if abs(Phi_delta - realPhi_delta) < tolerance:
                    break
            Phi_delta = (Phi_delta + realPhi_delta) / 2
            Caplambda_delta = Phi_delta / Sigma_F if Sigma_F != 0 else 0
            lambda_delta = Caplambda_delta / Caplambda_b if Caplambda_b != 0 else 0
            lambda_n = 1.09 * (self.params.sita_1 + (self.params.sita_prime_2 / L_ef + 1) - 1) * lambda_delta if lambda_delta !=0 else 0
            bm_N = lambda_n * (1 - f_prime_a) / (1 + lambda_n) if (1 + lambda_n) !=0 else 0
            realPhi_delta = bm_N * self.params.Br_work * self.params.A_m / (1.09 * (self.params.sita_1 + (self.params.sita_prime_2 / L_ef + 1) -1) * 1e4) if (1.09 * (self.params.sita_1 + (self.params.sita_prime_2 / L_ef + 1) -1) * 1e4) !=0 else 0
            iteration += 1
            logging.debug(f"After iteration {iteration}: Phi_delta={Phi_delta}, realPhi_delta={realPhi_delta}")
       
        # 保存结果
        self.results = {
            "极距 tau": f"{tau:.2f} cm",
            "预计满载磁通 Phi_delta": f"{Phi_delta:.6f} Wb",
            "预计导体总数 N'": f"{N_prime:.2f}",
            "每原件匝数 W_s": f"{W_s:.2f}",
            "实际每槽导体数 Ns": f"{Ns:.2f}",
            "实际导体总数 N": f"{N:.2f}",
            "换向片数 K": f"{K}",
            "实际电负荷 A": f"{A_load:.2f} A/cm",
            "槽净面积 A_s": f"{A_s:.2f} mm²",
            "槽满率 S_f": f"{S_f:.2f} %",
            "绕组电阻 Ra": f"{Ra:.6f} Ω",
            "电枢轭有效高 h_j21": f"{h_j21:.4f} cm",
            "气隙系数 sita_s": f"{sita_s:.4f}",
            "K_delta": f"{K_delta:.4f}",
            "气隙磁密 B_delta": f"{B_prime_delta:.4f} T",
            "电枢齿磁密 B_t2": f"{B_t2:.4f} T",
            # "电枢轭磁密 B_j2": f"{B_j2:.4f} T",  # 需要定义 B_j2
            "电枢轭磁密 B_j": f"{self.calculate_Stator_yoke_magnetic_flux():.4f} T",  # 需要定义 calculate_B_j 方法
            "外磁路总磁位差Sigma_F": f"{Sigma_F:.4f}",
            "气隙主磁导": f"{lambda_delta:.6f}",
            "外磁路总磁导": f"{lambda_n:.6f}",
            "实际满载磁通": f"{realPhi_delta:.6f} Wb",
            "迭代次数": f"{iteration}"
        }

class PMSMCalculator:
    def __init__(self, params: PMSMParameters):
        self.params = params
        self.results = {}
   
    def calculate(self):
        """
        永磁同步电动机的计算逻辑。
        计算基于输入参数，并考虑新增的计算字段。
        """
        try:
            logging.debug("开始 PMSM 计算")
            Un = self.params.Un
            In = self.params.In
            nn = self.params.nn
            p = self.params.p
            Br_work = self.params.Br_work
            Hc_work = self.params.Hc_work
            A_m = self.params.A_m
            delta = self.params.delta
            Q = self.params.Q
            a = self.params.a
            Nt = self.params.Nt
            u = self.params.u
            slot = self.params.slot_values
            # 使用新增的参数 y, Ht1, Ht2, Hj1, Hj2
            y = self.params.y
            Ht1 = self.params.Ht1
            Ht2 = self.params.Ht2
            Hj1 = self.params.Hj1
            Hj2 = self.params.Hj2
            # 这里可以根据实际需求使用这些参数进行计算
            # 示例计算：
            Phi_delta = Br_work * A_m  # 假设 Phi_delta = Br_work * A_m
            omega = 2 * math.pi * nn / 60  # 转速转换为角速度 (rad/s)
            T = (3 * p / 2) * (Phi_delta * In) / (math.pi * delta)  # 扭矩计算示例公式（需根据实际调整）
        
            # 扭矩密度
            torque_density = T / (math.pi * (self.params.h_pole_shoe / 2) ** 2)  # 示例公式
        
            # 输出功率计算
            P_out = T * omega  # W
            # 输入功率计算
            P_in = P_out / (efficiency / 100) if efficiency != 0 else 0.0  # W
        
            # 计算效率（如果需要，可以调整为实际计算方式）
            efficiency_computed = (P_out / P_in) * 100 if P_in != 0 else 0.0  # %
        
            # 保存结果
            self.results = {
                "扭矩 T": f"{T:.4f} N·m",
                "输出功率 P_out": f"{P_out:.4f} W",
                "输入功率 P_in": f"{P_in:.4f} W",
                "效率": f"{efficiency_computed:.2f} %",
                "转矩密度": f"{torque_density:.4f} N·m/cm²",
                "线电压 Un": f"{Un:.2f} V",
                "线电流 In": f"{In:.2f} A",
                "节距 y": f"{y:.2f} cm",
                "齿部磁场强度 Ht1": f"{Ht1:.2f} A/m",
                "齿部磁场强度 Ht2": f"{Ht2:.2f} A/m",
                "轭部磁场强度 Hj1": f"{Hj1:.2f} A/m",
                "轭部磁场强度 Hj2": f"{Hj2:.2f} A/m",
            }
            logging.debug("PMSM 计算完成")
        except Exception as e:
            logging.error(f"PMSM 计算错误: {e}")
            raise e

class DiscPMDCCalculator:
    def __init__(self, params: DiscPMDCParameters):
        self.params = params
        self.results = {}
   
    def calculate(self):
        """
        线绕盘式永磁直流电机的计算逻辑。
        使用简化的计算公式作为示例。
        """
        Un = self.params.Un
        In = self.params.In
        nn = self.params.nn
        p = self.params.p
        Br_work = self.params.Br_work
        Hc_work = self.params.Hc_work
        A_m = self.params.A_m
        La = self.params.La
        delta = self.params.delta
        Q = self.params.Q
        a = self.params.a
        Nt = self.params.Nt
        u = self.params.u
        W_c = self.params.W_c
        slot = self.params.slot_values
       
        # 假设 Phi_delta = Br_work * A_m
        Phi_delta = Br_work * A_m  # Wb
        # 扭矩计算示例公式
        T = (Br_work * A_m * In) / La  # N·m
       
        # 转矩密度
        torque_density = T / (math.pi * (self.params.Da / 2)**2)  # N·m/cm²
       
        # 功率计算
        P_out = T * (nn / 60) * (math.pi * self.params.Da / 100)  # W
        P_in = Un * In  # W
        efficiency = (P_out / P_in) * 100 if P_in != 0 else 0.0  # %
       
        # 保存结果
        self.results = {
            "扭矩 T": f"{T:.4f} N·m",
            "输出功率 P_out": f"{P_out:.4f} W",
            "输入功率 P_in": f"{P_in:.4f} W",
            "效率": f"{efficiency:.2f} %",
            "转矩密度": f"{torque_density:.4f} N·m/cm²"
        }

# 主应用类
class MotorDesignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("电机设计计算程序")
        self.root.geometry("1600x900")  # 增加宽度以容纳更多元素
       
        # 创建主菜单
        self.create_menu()
       
        # 创建主框架（可滚动）
        self.main_frame = ScrollableFrame(root)
        self.main_frame.pack(fill="both", expand=True)
       
        # 初始化电机数据存储
        self.motor_data = {}
   
    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
       
        # 文件菜单
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="保存", command=self.save_data)
        file_menu.add_command(label="加载", command=self.load_data)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
       
        # 电机类型菜单
        motor_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="电机类型", menu=motor_menu)
        motor_menu.add_command(label="永磁直流电机", command=self.show_pmdc_design)
        motor_menu.add_command(label="异步起动的永磁同步电动机", command=self.show_pmsm_design)
        motor_menu.add_command(label="线绕盘式永磁直流电机", command=self.show_disc_pmdc_design)
       
        # 帮助菜单
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_command(label="关于", command=self.show_about)
   
    def save_data(self):
        """
        保存当前输入的数据到JSON文件。
        """
        data = {k: var.get() for k, var in self.motor_data.items()}
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"),
                                                            ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("保存成功", f"数据已保存到 {file_path}")
            except Exception as e:
                messagebox.showerror("保存失败", f"无法保存文件: {e}")
   
    def load_data(self):
        """
        从JSON文件加载数据到输入框。
        """
        file_path = filedialog.askopenfilename(defaultextension=".json",
                                               filetypes=[("JSON files", "*.json"),
                                                          ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for k, v in data.items():
                    if k in self.motor_data:
                        self.motor_data[k].set(v)
                messagebox.showinfo("加载成功", f"数据已从 {file_path} 加载。")
            except Exception as e:
                messagebox.showerror("加载失败", f"无法加载文件: {e}")
   
    def show_pmdc_design(self):
        """
        显示永磁直流电机设计界面。
        """
        # 清空主框架的可滚动区域
        for widget in self.main_frame.scrollable_frame.winfo_children():
            widget.destroy()
       
        # 创建永磁直流电机设计界面
        self.create_pmdc_interface()
   
    def create_pmdc_interface(self):
        """
        创建永磁直流电机设计界面。
        """
        # 创建标签框架
        basic_params = ttk.LabelFrame(self.main_frame.scrollable_frame, text="基本参数", padding="10")
        basic_params.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
       
        # 基本参数输入
        param_fields = [
            ("额定电压 (V)", "Un"),
            ("额定电流 (A)", "In"),
            ("额定转速 (r/min)", "nn"),
            ("极对数 p", "p"),
            ("电枢直径 Da (cm)", "Da"),
            ("电枢长度 La (cm)", "La"),
            ("气隙长度 delta (cm)", "delta"),
            ("工作温度 t_work (°C)", "t_work")
        ]
       
        for idx, (label, var_name) in enumerate(param_fields):
            self.create_label_entry(basic_params, label, var_name, idx)
       
        # 铁芯材料选择
        material_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="铁芯材料选择", padding="10")
        material_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        material_desc = {
            "1": "0.5mm厚热轧硅钢片 (B25=1.47T)",
            "2": "0.5mm厚热轧硅钢片 (B25=1.54T)",
            "3": "0.5mm厚热轧硅钢片 (B25=1.57T)",
            "4": "DW540-50",
            "5": "DW465-50",
            "6": "DW360-50",
            "7": "DW315-50",
            "8": "厚度1-1.75mm的钢板",
            "9": "铸钢或厚钢板",
            "10": "10号钢"
        }
        ttk.Label(material_frame, text="请选择铁芯材料：").grid(row=0, column=0, sticky=tk.W)
        self.material_var = tk.StringVar()
        material_combo = ttk.Combobox(material_frame, textvariable=self.material_var, state="readonly")
        material_combo['values'] = [f"{k}. {v}" for k, v in material_desc.items()]
        material_combo.grid(row=1, column=0, padx=5, pady=5)
        material_combo.current(0)
        self.material_desc_map = material_desc  # 保存映射关系
       
        # 其他参数输入
        other_params = ttk.LabelFrame(self.main_frame.scrollable_frame, text="其他参数", padding="10")
        other_params.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        other_fields = [
            ("长径比预估值 lambda", "lambda_est"),
            ("永磁体厚度 hm (cm)", "hm"),
            ("永磁体轴向长度 lm (mm)", "lm"),
            ("永磁体类型 (钕铁硼/铁氧体)", "magnet_type"),
            ("极靴高度 h_pole_shoe (cm)", "h_pole_shoe"),
            ("槽数 Q", "Q"),
            ("电枢绕组的并联支路对数 a", "a"),
            ("并绕根数 Nt", "Nt"),
            ("每槽元件数 u", "u"),
            ("换向原件匝数 W_c", "W_c")
        ]
        for idx, (label, var_name) in enumerate(other_fields):
            self.create_label_entry(other_params, label, var_name, idx)
       
        # 槽参数输入
        slot_params = [
            ("槽口宽度 b02 (cm)", 'b02'),
            ("槽口高度 h02 (cm)", 'h02'),
            ("槽上部半径 r21 (cm)", 'r21'),
            ("槽下部半径 r22 (cm)", 'r22'),
            ("槽上部倒角半径 r23 (cm)", 'r23'),
            ("槽上部高度 h2 (cm)", 'h2'),
            ("槽上部宽度 d1 (cm)", 'd1'),
            ("槽中部宽度 h22 (cm)", 'h22'),
            ("槽下部宽度 d2 (cm)", 'd2'),
            ("槽上部倒角圆心距 d3 (cm)", 'd3'),
            ("槽高 ht2 (cm)", 'ht2'),
            ("槽绝缘厚度 C_i (cm)", 'C_i'),
            ("机壳厚度 h_j (cm)", 'h_j'),
            ("机壳长度 L_j (cm)", 'L_j'),
            ("转子冲片内径 Di2 (cm)", 'Di2'),
            ("永磁体每极磁通的截面积 A_m (cm²)", 'A_m')
        ]
        slot_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="槽参数", padding="10")
        slot_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        for idx, (label_text, var_name) in enumerate(slot_params):
            self.create_label_entry(slot_frame, label_text, var_name, idx)
       
        # 槽类型选择
        slot_type_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="槽类型选择", padding="10")
        slot_type_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.slot_type_var = tk.StringVar()
        slot_types = ["梨形槽", "半梨形槽", "圆形槽", "矩形槽", "斜肩圆底槽"]
        slot_type_combo = ttk.Combobox(slot_type_frame, textvariable=self.slot_type_var, state="readonly")
        slot_type_combo['values'] = slot_types
        slot_type_combo.grid(row=0, column=0, padx=5, pady=5)
        slot_type_combo.current(0)
       
        # 永磁体参数
        pmm_parameters = ttk.LabelFrame(self.main_frame.scrollable_frame, text="永磁体参数", padding="10")
        pmm_parameters.grid(row=5, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        pmm_fields = [
            ("永磁体剩磁大小 Br (T)", "Br"),
            ("矫顽力 Hc (kA/m)", "Hc"),
            ("相对回复磁导率 mu_r", "mu_r"),
            ("温度系数 alpha_tem (例如：-0.07)", "alpha_tem")
        ]
        for idx, (label, var_name) in enumerate(pmm_fields):
            self.create_label_entry(pmm_parameters, label, var_name, idx)
       
        # 计算参数输入
        calc_params_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="计算参数", padding="10")
        calc_params_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        calc_fields = [
            ("极弧系数 alpha_i（一般范围0.6～0.8）", "alpha_i"),
            ("漏磁系数 sita_1", "sita_1"),
            ("漏磁系数 sita'_2", "sita_prime_2"),
            ("电枢轭磁场强度 H_j1 (A/m)", "H_j1")  # 新增字段
        ]
        for idx, (label, var_name) in enumerate(calc_fields):
            self.create_label_entry(calc_params_frame, label, var_name, idx)
       
        # 预期 Phi_delta 输入（可选）
        expected_phi_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="预期磁通密度 Phi_delta (Wb)", padding="10")
        expected_phi_frame.grid(row=7, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Label(expected_phi_frame, text="请输入预期磁通密度 Phi_delta (Wb)（可选）：").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.expected_phi_var = tk.StringVar()
        expected_phi_entry = ttk.Entry(expected_phi_frame, textvariable=self.expected_phi_var)
        expected_phi_entry.grid(row=0, column=1, padx=5, pady=2)
       
        # 计算按钮
        ttk.Button(self.main_frame.scrollable_frame, text="开始计算", command=self.calculate_pmdc).grid(row=8, column=0, pady=10)
       
        # 结果展示
        result_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="计算结果", padding="10")
        result_frame.grid(row=0, column=1, rowspan=9, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)
        self.result_text = tk.Text(result_frame, width=80, height=40, wrap='word')
        self.result_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        result_scroll = ttk.Scrollbar(result_frame, orient='vertical', command=self.result_text.yview)
        result_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text['yscrollcommand'] = result_scroll.set
   
    def show_pmsm_design(self):
        """
        显示异步起动的永磁同步电动机设计界面。
        """
        # 清空主框架的可滚动区域
        for widget in self.main_frame.scrollable_frame.winfo_children():
            widget.destroy()
       
        # 创建异步起动的永磁同步电动机设计界面
        self.create_pmsm_interface()
   
    def create_pmsm_interface(self):
        """
        创建异步起动的永磁同步电动机设计界面。
        """
        # 创建标签框架
        basic_params = ttk.LabelFrame(self.main_frame.scrollable_frame, text="基本参数", padding="10")
        basic_params.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
       
        # 基本参数输入
        param_fields = [
            ("额定转速 (r/min)", "nn"),
            ("极对数 p", "p"),
            ("定子外径 D1 (cm)", "D1"),
            ("定子内径 Di1 (cm)", "Di1"),
            ("转子内径 Di2 (cm)", "Di2"),
            ("气隙长度 delta (cm)", "delta"),
            ("工作温度 t_work (°C)", "t_work")
        ]
       
        for idx, (label, var_name) in enumerate(param_fields):
            self.create_label_entry(basic_params, label, var_name, idx)
       
       # 新增额定相电压输入
        phase_voltage_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="额定相电压", padding="10")
        phase_voltage_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.V_phase_var = tk.StringVar()
        ttk.Label(phase_voltage_frame, text="额定相电压 V_phase (V)：").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        phase_voltage_entry = ttk.Entry(phase_voltage_frame, textvariable=self.V_phase_var)
        phase_voltage_entry.grid(row=0, column=1, padx=5, pady=2)
   
        # 新增连接类型选择
        connection_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="连接类型", padding="10")
        connection_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Label(connection_frame, text="请选择连接类型：").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.connection_type_var = tk.StringVar()
        connection_combo = ttk.Combobox(connection_frame, textvariable=self.connection_type_var, state="readonly")
        connection_combo['values'] = ["Y", "Δ"]
        connection_combo.grid(row=0, column=1, padx=5, pady=2)
        connection_combo.current(0)
   
        # 新增额定效率和功率因数输入
        efficiency_pf_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="额定效率与功率因数", padding="10")
        efficiency_pf_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
   
        ttk.Label(efficiency_pf_frame, text="额定效率 (%)：").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.efficiency_var = tk.StringVar()
        efficiency_entry = ttk.Entry(efficiency_pf_frame, textvariable=self.efficiency_var)
        efficiency_entry.grid(row=0, column=1, padx=5, pady=2)
        self.efficiency_var.set("100")  # 默认值
   
        ttk.Label(efficiency_pf_frame, text="额定功率因数：").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.power_factor_var = tk.StringVar()
        power_factor_entry = ttk.Entry(efficiency_pf_frame, textvariable=self.power_factor_var)
        power_factor_entry.grid(row=1, column=1, padx=5, pady=2)
        self.power_factor_var.set("1.0")  # 默认值
       
        # 铁芯材料选择
        material_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="铁芯材料选择", padding="10")
        material_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        material_desc = {
            "1": "0.5mm厚热轧硅钢片 (B25=1.47T)",
            "2": "0.5mm厚热轧硅钢片 (B25=1.54T)",
            "3": "0.5mm厚热轧硅钢片 (B25=1.57T)",
            "4": "DW540-50",
            "5": "DW465-50",
            "6": "DW360-50",
            "7": "DW315-50",
            "8": "厚度1-1.75mm的钢板",
            "9": "铸钢或厚钢板",
            "10": "10号钢"
        }
        ttk.Label(material_frame, text="请选择铁芯材料：").grid(row=0, column=0, sticky=tk.W)
        self.material_var_pmsm = tk.StringVar()
        material_combo = ttk.Combobox(material_frame, textvariable=self.material_var_pmsm, state="readonly")
        material_combo['values'] = [f"{k}. {v}" for k, v in material_desc.items()]
        material_combo.grid(row=1, column=0, padx=5, pady=5)
        material_combo.current(0)
        self.material_desc_map_pmsm = material_desc  # 保存映射关系
       
        # 其他参数输入
        other_params = ttk.LabelFrame(self.main_frame.scrollable_frame, text="其他参数", padding="10")
        other_params.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        other_fields = [
            ("长径比预估值 lambda", "lambda_est"),
            ("永磁体厚度 hm (cm)", "hm"),
            ("永磁体轴向长度 lm (mm)", "lm"),
            ("极靴高度 h_pole_shoe (cm)", "h_pole_shoe"),
            ("槽数 Q", "Q"),
            ("电枢绕组的并联支路对数 a", "a"),
            ("并绕根数 Nt", "Nt"),
            ("每槽元件数 u", "u"),
            ("换向原件匝数 W_c", "W_c")
        ]
        for idx, (label, var_name) in enumerate(other_fields):
            self.create_label_entry(other_params, label, var_name, idx)
       
        # 槽参数输入
        slot_params = [
            ("定子槽口宽度 b01 (cm)", 'b01'),
            ("定子槽口高度 h01 (cm)", 'h01'),
            ("转子槽口宽度 b02 (cm)", 'b02'),
            ("转子槽口高度 h02 (cm)", 'h02'),
            ("转子槽上部半径 br1 (cm)", 'br1'),
            ("转子槽下部宽度 br2 (cm)", 'br2'),
            ("槽上部倒角半径 r23 (cm)", 'r23'),
            ("转子槽主体高度（不包含槽口） hr12 (cm)", 'hr12'),
            ("槽中部宽度 h22 (cm)", 'h22'),
            ("槽高 ht2 (cm)", 'ht2'),
            ("转子冲片内径 Di2 (cm)", 'Di2'),
            ("永磁体每极磁通的截面积 A_m (cm²)", 'A_m')
        ]
        slot_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="槽参数", padding="10")
        slot_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        for idx, (label_text, var_name) in enumerate(slot_params):
            self.create_label_entry(slot_frame, label_text, var_name, idx)
       
        # 槽类型选择
        slot_type_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="槽类型选择", padding="10")
        slot_type_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.slot_type_var_pmsm = tk.StringVar()
        slot_types = ["平底槽", "圆底槽", "圆形槽"]
        slot_type_combo = ttk.Combobox(slot_type_frame, textvariable=self.slot_type_var_pmsm, state="readonly")
        slot_type_combo['values'] = slot_types
        slot_type_combo.grid(row=0, column=0, padx=5, pady=5)
        slot_type_combo.current(0)
       
        # 永磁体参数
        pmm_parameters = ttk.LabelFrame(self.main_frame.scrollable_frame, text="永磁体参数", padding="10")
        pmm_parameters.grid(row=5, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        pmm_fields = [
            ("永磁体剩磁大小 Br (T)", "Br"),
            ("矫顽力 Hc (kA/m)", "Hc"),
            ("相对回复磁导率 mu_r", "mu_r"),
            ("温度系数 alpha_tem (例如：-0.07)", "alpha_tem")
        ]
        for idx, (label, var_name) in enumerate(pmm_fields):
            self.create_label_entry(pmm_parameters, label, var_name, idx)
       
        # 计算参数输入
        calc_params_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="计算参数", padding="10")
        calc_params_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        calc_fields = [
            ("极弧系数 alpha_i（一般范围0.6～0.8）", "alpha_i"),
            ("漏磁系数 sita_1", "sita_1"),
            ("漏磁系数 sita'_2", "sita_prime_2"),
            ("电枢轭磁场强度 H_j1 (A/m)", "H_j1")  # 新增字段
        ]
        for idx, (label, var_name) in enumerate(calc_fields):
            self.create_label_entry(calc_params_frame, label, var_name, idx)

        # 新增节距 y, 齿部磁场强度 Ht1, Ht2, 轭部磁场强度 Hj1, Hj2
        additional_params = ttk.LabelFrame(self.main_frame.scrollable_frame, text="新增参数", padding="10")
        additional_params.grid(row=4, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        additional_fields = [
            ("节距 y (cm)", "y"),
            ("齿部磁场强度 Ht1 (A/m)", "Ht1"),
            ("齿部磁场强度 Ht2 (A/m)", "Ht2"),
            ("轭部磁场强度 Hj1 (A/m)", "Hj1"),
            ("轭部磁场强度 Hj2 (A/m)", "Hj2")
        ]
        for idx, (label, var_name) in enumerate(additional_fields):
            self.create_label_entry(additional_params, label, var_name, idx)
            
        # 预期 Phi_delta 输入（可选）
        expected_phi_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="预期磁通密度 Phi_delta (Wb)", padding="10")
        expected_phi_frame.grid(row=7, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Label(expected_phi_frame, text="请输入预期磁通密度 Phi_delta (Wb)（可选）：").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.expected_phi_var = tk.StringVar()
        expected_phi_entry = ttk.Entry(expected_phi_frame, textvariable=self.expected_phi_var)
        expected_phi_entry.grid(row=0, column=1, padx=5, pady=2)
       
        # 计算按钮
        ttk.Button(self.main_frame.scrollable_frame, text="开始计算", command=self.calculate_pmdc).grid(row=8, column=0, pady=10)
       
        # 结果展示
        result_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="计算结果", padding="10")
        result_frame.grid(row=0, column=1, rowspan=9, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)
        self.result_text = tk.Text(result_frame, width=80, height=40, wrap='word')
        self.result_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        result_scroll = ttk.Scrollbar(result_frame, orient='vertical', command=self.result_text.yview)
        result_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text['yscrollcommand'] = result_scroll.set

    def show_disc_pmdc_design(self):
        """
        显示线绕盘式永磁直流电机设计界面。
        """
        # 清空主框架的可滚动区域
        for widget in self.main_frame.scrollable_frame.winfo_children():
            widget.destroy()
       
        # 创建线绕盘式永磁直流电机设计界面
        self.create_disc_pmdc_interface()
   
    def create_disc_pmdc_interface(self):
        """
        创建线绕盘式永磁直流电机设计界面。
        """
        # 创建标签框架
        basic_params = ttk.LabelFrame(self.main_frame.scrollable_frame, text="基本参数", padding="10")
        basic_params.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
       
        # 基本参数输入
        param_fields = [
            ("额定电压 (V)", "Un"),
            ("额定电流 (A)", "In"),
            ("额定转速 (r/min)", "nn"),
            ("极对数 p", "p"),
            ("圆盘直径 Da (cm)", "Da"),
            ("圆盘长度 La (cm)", "La"),
            ("气隙长度 delta (cm)", "delta"),
            ("工作温度 t_work (°C)", "t_work")
        ]
       
        for idx, (label, var_name) in enumerate(param_fields):
            self.create_label_entry_disc_pmdc(basic_params, label, var_name, idx)
       
        # 铁芯材料选择
        material_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="铁芯材料选择", padding="10")
        material_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        material_desc = {
            "1": "0.5mm厚热轧硅钢片 (B25=1.47T)",
            "2": "0.5mm厚热轧硅钢片 (B25=1.54T)",
            "3": "0.5mm厚热轧硅钢片 (B25=1.57T)",
            "4": "DW540-50",
            "5": "DW465-50",
            "6": "DW360-50",
            "7": "DW315-50",
            "8": "厚度1-1.75mm的钢板",
            "9": "铸钢或厚钢板",
            "10": "10号钢"
        }
        ttk.Label(material_frame, text="请选择铁芯材料：").grid(row=0, column=0, sticky=tk.W)
        self.material_var_disc_pmdc = tk.StringVar()
        material_combo = ttk.Combobox(material_frame, textvariable=self.material_var_disc_pmdc, state="readonly")
        material_combo['values'] = [f"{k}. {v}" for k, v in material_desc.items()]
        material_combo.grid(row=1, column=0, padx=5, pady=5)
        material_combo.current(0)
        self.material_desc_map_disc_pmdc = material_desc  # 保存映射关系
       
        # 其他参数输入
        other_params = ttk.LabelFrame(self.main_frame.scrollable_frame, text="其他参数", padding="10")
        other_params.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        other_fields = [
            ("长径比预估值 lambda", "lambda_est"),
            ("永磁体厚度 hm (cm)", "hm"),
            ("永磁体轴向长度 lm (mm)", "lm"),
            ("永磁体类型 (钕铁硼/铁氧体)", "magnet_type"),
            ("极靴高度 h_pole_shoe (cm)", "h_pole_shoe"),
            ("槽数 Q", "Q"),
            ("电枢绕组的并联支路对数 a", "a"),
            ("并绕根数 Nt", "Nt"),
            ("每槽元件数 u", "u"),
            ("换向原件匝数 W_c", "W_c")
        ]
        for idx, (label, var_name) in enumerate(other_fields):
            self.create_label_entry_disc_pmdc(other_params, label, var_name, idx)
       
        # 槽参数输入
        slot_params = [
            ("槽口宽度 b02 (cm)", 'b02'),
            ("槽口高度 h02 (cm)", 'h02'),
            ("槽上部半径 r21 (cm)", 'r21'),
            ("槽下部半径 r22 (cm)", 'r22'),
            ("槽上部倒角半径 r23 (cm)", 'r23'),
            ("槽上部高度 h2 (cm)", 'h2'),
            ("槽上部宽度 d1 (cm)", 'd1'),
            ("槽中部宽度 h22 (cm)", 'h22'),
            ("槽下部宽度 d2 (cm)", 'd2'),
            ("槽上部倒角圆心距 d3 (cm)", 'd3'),
            ("槽高 ht2 (cm)", 'ht2'),
            ("槽绝缘厚度 C_i (cm)", 'C_i'),
            ("机壳厚度 h_j (cm)", 'h_j'),
            ("机壳长度 L_j (cm)", 'L_j'),
            ("转子冲片内径 Di2 (cm)", 'Di2'),
            ("永磁体每极磁通的截面积 A_m (cm²)", 'A_m')
        ]
        slot_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="槽参数", padding="10")
        slot_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        for idx, (label_text, var_name) in enumerate(slot_params):
            self.create_label_entry(slot_frame, label_text, var_name, idx)
       
        # 槽类型选择
        slot_type_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="槽类型选择", padding="10")
        slot_type_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.slot_type_var_pmsm = tk.StringVar()
        slot_types = ["梨形槽", "半梨形槽", "圆形槽", "矩形槽", "圆底槽"]
        slot_type_combo = ttk.Combobox(slot_type_frame, textvariable=self.slot_type_var_pmsm, state="readonly")
        slot_type_combo['values'] = slot_types
        slot_type_combo.grid(row=0, column=0, padx=5, pady=5)
        slot_type_combo.current(0)
       
        # 永磁体参数
        pmm_parameters = ttk.LabelFrame(self.main_frame.scrollable_frame, text="永磁体参数", padding="10")
        pmm_parameters.grid(row=5, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        pmm_fields = [
            ("永磁体剩磁大小 Br (T)", "Br"),
            ("矫顽力 Hc (kA/m)", "Hc"),
            ("相对回复磁导率 mu_r", "mu_r"),
            ("温度系数 alpha_tem (例如：-0.07)", "alpha_tem")
        ]
        for idx, (label, var_name) in enumerate(pmm_fields):
            self.create_label_entry(pmm_parameters, label, var_name, idx)
       
        
        # 计算参数输入
        calc_params_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="计算参数", padding="10")
        calc_params_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        calc_fields = [
            ("极弧系数 alpha_i（一般范围0.6～0.8）", "alpha_i"),
            ("漏磁系数 sita_1", "sita_1"),
            ("漏磁系数 sita'_2", "sita_prime_2"),
            ("电枢轭磁场强度 H_j1 (A/m)", "H_j1")  # 新增字段
        ]
        for idx, (label, var_name) in enumerate(calc_fields):
            self.create_label_entry(calc_params_frame, label, var_name, idx)
       
        # 预期 Phi_delta 输入（可选）
        expected_phi_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="预期磁通密度 Phi_delta (Wb)", padding="10")
        expected_phi_frame.grid(row=7, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Label(expected_phi_frame, text="请输入预期磁通密度 Phi_delta (Wb)（可选）：").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.expected_phi_var = tk.StringVar()
        expected_phi_entry = ttk.Entry(expected_phi_frame, textvariable=self.expected_phi_var)
        expected_phi_entry.grid(row=0, column=1, padx=5, pady=2)
       
        # 计算按钮
        ttk.Button(self.main_frame.scrollable_frame, text="开始计算", command=self.calculate_pmdc).grid(row=8, column=0, pady=10)
       
        # 结果展示
        result_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="计算结果", padding="10")
        result_frame.grid(row=0, column=1, rowspan=9, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)
        self.result_text = tk.Text(result_frame, width=80, height=40, wrap='word')
        self.result_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        result_scroll = ttk.Scrollbar(result_frame, orient='vertical', command=self.result_text.yview)
        result_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text['yscrollcommand'] = result_scroll.set
   
    def show_pmsm_design(self):
        """
        显示异步起动的永磁同步电动机设计界面。
        """
        # 清空主框架的可滚动区域
        for widget in self.main_frame.scrollable_frame.winfo_children():
            widget.destroy()
       
        # 创建异步起动的永磁同步电动机设计界面
        self.create_pmsm_interface()
   
    def create_pmsm_interface(self):
        """
        创建异步起动的永磁同步电动机设计界面。
        """
        # 创建标签框架
        basic_params = ttk.LabelFrame(self.main_frame.scrollable_frame, text="基本参数", padding="10")
        basic_params.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
       
        # 基本参数输入
        param_fields = [
            ("额定转速 (r/min)", "nn"),
            ("极对数 p", "p"),
            ("定子槽数Q1", "Q1"),
            ("转子槽数Q2", "Q2"),
            ("定子外径 D1 (cm)", "D1"),
            ("定子内径 Di1 (cm)", "Di1"),
            ("转子内径 Di2 (cm)", "Di2"),
            ("气隙长度 delta (cm)", "delta"),
            ("工作温度 t_work (°C)", "t_work")
        ]
       
        for idx, (label, var_name) in enumerate(param_fields):
            self.create_label_entry(basic_params, label, var_name, idx)
       
        # 铁芯材料选择
        material_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="铁芯材料选择", padding="10")
        material_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        material_desc = {
            "1": "0.5mm厚热轧硅钢片 (B25=1.47T)",
            "2": "0.5mm厚热轧硅钢片 (B25=1.54T)",
            "3": "0.5mm厚热轧硅钢片 (B25=1.57T)",
            "4": "DW540-50",
            "5": "DW465-50",
            "6": "DW360-50",
            "7": "DW315-50",
            "8": "厚度1-1.75mm的钢板",
            "9": "铸钢或厚钢板",
            "10": "10号钢"
        }
        ttk.Label(material_frame, text="请选择铁芯材料：").grid(row=0, column=0, sticky=tk.W)
        self.material_var_pmsm = tk.StringVar()
        material_combo = ttk.Combobox(material_frame, textvariable=self.material_var_pmsm, state="readonly")
        material_combo['values'] = [f"{k}. {v}" for k, v in material_desc.items()]
        material_combo.grid(row=1, column=0, padx=5, pady=5)
        material_combo.current(0)
        self.material_desc_map_pmsm = material_desc  # 保存映射关系
       
        # 其他参数输入
        other_params = ttk.LabelFrame(self.main_frame.scrollable_frame, text="其他参数", padding="10")
        other_params.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        other_fields = [
            ("永磁体厚度 hm (cm)", "hm"),
            ("永磁体轴向长度 lm (mm)", "lm"),
            ("极靴高度 h_pole_shoe (cm)", "h_pole_shoe"),
            ("槽数 Q", "Q"),
            ("电枢绕组的并联支路对数 a", "a"),
            ("并绕根数 Nt", "Nt"),
            ("每槽元件数 u", "u"),
        ]
        for idx, (label, var_name) in enumerate(other_fields):
            self.create_label_entry(other_params, label, var_name, idx)
       
        # 槽参数输入
        slot_params = [
            ("定子槽口宽度 b01 (cm)", 'b01'),
            ("定子槽口高度 h01 (cm)", 'h01'),
            ("转子槽口宽度 b02 (cm)", 'b02'),
            ("转子槽口高度 h02 (cm)", 'h02'),
            ("转子槽上部半径 br1 (cm)", 'br1'),
            ("转子槽下部宽度 br2 (cm)", 'br2'),
            ("槽上部倒角半径 r23 (cm)", 'r23'),
            ("转子槽主体高度（不包含槽口） hr12 (cm)", 'hr12'),
            ("槽上部高度 h2 (cm)", 'h2'),
            ("槽中部宽度 h22 (cm)", 'h22'),
            ("槽高 ht2 (cm)", 'ht2'),
            ("转子冲片内径 Di2 (cm)", 'Di2'),
            ("永磁体每极磁通的截面积 A_m (cm²)", 'A_m')
        ]
        slot_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="槽参数", padding="10")
        slot_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        for idx, (label_text, var_name) in enumerate(slot_params):
            self.create_label_entry(slot_frame, label_text, var_name, idx)
       
        # 槽类型选择
        slot_type_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="槽类型选择", padding="10")
        slot_type_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.slot_type_var_pmsm = tk.StringVar()
        slot_types = ["平底槽", "圆底槽", "圆形槽"]
        slot_type_combo = ttk.Combobox(slot_type_frame, textvariable=self.slot_type_var_pmsm, state="readonly")
        slot_type_combo['values'] = slot_types
        slot_type_combo.grid(row=0, column=0, padx=5, pady=5)
        slot_type_combo.current(0)
       
        # 永磁体参数
        pmm_parameters = ttk.LabelFrame(self.main_frame.scrollable_frame, text="永磁体参数", padding="10")
        pmm_parameters.grid(row=5, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        pmm_fields = [
            ("永磁体剩磁大小 Br (T)", "Br"),
            ("矫顽力 Hc (kA/m)", "Hc"),
            ("相对回复磁导率 mu_r", "mu_r"),
            ("温度系数 alpha_tem (例如：-0.07)", "alpha_tem")
        ]
        for idx, (label, var_name) in enumerate(pmm_fields):
            self.create_label_entry(pmm_parameters, label, var_name, idx)
       
        # 计算参数输入
        calc_params_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="计算参数", padding="10")
        calc_params_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        calc_fields = [
            ("极弧系数 alpha_i（一般范围0.6～0.8）", "alpha_i"),
            ("漏磁系数 sita_1", "sita_1"),
            ("漏磁系数 sita'_2", "sita_prime_2"),
            ("电枢轭磁场强度 H_j1 (A/m)", "H_j1")  # 新增字段
        ]
        for idx, (label, var_name) in enumerate(calc_fields):
            self.create_label_entry(calc_params_frame, label, var_name, idx)
            
        # 新增节距 y, 齿部磁场强度 Ht1, Ht2, 轭部磁场强度 Hj1, Hj2
        additional_params = ttk.LabelFrame(self.main_frame.scrollable_frame, text="新增参数", padding="10")
        additional_params.grid(row=4, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        additional_fields = [
            ("节距 y (cm)", "y"),
            ("齿部磁场强度 Ht1 (A/m)", "Ht1"),
            ("齿部磁场强度 Ht2 (A/m)", "Ht2"),
            ("轭部磁场强度 Hj1 (A/m)", "Hj1"),
            ("轭部磁场强度 Hj2 (A/m)", "Hj2")
        ]
        for idx, (label, var_name) in enumerate(additional_fields):
            self.create_label_entry(additional_params, label, var_name, idx)
       
        # 预期 Phi_delta 输入（可选）
        expected_phi_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="预期磁通密度 Phi_delta (Wb)", padding="10")
        expected_phi_frame.grid(row=7, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Label(expected_phi_frame, text="请输入预期磁通密度 Phi_delta (Wb)（可选）：").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.expected_phi_var = tk.StringVar()
        expected_phi_entry = ttk.Entry(expected_phi_frame, textvariable=self.expected_phi_var)
        expected_phi_entry.grid(row=0, column=1, padx=5, pady=2)
       
        # 计算按钮
        ttk.Button(self.main_frame.scrollable_frame, text="开始计算", command=self.calculate_pmdc).grid(row=8, column=0, pady=10)
       
        # 结果展示
        result_frame = ttk.LabelFrame(self.main_frame.scrollable_frame, text="计算结果", padding="10")
        result_frame.grid(row=0, column=1, rowspan=9, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)
        self.result_text = tk.Text(result_frame, width=80, height=40, wrap='word')
        self.result_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        result_scroll = ttk.Scrollbar(result_frame, orient='vertical', command=self.result_text.yview)
        result_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text['yscrollcommand'] = result_scroll.set

    def show_help(self):
        """
        显示使用说明。
        """
        help_text ="""
    电机设计计算程序使用说明：

    1. 从菜单栏选择要设计的电机类型：
    - 永磁直流电机
    - 异步起动的永磁同步电动机
    - 线绕盘式永磁直流电机

    2. 在相应的界面中输入所需的参数。确保输入的数据类型正确，并根据提示输入相应的参数及其单位。

    3. 点击“开始计算”按钮，程序将执行电磁计算并在右侧区域显示结果。

    4. 可以通过“文件”菜单中的“保存”和“加载”功能，将当前输入的数据保存到文件或从文件加载数据，便于后续使用。

    5. 点击“帮助”菜单中的“使用说明”和“关于”查看详细信息。

    注意事项：
    - 输入参数时，请确保所有必填项均已填写。
    - 在计算过程中，程序会根据输入的槽参数和永磁体参数进行计算。请确保输入的槽参数合理，并理解各参数的含义。
    - 若输入参数有误或缺失，程序将提示错误信息，请根据提示进行修正。
    - 预期磁通密度 Phi_delta 是可选项，如果您有一个期望的 Phi_delta 值，可以输入以提供给迭代过程参考。
        """
        messagebox.showinfo("使用说明", help_text)
   
    def show_about(self):
        """
        显示关于信息。
        """
        about_text = "电机设计计算程序 v1.0\n作者：魏召霖\n日期：2024-12-29"
        messagebox.showinfo("关于", about_text)
   
    def create_label_entry_disc_pmdc(self, parent, label_text, var_name, row):
        """
        创建标签和输入框（Disc-PMDC专用）。
       
        参数:
            parent (tk.Frame): 父容器。
            label_text (str): 标签文本。
            var_name (str): 输入变量名称。
            row (int): 所在行数。
        """
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        var = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=var)
        entry.grid(row=row, column=1, padx=5, pady=2)
        self.motor_data[var_name] = var  # 存储到App的motor_data字典中
   
    def create_label_entry(self, parent, label_text, var_name, row):
        """
        创建标签和输入框。
       
        参数:
            parent (tk.Frame): 父容器。
            label_text (str): 标签文本。
            var_name (str): 输入变量名称。
            row (int): 所在行数。
        """
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        var = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=var)
        entry.grid(row=row, column=1, padx=5, pady=2)
        self.motor_data[var_name] = var  # 存储到App的motor_data字典中
   
    def calculate_pmdc(self):
        """
        永磁直流电机的计算逻辑。
        """
        try:
            # 获取基本参数
            params = {
                "Un": float(self.motor_data["Un"].get()),
                "In": float(self.motor_data["In"].get()),
                "nn": float(self.motor_data["nn"].get()),
                "p": int(self.motor_data["p"].get()),
                "Da": float(self.motor_data["Da"].get()),
                "La": float(self.motor_data["La"].get()),
                "delta": float(self.motor_data["delta"].get()),
                "t_work": float(self.motor_data["t_work"].get()),
                "lambda_est": float(self.motor_data["lambda_est"].get()),
                "hm": float(self.motor_data["hm"].get()),
                "lm": float(self.motor_data["lm"].get()),
                "magnet_type": self.motor_data["magnet_type"].get(),
                "h_pole_shoe": float(self.motor_data["h_pole_shoe"].get()),
                "Q": int(self.motor_data["Q"].get()),
                "a": int(self.motor_data["a"].get()),
                "Nt": int(self.motor_data["Nt"].get()),
                "u": int(self.motor_data["u"].get()),
                "W_c": int(self.motor_data["W_c"].get()),
                "Br": float(self.motor_data["Br"].get()),
                "Hc": float(self.motor_data["Hc"].get()),
                "mu_r": float(self.motor_data["mu_r"].get()),
                "alpha_tem": float(self.motor_data["alpha_tem"].get()),
                "Di2": float(self.motor_data["Di2"].get()),
                "A_m": float(self.motor_data["A_m"].get()),
                "alpha_i": float(self.motor_data["alpha_i"].get()),
                "sita_1": float(self.motor_data["sita_1"].get()),
                "sita_prime_2": float(self.motor_data["sita_prime_2"].get()),
                "H_j1": float(self.motor_data["H_j1"].get())  # 获取 H_j1
            }
           
            # 获取槽参数
            slot_keys = [
                'b02', 'h02', 'r21', 'r22', 'r23', 'h2', 'd1',
                'h22', 'd2', 'd3', 'ht2', 'C_i', 'h_j', 'L_j'
            ]
            slot_values = {}
            for key in slot_keys:
                slot_values[key] = float(self.motor_data[key].get())
            params['slot_values'] = slot_values
           
            # 获取槽类型
            slot_type = self.slot_type_var.get()
            params['slot_type'] = slot_type
           
            # 获取铁芯材料描述
            material_full = self.material_var.get()
            material_key = material_full.split(".")[0]
            material_desc = self.material_desc_map.get(material_key, "未知材料")
            params['material_key'] = material_key
            params['material_desc'] = material_desc
           
            # 获取预期 Phi_delta（可选）
            expected_phi_input = self.expected_phi_var.get()
            expected_Phi_delta = float(expected_phi_input) if expected_phi_input.strip() != "" else None
           
            # 创建 PMDC 参数对象
            pmdc_params = PMDCParameters(**params)
           
            # 处理永磁体类型特定参数
            if pmdc_params.magnet_type.lower() in ["钕铁硼", "铁氧体"]:
                pmdc_params.Br_work = ((1 + (pmdc_params.t_work - 20) * pmdc_params.alpha_tem / 100) *
                                        (1 - 0.02) * pmdc_params.Br)
                pmdc_params.Hc_work = ((1 + (pmdc_params.t_work - 20) * pmdc_params.alpha_tem / 100) *
                                        (1 - 0.02) * pmdc_params.Hc)
            else:
                messagebox.showerror("输入错误", "不支持的永磁体类型。")
                return
           
            # 创建计算器对象并执行计算
            calculator = PMDCCalculator(pmdc_params)
            calculator.calculate(expected_Phi_delta)
           
            # 显示结果
            self.display_results(calculator.results)
           
        except ValueError as e:
            messagebox.showerror("输入错误", f"请输入正确的数值。\n详细错误: {e}")
        except KeyError as e:
            messagebox.showerror("计算错误", f"缺少必要的槽参数: {e}")
        except ZeroDivisionError as e:
            messagebox.showerror("计算错误", f"数学错误: {e}")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {e}")
   
    def display_results(self, results: Dict[str, Any]):
        """
        显示计算结果。
        """
        self.result_text.delete(1.0, tk.END)
        for key, value in results.items():
            self.result_text.insert(tk.END, f"{key}: {value}\n")

# 主程序
def main():
    root = tk.Tk()
    app = MotorDesignApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()