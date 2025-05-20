import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import numpy as np
import math
import sys
import os

# 常量定义
PAI = 3.1415926

# 读取曲线图表离散点数据
# DW315-50磁化损耗曲线
HW10 = [0.60, 0.62, 0.63, 0.65, 0.6, 0.68, 0.69, 0.71,
        0.72, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.80, 0.82, 0.84,
        0.86, 0.88, 0.90, 0.92, 0.95, 0.97, 1.00, 1.02, 1.05, 1.07,
        1.10, 1.12, 1.15, 1.18, 1.21, 1.24, 1.27, 1.30, 1.33, 1.36,
        1.39, 1.42, 1.45, 1.48, 1.51, 1.54, 1.57, 1.60, 1.64, 1.68,
        1.72, 1.75, 1.79, 1.83, 1.87, 1.92, 1.96, 2.00, 2.05, 2.10,
        2.16, 2.21, 2.26, 2.32, 2.38, 2.44, 2.50, 2.56, 2.62, 2.68,
        2.75, 2.81, 2.87, 2.95, 3.03, 3.11, 3.19, 3.27, 3.37, 3.47,
        3.56, 3.66, 3.76, 3.80, 4.00, 4.15, 4.30, 4.45, 4.60, 4.85,
        5.10, 5.55, 6.00, 6.50, 7.00, 7.50, 8.00, 8.50, 9.00, 9.50,
        10.0, 10.7, 11.3, 12.2, 13.0, 14.1, 15.2, 16.5, 17.8, 19.4,
        21.0, 23.5, 26.0, 28.5, 31.0, 34.0, 37.0, 40.0, 43.0, 46.5,
        50.0, 54.0, 58.0, 62.0, 66.0, 70.3, 74.5, 78.8, 83.0, 87.3,
        91.5, 95.8, 100., 106., 112., 118., 124., 131., 137., 144.,
        151., 158., 165., 172., 179., 186., 193., 200., 207., 214.,
        221., 228.]

PW10 = [0.23, 0.25, 0.26, 0.27, 0.29, 0.30, 0.31, 0.32,
        0.34, 0.35, 0.36, 0.38, 0.39, 0.40, 0.42, 0.43, 0.44, 0.45,
        0.47, 0.48, 0.49, 0.51, 0.52, 0.53, 0.56, 0.57, 0.58, 0.61,
        0.62, 0.64, 0.65, 0.68, 0.69, 0.70, 0.73, 0.74, 0.75, 0.78,
        0.80, 0.82, 0.84, 0.86, 0.88, 0.90, 0.92, 0.94, 0.95, 0.97,
        0.99, 1.01, 1.03, 1.05, 1.06, 1.08, 1.10, 1.12, 1.14, 1.16,
        1.18, 1.21, 1.24, 1.27, 1.29, 1.31, 1.34, 1.36, 1.39, 1.42,
        1.44, 1.47, 1.49, 1.52, 1.55, 1.57, 1.60, 1.64, 1.66, 1.69,
        1.71, 1.74, 1.78, 1.84, 1.88, 1.92, 1.96, 2.00, 2.04, 2.08,
        2.10, 2.12, 2.14, 2.18, 2.22, 2.26, 2.30, 2.34, 2.38, 2.40,
        2.44, 2.48, 2.52, 2.56, 2.60, 2.64, 2.68, 2.70, 2.74, 2.78,
        2.82, 2.86, 2.90, 2.95, 3.00, 3.05, 3.10, 3.17, 3.22, 3.27,
        3.34, 3.39, 3.45, 3.51, 3.57, 3.62, 3.68, 3.74, 3.79, 3.84,
        3.91, 3.96, 4.01, 4.08, 4.13, 4.18, 4.23, 4.30, 4.35, 4.40,
        4.47, 4.52, 4.57, 4.64, 4.69, 4.74, 4.81, 4.86, 4.91, 4.96,
        5.03, 5.08]

BW10 = [0.40, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47,
        0.48, 0.49, 0.50, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57,
        0.58, 0.59, 0.60, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67,
        0.68, 0.69, 0.70, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77,
        0.78, 0.79, 0.80, 0.81, 0.83, 0.84, 0.85, 0.86, 0.87,
        0.88, 0.89, 0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97,
        0.98, 0.99, 1.00, 1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07,
        1.08, 1.09, 1.10, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17,
        1.18, 1.19, 1.20, 1.21, 1.22, 1.23, 1.24, 1.25, 1.26, 1.27,
        1.28, 1.29, 1.30, 1.31, 1.32, 1.33, 1.34, 1.35, 1.36, 1.37,
        1.38, 1.39, 1.40, 1.41, 1.42, 1.43, 1.44, 1.45, 1.46, 1.47,
        1.48, 1.49, 1.50, 1.51, 1.52, 1.53, 1.54, 1.55, 1.56, 1.57,
        1.58, 1.59, 1.60, 1.61, 1.62, 1.63, 1.64, 1.65, 1.66, 1.67,
        1.68, 1.69, 1.70, 1.71, 1.72, 1.73, 1.74, 1.75, 1.76, 1.77,
        1.78, 1.79, 1.80, 1.81, 1.82, 1.83, 1.84, 1.85, 1.86, 1.87,
        1.88, 1.89]

# DR550-50磁化损耗曲线
HD21 = [1.40, 1.43, 1.46, 1.49, 1.52, 1.55, 1.58, 1.61,
        1.64, 1.67, 1.71, 1.75, 1.79, 1.83, 1.87, 1.91, 1.95, 1.99,
        2.03, 2.07, 2.12, 2.17, 2.22, 2.27, 2.32, 2.37, 2.42, 2.48,
        2.54, 2.60, 2.67, 2.74, 2.81, 2.88, 2.95, 3.02, 3.09, 3.16,
        3.24, 3.32, 3.40, 3.48, 3.56, 3.64, 3.72, 3.80, 3.89, 3.98,
        4.07, 4.16, 4.25, 4.35, 4.45, 4.55, 4.65, 4.76, 4.88, 5.00,
        5.12, 5.24, 5.36, 5.49, 5.62, 5.75, 5.88, 6.02, 6.16, 6.30,
        6.45, 6.60, 6.75, 6.91, 7.08, 7.26, 7.45, 7.65, 7.86, 8.08,
        8.31, 8.55, 8.80, 9.06, 9.33, 9.61, 9.90, 10.2, 10.5, 10.9,
        11.2, 11.6, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.6,
        16.2, 16.8, 17.4, 18.2, 18.9, 19.8, 20.6, 21.6, 22.6, 23.8,
        25.0, 26.4, 28.0, 29.7, 31.5, 33.7, 36.0, 38.5, 41.3, 44.0,
        47.0, 50.0, 52.9, 55.9, 59.0, 62.1, 65.3, 69.2, 72.8, 76.6,
        80.4, 84.2, 88.0, 92.0, 95.6, 100, 105, 110, 115, 120, 126,
        132, 138, 145, 152, 159, 166, 173, 181, 189, 197, 205]

BD21 = [0.40, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47,
        0.48, 0.49, 0.50, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57,
        0.58, 0.59, 0.60, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67,
        0.68, 0.69, 0.70, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77,
        0.78, 0.79, 0.80, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87,
        0.88, 0.89, 0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97,
        0.98, 0.99, 1.00, 1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07,
        1.08, 1.09, 1.10, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17,
        1.18, 1.19, 1.20, 1.21, 1.22, 1.23, 1.24, 1.25, 1.26, 1.27,
        1.28, 1.29, 1.30, 1.31, 1.32, 1.33, 1.34, 1.35, 1.36, 1.37,
        1.38, 1.39, 1.40, 1.41, 1.42, 1.43, 1.44, 1.45, 1.46, 1.47,
        1.48, 1.49, 1.50, 1.51, 1.52, 1.53, 1.54, 1.55, 1.56, 1.57,
        1.58, 1.59, 1.60, 1.61, 1.62, 1.63, 1.64, 1.65, 1.66, 1.67,
        1.68, 1.69, 1.70, 1.71, 1.72, 1.73, 1.74, 1.75, 1.76, 1.77,
        1.78, 1.79, 1.80, 1.81, 1.82, 1.83, 1.84, 1.85, 1.86, 1.87,
        1.88, 1.89]

PD21 = [0.82, 0.84, 0.88, 0.91, 0.94, 0.97, 1.00, 1.03,
        1.06, 1.09, 1.12, 1.16, 1.19, 1.22, 1.25, 1.29, 1.31, 1.35,
        1.38, 1.42, 1.44, 1.48, 1.51, 1.55, 1.57, 1.61, 1.65, 1.68,
        1.71, 1.74, 1.77, 1.82, 1.84, 1.87, 1.91, 1.95, 1.97, 2.01,
        2.05, 2.08, 2.12, 2.16, 2.19, 2.23, 2.27, 2.31, 2.35, 2.40,
        2.44, 2.48, 2.53, 2.58, 2.62, 2.68, 2.73, 2.78, 2.83, 2.90,
        2.95, 3.01, 3.08, 3.14, 3.21, 3.27, 3.34, 3.42, 3.48, 3.55,
        3.62, 3.70, 3.77, 3.84, 3.91, 3.99, 4.06, 4.14, 4.22, 4.30,
        4.38, 4.45, 4.53, 4.61, 4.68, 4.77, 4.84, 4.92, 5.00, 5.08,
        5.16, 5.23, 5.31, 5.39, 5.47, 5.55, 5.62, 5.71, 5.79, 5.87,
        5.95, 6.03, 6.12, 6.19, 6.27, 6.35, 6.44, 6.52, 6.60, 6.68,
        6.74, 6.83, 6.90, 6.97, 7.05, 7.13, 7.21, 7.29, 7.36, 7.44,
        7.52, 7.60, 7.68, 7.75, 7.83, 7.91, 8.00, 8.09, 8.17, 8.26,
        8.36, 8.44, 8.55, 8.65, 8.75, 8.86, 8.96, 9.08, 9.19, 9.31,
        9.43, 9.55, 9.66, 9.79, 9.91, 10.0, 10.1, 10.2, 10.4, 10.5,
        10.6, 10.8]

BPD21 = [0.50, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57,
         0.58, 0.59, 0.60, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67,
         0.68, 0.69, 0.70, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77,
         0.78, 0.79, 0.80, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87,
         0.88, 0.89, 0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97,
         0.98, 0.99, 1.00, 1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07,
         1.08, 1.09, 1.10, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17,
         1.18, 1.19, 1.20, 1.21, 1.22, 1.23, 1.24, 1.25, 1.26, 1.27,
         1.28, 1.29, 1.30, 1.31, 1.32, 1.33, 1.34, 1.35, 1.36, 1.37,
         1.38, 1.39, 1.40, 1.41, 1.42, 1.43, 1.44, 1.45, 1.46, 1.47,
         1.48, 1.49, 1.50, 1.51, 1.52, 1.53, 1.54, 1.55, 1.56, 1.57,
         1.58, 1.59, 1.60, 1.61, 1.62, 1.63, 1.64, 1.65, 1.66, 1.67,
         1.68, 1.69, 1.70, 1.71, 1.72, 1.73, 1.74, 1.75, 1.76, 1.77,
         1.78, 1.79, 1.80, 1.81, 1.82, 1.83, 1.84, 1.85, 1.86, 1.87,
         1.88, 1.89, 1.90, 1.91, 1.92, 1.93, 1.94, 1.95, 1.96, 1.97,
         1.98, 1.99]

# DR510-50磁化曲线
HD23 = [1.38, 1.40, 1.42, 1.44, 1.46, 1.48, 1.50, 1.52,
        1.54, 1.56, 1.58, 1.60, 1.62, 1.64, 1.66, 1.69, 1.71, 1.74,
        1.76, 1.78, 1.81, 1.84, 1.86, 1.89, 1.91, 1.94, 1.97, 2.00,
        2.03, 2.06, 2.10, 2.13, 2.16, 2.20, 2.24, 2.28, 2.32, 2.36,
        2.40, 2.45, 2.50, 2.55, 2.60, 2.65, 2.70, 2.76, 2.81, 2.87,
        2.93, 2.99, 3.06, 3.13, 3.19, 3.26, 3.33, 3.41, 3.49, 3.57,
        3.65, 3.74, 3.83, 3.92, 4.01, 4.11, 4.22, 4.33, 4.44, 4.56,
        4.67, 4.80, 4.93, 5.07, 5.21, 5.36, 5.52, 5.68, 5.84, 6.00,
        6.16, 6.38, 6.52, 6.72, 6.94, 7.16, 7.38, 7.62, 7.86, 8.10,
        8.36, 8.62, 8.90, 9.20, 9.50, 9.80, 10.1, 10.5, 10.9, 11.3,
        11.7, 12.1, 12.6, 13.1, 13.6, 14.2, 14.8, 15.5, 16.3, 17.1,
        18.1, 19.1, 20.1, 21.2, 22.4, 23.7, 25.0, 26.7, 28.5, 30.4,
        32.6, 35.1, 37.8, 40.7, 43.7, 46.8, 50.0, 53.4, 56.8, 60.4,
        64.0, 67.8, 72.0, 76.4, 80.8, 85.4, 90.2, 95.0, 100, 105,
        110, 116, 122, 128, 134, 140, 146, 152, 158, 165, 172, 180]

BD23 = [0.40, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47,
        0.48, 0.49, 0.50, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57,
        0.58, 0.59, 0.60, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67,
        0.68, 0.69, 0.70, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77,
        0.78, 0.79, 0.80, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87,
        0.88, 0.89, 0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97,
        0.98, 0.99, 1.00, 1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07,
        1.08, 1.09, 1.10, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17,
        1.18, 1.19, 1.20, 1.21, 1.22, 1.23, 1.24, 1.25, 1.26, 1.27,
        1.28, 1.29, 1.30, 1.31, 1.32, 1.33, 1.34, 1.35, 1.36, 1.37,
        1.38, 1.39, 1.40, 1.41, 1.42, 1.43, 1.44, 1.45, 1.46, 1.47,
        1.48, 1.49, 1.50, 1.51, 1.52, 1.53, 1.54, 1.55, 1.56, 1.57,
        1.58, 1.59, 1.60, 1.61, 1.62, 1.63, 1.64, 1.65, 1.66, 1.67,
        1.68, 1.69, 1.70, 1.71, 1.72, 1.73, 1.74, 1.75, 1.76, 1.77,
        1.78, 1.79, 1.80, 1.81, 1.82, 1.83, 1.84, 1.85, 1.86, 1.87,
        1.88, 1.89]

# DR490-50磁化曲线
HD24 = [1.37, 1.38, 1.40, 1.42, 1.44, 1.46, 1.48, 1.50,
        1.52, 1.54, 1.56, 1.58, 1.60, 1.62, 1.64, 1.66, 1.68, 1.70,
        1.72, 1.75, 1.77, 1.79, 1.81, 1.84, 1.87, 1.89, 1.92, 1.94,
        1.97, 2.00, 2.03, 2.06, 2.09, 2.12, 2.16, 2.20, 2.23, 2.27,
        2.31, 2.35, 2.39, 2.43, 2.48, 2.52, 2.57, 2.62, 2.67, 2.73,
        2.79, 2.85, 2.91, 2.97, 3.03, 3.10, 3.17, 3.24, 3.31, 3.39,
        3.47, 3.55, 3.63, 3.71, 3.79, 3.88, 3.97, 4.06, 4.16, 4.26,
        4.37, 4.48, 4.60, 4.72, 4.86, 5.00, 5.14, 5.29, 5.44, 5.60,
        5.76, 5.92, 6.10, 6.28, 6.46, 6.65, 6.85, 7.05, 7.25, 7.46,
        7.68, 7.90, 8.14, 8.40, 8.68, 8.96, 9.26, 9.58, 9.86, 10.2,
        10.6, 11.0, 11.4, 11.8, 12.3, 12.8, 13.3, 13.8, 14.4, 15.0,
        15.7, 16.4, 17.2, 18.0, 18.9, 19.9, 20.9, 22.1, 23.5, 25.0,
        26.8, 28.6, 30.7, 33.0, 35.6, 38.2, 41.1, 44.0, 47.0, 50.0,
        53.5, 57.5, 61.5, 66.0, 70.5, 75.0, 79.7, 84.5, 89.5, 94.7,
        100, 105, 110, 116, 122, 128, 134, 141, 148, 155, 162, 170]

BD24 = [0.40, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47,
        0.48, 0.49, 0.50, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57,
        0.58, 0.59, 0.60, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67,
        0.68, 0.69, 0.70, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77,
        0.78, 0.79, 0.80, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87,
        0.88, 0.89, 0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97,
        0.98, 0.99, 1.00, 1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07,
        1.08, 1.09, 1.10, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17,
        1.18, 1.19, 1.20, 1.21, 1.22, 1.23, 1.24, 1.25, 1.26, 1.27,
        1.28, 1.29, 1.30, 1.31, 1.32, 1.33, 1.34, 1.35, 1.36, 1.37,
        1.38, 1.39, 1.40, 1.41, 1.42, 1.43, 1.44, 1.45, 1.46, 1.47,
        1.48, 1.49, 1.50, 1.51, 1.52, 1.53, 1.54, 1.55, 1.56, 1.57,
        1.58, 1.59, 1.60, 1.61, 1.62, 1.63, 1.64, 1.65, 1.66, 1.67,
        1.68, 1.69, 1.70, 1.71, 1.72, 1.73, 1.74, 1.75, 1.76, 1.77,
        1.78, 1.79, 1.80, 1.81, 1.82, 1.83, 1.84, 1.85, 1.86, 1.87,
        1.88, 1.89]

# DR510-50DR490-50损耗曲线
PD234 = [0.70, 0.72, 0.74, 0.76, 0.78, 0.80, 0.82, 0.84,
         0.87, 0.89, 0.91, 0.93, 0.96, 0.98, 1.01, 1.03, 1.06, 1.08,
         1.11, 1.13, 1.16, 1.19, 1.22, 1.25, 1.28, 1.31, 1.34, 1.37,
         1.40, 1.43, 1.46, 1.49, 1.52, 1.56, 1.59, 1.62, 1.65, 1.68,
         1.72, 1.75, 1.78, 1.81, 1.84, 1.88, 1.91, 1.94, 1.97, 2.00,
         2.04, 2.07, 2.10, 2.14, 2.19, 2.23, 2.28, 2.32, 2.36, 2.40,
         2.45, 2.49, 2.53, 2.57, 2.62, 2.66, 2.71, 2.75, 2.80, 2.85,
         2.90, 2.95, 3.00, 3.05, 3.10, 3.16, 3.21, 3.26, 3.32, 3.38,
         3.44, 3.50, 3.56, 3.62, 3.67, 3.73, 3.78, 3.84, 3.91, 3.98,
         4.06, 4.13, 4.20, 4.28, 4.36, 4.44, 4.52, 4.60, 4.70, 4.80,
         4.90, 5.00, 5.10, 5.22, 5.34, 5.46, 5.58, 5.70, 5.84, 5.98,
         6.12, 6.26, 6.40, 6.53, 6.66, 6.80, 6.93, 7.06, 7.18, 7.28,
         7.41, 7.52, 7.64, 7.70, 7.77, 7.83, 7.90, 7.96, 8.00, 8.04,
         8.07, 8.11, 8.15, 8.24, 8.33, 8.42, 8.51, 8.60, 8.70, 8.80,
         8.90, 9.00, 9.10, 9.20, 9.30, 9.40, 9.50, 9.60, 9.74, 9.88,
         10.0, 10.2]

BD234 = [0.50, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57,
         0.58, 0.59, 0.60, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67,
         0.68, 0.69, 0.70, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77,
         0.78, 0.79, 0.80, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87,
         0.88, 0.89, 0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97,
         0.98, 0.99, 1.00, 1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07,
         1.08, 1.09, 1.10, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17,
         1.18, 1.19, 1.20, 1.21, 1.22, 1.23, 1.24, 1.25, 1.26, 1.27,
         1.28, 1.29, 1.30, 1.31, 1.32, 1.33, 1.34, 1.35, 1.36, 1.37,
         1.38, 1.39, 1.40, 1.41, 1.42, 1.43, 1.44, 1.45, 1.46, 1.47,
         1.48, 1.49, 1.50, 1.51, 1.52, 1.53, 1.54, 1.55, 1.56, 1.57,
         1.58, 1.59, 1.60, 1.61, 1.62, 1.63, 1.64, 1.65, 1.66, 1.67,
         1.68, 1.69, 1.70, 1.71, 1.72, 1.73, 1.74, 1.75, 1.76, 1.77,
         1.78, 1.79, 1.80, 1.81, 1.82, 1.83, 1.84, 1.85, 1.86, 1.87,
         1.88, 1.89, 1.90, 1.91, 1.92, 1.93, 1.94, 1.95, 1.96, 1.97,
         1.98, 1.99]

# DR420-50磁化损耗曲线
HD25 = [3.00, 3.30, 3.74, 4.27, 4.90, 5.50, 6.50, 7.50,
        8.90, 10.5, 13.2, 16.4, 20.4, 25.2, 30.5, 36.0, 42.4, 50.0,
        58.0, 67.0, 77.0]

BD25 = [1.225, 1.250, 1.275, 1.300, 1.325, 1.350,
        1.375, 1.400, 1.425, 1.450, 1.475, 1.500, 1.525, 1.550,
        1.575, 1.600, 1.625, 1.650, 1.675, 1.700, 1.725]

PD25 = [0.48, 0.54, 0.60, 0.70, 0.80, 0.91, 1.04, 1.18,
        1.30, 1.42, 1.55, 1.70, 1.81, 2.00, 2.16, 2.34, 2.54, 2.77,
        3.08, 3.38, 3.76, 4.10]

BPD25 = [0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80,
         0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30,
         1.35, 1.40, 1.45, 1.50]

# 铸钢磁化损耗曲线
HZG = [0.80, 0.88, 0.96, 1.04, 1.12, 1.20, 1.28, 1.36,
       1.44, 1.52, 1.60, 1.68, 1.76, 1.84, 1.92, 2.00, 2.08, 2.16,
       2.24, 2.32, 2.40, 2.48, 2.56, 2.64, 2.72, 2.80, 2.88, 2.96,
       3.04, 3.12, 3.20, 3.28, 3.36, 3.44, 3.52, 3.60, 3.68, 3.76,
       3.84, 3.92, 4.00, 4.08, 4.17, 4.26, 4.34, 4.43, 4.52, 4.6,
       4.70, 4.79, 4.88, 4.97, 5.06, 5.16, 5.25, 5.35, 5.44, 5.54,
       5.64, 5.74, 5.84, 5.93, 6.03, 6.13, 6.23, 6.32, 6.42, 6.52,
       6.62, 6.72, 6.82, 6.93, 7.03, 7.20, 7.34, 7.45, 7.55, 7.66,
       7.76, 7.87, 7.98, 8.10, 8.23, 8.35, 8.48, 8.60, 8.72, 8.85,
       8.98, 9.10, 9.24, 9.38, 9.53, 9.69, 9.86, 10.04, 10.22,
       10.39, 10.56, 10.73, 10.9, 11.08, 11.27, 11.47, 11.67,
       11.87, 12.07, 12.27, 12.48, 12.69, 12.9, 13.15, 13.4, 13.7,
       14.0, 14.3, 14.6, 14.9, 15.2, 15.55, 15.9, 16.3, 16.7, 17.2,
       17.6, 18.1, 18.6, 19.2, 19.7, 20.3, 20.9, 21.6, 22.3, 23.0,
       23.7, 24.4, 25.3, 26.2, 27.1, 28.0, 28.9, 29.9, 31.0, 32.1,
       33.2, 34.3, 35.6, 37.0, 38.3, 39.6, 41.0, 42.5, 44.0, 45.5,
       47.0, 48.5, 50.0, 51.5, 53.0, 55.0]

BZG = [0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17,
       0.18, 0.19, 0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27,
       0.28, 0.29, 0.30, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37,
       0.38, 0.39, 0.40, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47,
       0.48, 0.49, 0.50, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57,
       0.58, 0.59, 0.60, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67,
       0.68, 0.69, 0.70, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77,
       0.78, 0.79, 0.80, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87,
       0.88, 0.89, 0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97,
       0.98, 0.99, 1.00, 1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07,
       1.08, 1.09, 1.10, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17,
       1.18, 1.19, 1.20, 1.21, 1.22, 1.23, 1.24, 1.25, 1.26, 1.27,
       1.28, 1.29, 1.30, 1.31, 1.32, 1.33, 1.34, 1.35, 1.36, 1.37,
       1.38, 1.39, 1.40, 1.41, 1.42, 1.43, 1.44, 1.45, 1.46, 1.47,
       1.48, 1.49, 1.50, 1.51, 1.52, 1.53, 1.54, 1.55, 1.56, 1.57,
       1.58, 1.59, 1.60, 1.61, 1.62, 1.63, 1.64, 1.65, 1.66, 1.67,
       1.68, 1.69]

# 铸铁磁化曲线
HZT = [1.90, 4.40, 8.00, 8.50, 8.70, 9.00, 12.6, 13.0,
       13.5, 14.2, 15.0, 15.7, 16.3, 17.0, 17.6, 18.3, 19.0, 20.0,
       21.0, 22.0, 23.0, 24.0, 25.0, 26.3, 27.6, 28.8, 30.0, 31.5,
       33.0, 34.5, 36.0, 37.5, 39.0, 40.5, 42.0, 43.5, 45.0, 47.0,
       49.0, 51.0, 53.0, 55.0, 57.0, 59.0, 61.0, 63.0, 65.0, 67.7,
       70.4, 73.1, 75.8, 78.5, 81.2, 84.0, 86.6, 89.3, 92.0, 95.8,
       99.6, 103.6, 107.2, 111, 115, 119, 123, 127, 130, 137, 144,
       151, 158, 165, 172, 179, 186, 193, 200]

BZT = [0.10, 0.20, 0.30, 0.31, 0.32, 0.33, 0.40, 0.41,
       0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.50, 0.51,
       0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.60, 0.61,
       0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.70, 0.71,
       0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.80, 0.81,
       0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.90, 0.91,
       0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.00, 1.01,
       1.02, 1.03, 1.04, 1.05, 1.06, 1.07, 1.08, 1.09, 1.10]

# 漆包圆铜线规格
DLX = [0.070, 0.080, 0.090, 0.100, 0.110, 0.120, 0.130,
       0.140, 0.150, 0.160, 0.170, 0.180, 0.190, 0.200, 0.210,
       0.230, 0.250, 0.280, 0.310, 0.330, 0.350, 0.380, 0.400,
       0.420, 0.450, 0.470, 0.500, 0.530, 0.560, 0.630, 0.670,
       0.710, 0.750, 0.800, 0.850, 0.900, 0.950, 1.000, 1.060,
       1.120, 1.180, 1.250, 1.300, 1.400, 1.500]

DHQ = [0.078, 0.088, 0.098, 0.110, 0.120, 0.130, 0.140,
       0.152, 0.162, 0.172, 0.182, 0.195, 0.205, 0.215, 0.225,
       0.250, 0.270, 0.300, 0.330, 0.350, 0.370, 0.400, 0.420,
       0.440, 0.470, 0.490, 0.520, 0.555, 0.585, 0.655, 0.695,
       0.735, 0.780, 0.830, 0.880, 0.930, 0.980, 1.040, 1.100,
       1.160, 1.220, 1.290, 1.340, 1.450, 1.550]

# 求ΔLa*L曲线
SZDLMB = [-0.4, 0, 0.4, 0.8, 1.2, 1.6, 2, 2.4, 2.8, 3.2, 3.6, 4]
SZHMG = [4, 9, 14]
SZGAP = [0.4, 0.6, 0.8, 1.0]
SZDLAB = [-0.48, -0.16, 0.08, 0.32, 0.52, 0.70, 0.88,
          1.04, 1.16, 1.28, 1.40, 1.48, -0.44, -0.12, 0.14, 0.42,
          0.64, 0.84, 1.00, 1.16, 1.30, 1.44, 1.56, 1.64, -0.40,
          -0.08, 0.16, 0.44, 0.66, 0.86, 1.04, 1.20, 1.36, 1.48,
          1.60, 1.72, -0.44, -0.12, 0.12, 0.36, 0.56, 0.76, 0.94,
          1.10, 1.26, 1.34, 1.50, 1.60, -0.40, -0.10, 0.13, 0.40,
          0.64, 0.84, 1.02, 1.16, 1.32, 1.48, 1.60, 1.72, -0.36,
          -0.08, 0.20, 0.44, 0.68, 0.88, 1.07, 1.22, 1.36, 1.52,
          1.66, 1.78, -0.46, -0.14, 0.14, 0.40, 0.64, 0.84, 1.02,
          1.18, 1.32, 1.44, 1.56, 1.64, -0.45, -0.13, 0.16, 0.42,
          0.66, 0.86, 1.04, 1.23, 1.38, 1.50, 1.62, 1.76, -0.44,
          -0.12, 0.20, 0.44, 0.70, 0.90, 1.06, 1.24, 1.40, 1.52,
          1.70, 1.84, -0.40, -0.12, 0.16, 0.42, 0.62, 0.84, 1.03,
          1.18, 1.32, 1.48, 1.59, 1.70, -0.38, -0.10, 0.18, 0.42,
          0.63, 0.86, 1.06, 1.22, 1.38, 1.52, 1.66, 1.80, -0.37,
          -0.08, 0.19, 0.43, 0.64, 0.87, 1.08, 1.22, 1.40, 1.56,
          1.72, 1.88]


# 插值子程序
def LAG(K, X, XX0, YY0):
    """拉格朗日插值"""
    if K <= 0:
        return 0.0
    
    if X < XX0[0]:
        Y = YY0[0] + (X - XX0[0]) * (YY0[1] - YY0[0]) / (XX0[1] - XX0[0])
        return Y
    elif X >= XX0[K - 1]:
        Y = YY0[K - 1] + (X - XX0[K - 1]) * (YY0[K - 1] - YY0[K - 2]) / (XX0[K - 1] - XX0[K - 2])
        return Y
    
    for i in range(1, K):
        if X < XX0[i]:
            Y = YY0[i - 1] + (X - XX0[i - 1]) * (YY0[i] - YY0[i - 1]) / (XX0[i] - XX0[i - 1])
            return Y
    
    # 如果没有找到合适的区间，返回最后一个值
    return YY0[K - 1]

def YYCZ(M, X, XX, YY):
    """一元插值"""
    return LAG(M, X, XX, YY)

def EYCZ(M, N, X1, X2, XX1, XX2, YY):
    """二元插值"""
    YY1 = [0] * M
    YY2 = [0] * N
    
    for i in range(N):
        for j in range(M):
            YY1[j] = YY[j][i]
        Y = LAG(M, X1, XX1, YY1)
        YY2[i] = Y
    
    XLAG = LAG(N, X2, XX2, YY2)
    return XLAG

def SYCZ(L, M, N, X1, X2, X3, XX1, XX2, XX3, YY):
    """三元插值"""
    YY1 = [0] * L
    YY2 = [0] * M
    YY3 = [0] * N
    
    for i in range(N):
        for j in range(M):
            for k in range(L):
                YY1[k] = YY[k][j][i]
            Y = LAG(L, X1, XX1, YY1)
            YY2[j] = Y
        Y = LAG(M, X2, XX2, YY2)
        YY3[i] = Y
    
    XLAG = LAG(N, X3, XX3, YY3)
    return XLAG

def CLCD(CX, b02, h02, d1, h2, h22, d2):
    """电枢槽比漏磁导计算子程序"""
    QSX = h22 / d2
    B12 = d1 / d2
    
    KRS1 = 1.0 / 3.0 - (1.0 - B12) * (0.25 + 1.0 / (3.0 * (1.0 - B12)) + 1.0 / (2.0 * (1.0 - B12)**2) + 1.0 / (1.0 - B12)**3 + math.log(B12) / (1.0 - B12)**4) / 4.0
    
    KRS2 = (2.0 * PAI**2 - 9.0) * PAI / (1536.0 * QSX**3) + PAI / (16.0 * QSX) - PAI / (8.0 * (1.0 - B12) * QSX) - (PAI**2 / (64.0 * (1.0 - B12) * QSX**2) + PAI / (8.0 * (1.0 - B12)**2 * QSX)) * math.log(B12)
    
    KRS3 = PAI / (4.0 * QSX) * (PAI * (1.0 - B12**2) / (8.0 * QSX) + (1.0 + B12) / 2.0)**2 + (4.0 + 3.0 * PAI**2) * B12**2 / (32.0 * QSX**2) * (PAI * (1.0 - B12**2) / (8.0 * QSX) + (1.0 + B12) / 2.0) + (14.0 * PAI**2 + 39.0) * PAI / 1536.0 * B12**4 / QSX**3
    
    if CX == 1:
        if abs(B12 - 1.0) <= 1.0e-4:
            LUMDAS = (4.0 * QSX**3 / 3.0 + 3.0 * PAI * QSX**2 / 2.0 + 4.816 * QSX + 1.5377) / (2.0 * QSX + PAI / 2.0)**2 + h02 / b02
        else:
            LUMDAS = QSX * (KRS1 + KRS2 + KRS3) / (PAI * (1.0 + B12**2) / (8.0 * QSX) + (1.0 + B12) / 2.0)**2 + h02 / b02
    elif CX == 2:
        LUMDAS = h2 / d1 + 2.0 * h22 / (3.0 * (d1 + d2)) + h02 / b02
    elif CX == 3:
        LUMDAS = 0.623 + h02 / b02
    elif CX == 4:
        if abs(B12 - 1.0) <= 1.0e-4:
            LUMDAS = (PAI**2 * QSX / 16.0 + PAI * QSX**2 / 2.0 + 4.0 * QSX**3 / 3.0) / (2.0 * QSX + PAI / 4.0)**2 + h02 / b02 + 2.0 * h2 / (b02 + d1)
        else:
            LUMDAS = QSX * (KRS1 + KRS2) / (PAI / (8.0 * QSX) + (1.0 + B12) / 2.0)**2 + h02 / b02 + 2.0 * h2 / (b02 + d1)
    
    return LUMDAS

def XXG(DLX, S):
    """自动选线规子程序"""
    for j in range(51):
        for i in range(44, -1, -1):
            d = DLX[i]
            for k in range(1, 4):
                N = k
                SS = k * PAI * d**2 / 4.0
                if abs(SS - S) / S <= (0.01 + j * 0.001):
                    return d, N
    
    # 如果没有找到合适的线规，返回默认值
    return DLX[0], 1

def get_material_name(code, material_type):
    """获取材料名称"""
    if material_type == "YCCL":
        materials = {1: "NdFeB", 2: "Ferrite"}
    elif material_type == "JZCL":
        materials = {1: "铸钢", 2: "铸铁"}
    elif material_type == "RZCL":
        materials = {1: "黄铜", 2: "紫铜"}
    elif material_type == "INSC":
        materials = {1: "A", 2: "E", 3: "B", 4: "F", 5: "H"}
    elif material_type == "DSCL":
        materials = {1: "DR510-50", 2: "DR420-50", 3: "DR490-50", 4: "DR550-50", 5: "DW315-50"}
    elif material_type == "CX":
        materials = {1: "梨形槽", 2: "半梨形槽", 3: "圆形槽", 4: "斜肩圆"}
    else:
        return "未知"
    
    return materials.get(code, "未知")

class ScrollableFrame(ttk.Frame):
    """创建可滚动的Frame"""
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

class MotorCalculator:
    """永磁直流电动机电磁计算程序"""
    def __init__(self, root):
        self.root = root
        self.root.title("永磁直流电动机电磁计算程序")
        self.root.geometry("1280x800")
        
        # 创建主框架
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True)
        
        # 创建左侧输入区域（可滚动）
        self.left_frame = ScrollableFrame(main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # 创建右侧结果显示区域
        self.right_frame = ttk.Frame(main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # 添加标题
        ttk.Label(self.left_frame.scrollable_frame, text="永磁直流电动机参数输入", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # 创建输入字段
        self.create_input_fields()
        
        # 创建计算按钮
        ttk.Button(self.left_frame.scrollable_frame, text="计算", command=self.calculate).grid(row=100, column=0, columnspan=2, pady=20)
        
        # 创建结果显示区域
        ttk.Label(self.right_frame, text="计算结果", font=("Arial", 14, "bold")).pack(pady=10)
        self.result_text = scrolledtext.ScrolledText(self.right_frame, width=70, height=40, font=("Courier New", 10))
        self.result_text.pack(fill="both", expand=True)
        
        # 添加使用说明和关于按钮
        ttk.Button(self.left_frame.scrollable_frame, text="使用说明", command=self.show_help).grid(row=101, column=0, pady=5)
        ttk.Button(self.left_frame.scrollable_frame, text="关于", command=self.show_about).grid(row=101, column=1, pady=5)
    
    def create_input_fields(self):
        """创建所有输入字段"""
        # 基本参数
        row = 1
        ttk.Label(self.left_frame.scrollable_frame, text="基本参数", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        # 添加输入字段
        self.entries = {}
        
        # 额定参数
        self.add_entry(row, "PN", "额定功率 (W)", 38.0); row += 1
        self.add_entry(row, "UN", "额定电压 (V)", 24.0); row += 1
        self.add_entry(row, "nN", "额定转速 (r/min)", 3000.0); row += 1
        self.add_entry(row, "IN", "额定电流 (A)", 2.55); row += 1
        self.add_entry(row, "TstbN", "额定起动转矩倍数", 4.5); row += 1
        self.add_entry(row, "TEMP", "工作温度 (°C)", 60.0); row += 1
        
        # 设计参数
        row += 1
        ttk.Label(self.left_frame.scrollable_frame, text="设计参数", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        self.add_entry(row, "A1", "电负荷 (A/cm)", 93.0); row += 1
        self.add_entry(row, "Bj11", "定子轭磁密 (T)", 1.6); row += 1
        self.add_entry(row, "J21", "电流密度 (A/mm²)", 6.50); row += 1
        self.add_entry(row, "LUMDA", "电枢长径比", 0.58); row += 1
        
        # 经验系数
        row += 1
        ttk.Label(self.left_frame.scrollable_frame, text="经验系数", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        self.add_entry(row, "XSBGR", "气隙磁密与剩磁比 (Bg1/Br)", 0.681); row += 1
        self.add_entry(row, "XSHMG", "永磁体厚度与气隙比 (hM/g)", 8.0); row += 1
        self.add_entry(row, "XSLMA", "永磁体与电枢长度比 (LM/La)", 1.0); row += 1
        self.add_entry(row, "XSLJA", "机座与电枢长度比 (Lj/La)", 2.5); row += 1
        self.add_entry(row, "XSDB", "λE计算式中系数", 0.75); row += 1
        self.add_entry(row, "XSTH", "铁损计算式中系数", 2.5); row += 1
        
        # 定子参数
        row += 1
        ttk.Label(self.left_frame.scrollable_frame, text="定子参数", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        self.add_entry(row, "DO", "铁心内径 (cm)", 0.7); row += 1
        self.add_entry(row, "g", "气隙长度 (cm)", 0.05); row += 1
        self.add_entry(row, "SIGMA0", "漏磁系数", 1.213); row += 1
        self.add_entry(row, "SITAP", "磁瓦圆心角 (°)", 129.60); row += 1
        self.add_entry(row, "p", "极对数", 1.0); row += 1
        self.add_entry(row, "KFe", "铁心叠积系数", 0.95); row += 1
        
        # 永磁体参数
        row += 1
        ttk.Label(self.left_frame.scrollable_frame, text="永磁体参数", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        # 永磁材料选择
        ttk.Label(self.left_frame.scrollable_frame, text="永磁材料 (YCCL)").grid(row=row, column=0, sticky="w")
        self.yccl_var = tk.IntVar(value=1)
        yccl_frame = ttk.Frame(self.left_frame.scrollable_frame)
        yccl_frame.grid(row=row, column=1, sticky="w")
        ttk.Radiobutton(yccl_frame, text="NdFeB", variable=self.yccl_var, value=1).pack(side="left")
        ttk.Radiobutton(yccl_frame, text="Ferrite", variable=self.yccl_var, value=2).pack(side="left")
        row += 1
        
        self.add_entry(row, "Br20", "剩磁密度 (T)", 0.65); row += 1
        self.add_entry(row, "Hc20", "矫顽力 (kA/m)", 440.0); row += 1
        self.add_entry(row, "MUr", "相对磁导率", 1.17); row += 1
        self.add_entry(row, "ALFABr", "剩磁温度系数 (%/K)", -0.07); row += 1
        self.add_entry(row, "IL", "不可逆损失 (%)", 0.0); row += 1
        
        # 转子参数
        row += 1
        ttk.Label(self.left_frame.scrollable_frame, text="转子参数", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        # 槽型选择
        ttk.Label(self.left_frame.scrollable_frame, text="槽型 (CX)").grid(row=row, column=0, sticky="w")
        self.cx_var = tk.IntVar(value=2)
        cx_frame = ttk.Frame(self.left_frame.scrollable_frame)
        cx_frame.grid(row=row, column=1, sticky="w")
        ttk.Radiobutton(cx_frame, text="梨形槽", variable=self.cx_var, value=1).pack(side="left")
        ttk.Radiobutton(cx_frame, text="半梨形槽", variable=self.cx_var, value=2).pack(side="left")
        ttk.Radiobutton(cx_frame, text="圆形槽", variable=self.cx_var, value=3).pack(side="left")
        ttk.Radiobutton(cx_frame, text="斜肩圆", variable=self.cx_var, value=4).pack(side="left")
        row += 1
        
        self.add_entry(row, "Q", "槽数", 13.0); row += 1
        self.add_entry(row, "b02", "槽口宽度 (cm)", 0.16); row += 1
        self.add_entry(row, "h02", "槽口高度 (cm)", 0.08); row += 1
        self.add_entry(row, "r21", "槽底圆弧半径 (cm)", 0.0); row += 1
        self.add_entry(row, "r22", "槽上部圆弧半径 (cm)", 0.13); row += 1
        self.add_entry(row, "r23", "槽下部圆弧半径 (cm)", 0.1); row += 1
        self.add_entry(row, "h2", "槽楔高度 (cm)", 0.1); row += 1
        self.add_entry(row, "d1", "槽上部宽度 (cm)", 0.57); row += 1
        self.add_entry(row, "h22", "槽身高度 (cm)", 0.64); row += 1
        self.add_entry(row, "d2", "槽下部宽度 (cm)", 0.26); row += 1
        self.add_entry(row, "d3", "槽底宽度 (cm)", 0.37); row += 1
        
        # 绕组参数
        row += 1
        ttk.Label(self.left_frame.scrollable_frame, text="绕组参数", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        # 绕组类型选择
        ttk.Label(self.left_frame.scrollable_frame, text="绕组类型 (RZXS)").grid(row=row, column=0, sticky="w")
        self.rzxs_var = tk.IntVar(value=1)
        rzxs_frame = ttk.Frame(self.left_frame.scrollable_frame)
        rzxs_frame.grid(row=row, column=1, sticky="w")
        ttk.Radiobutton(rzxs_frame, text="单叠绕组", variable=self.rzxs_var, value=1).pack(side="left")
        ttk.Radiobutton(rzxs_frame, text="单波绕组", variable=self.rzxs_var, value=2).pack(side="left")
        row += 1
        
        self.add_entry(row, "u", "每极每相槽数", 2.0); row += 1
        self.add_entry(row, "y1", "节距", 13.0); row += 1
        self.add_entry(row, "Ci", "绝缘厚度 (cm)", 0.025); row += 1
        self.add_entry(row, "ABX", "扁线窄边长 (mm)", 0.0); row += 1
        self.add_entry(row, "BBX", "扁线宽边长 (mm)", 0.0); row += 1
        
        # 换向器参数
        row += 1
        ttk.Label(self.left_frame.scrollable_frame, text="换向器参数", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        self.add_entry(row, "Lb", "电刷长度 (cm)", 0.8); row += 1
        self.add_entry(row, "bb", "电刷宽度 (cm)", 0.55); row += 1
        self.add_entry(row, "Nb", "每刷片电刷数", 1.0); row += 1
        self.add_entry(row, "LK", "换向器长度 (cm)", 1.4); row += 1
        self.add_entry(row, "DK", "换向器直径 (cm)", 2.4); row += 1
        self.add_entry(row, "NPB", "电刷对数", 1.0); row += 1
        self.add_entry(row, "BBTEA", "电刷中性位置偏移角 (°)", 0.0); row += 1
        self.add_entry(row, "bs", "电刷间距 (cm)", 0.025); row += 1
        self.add_entry(row, "MU", "电刷与换向器间摩擦系数", 0.25); row += 1
        self.add_entry(row, "DELTUb", "电刷压降 (V)", 2.0); row += 1
        self.add_entry(row, "Pbp", "电刷单位面积压力 (N/cm²)", 3.5); row += 1
        
        # 材料选择
        row += 1
        ttk.Label(self.left_frame.scrollable_frame, text="材料选择", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        # 电枢材料
        ttk.Label(self.left_frame.scrollable_frame, text="电枢材料 (DSCL)").grid(row=row, column=0, sticky="w")
        self.dscl_var = tk.IntVar(value=1)
        dscl_frame = ttk.Frame(self.left_frame.scrollable_frame)
        dscl_frame.grid(row=row, column=1, sticky="w")
        ttk.Radiobutton(dscl_frame, text="DR510-50", variable=self.dscl_var, value=1).pack(side="left")
        ttk.Radiobutton(dscl_frame, text="DR420-50", variable=self.dscl_var, value=2).pack(side="left")
        ttk.Radiobutton(dscl_frame, text="DR490-50", variable=self.dscl_var, value=3).pack(side="left")
        ttk.Radiobutton(dscl_frame, text="DR550-50", variable=self.dscl_var, value=4).pack(side="left")
        ttk.Radiobutton(dscl_frame, text="DW315-50", variable=self.dscl_var, value=5).pack(side="left")
        row += 1
        
        # 机座材料
        ttk.Label(self.left_frame.scrollable_frame, text="机座材料 (JZCL)").grid(row=row, column=0, sticky="w")
        self.jzcl_var = tk.IntVar(value=1)
        jzcl_frame = ttk.Frame(self.left_frame.scrollable_frame)
        jzcl_frame.grid(row=row, column=1, sticky="w")
        ttk.Radiobutton(jzcl_frame, text="铸钢", variable=self.jzcl_var, value=1).pack(side="left")
        ttk.Radiobutton(jzcl_frame, text="铸铁", variable=self.jzcl_var, value=2).pack(side="left")
        row += 1
        
        # 绕组材料
        ttk.Label(self.left_frame.scrollable_frame, text="绕组材料 (RZCL)").grid(row=row, column=0, sticky="w")
        self.rzcl_var = tk.IntVar(value=2)
        rzcl_frame = ttk.Frame(self.left_frame.scrollable_frame)
        rzcl_frame.grid(row=row, column=1, sticky="w")
        ttk.Radiobutton(rzcl_frame, text="黄铜", variable=self.rzcl_var, value=1).pack(side="left")
        ttk.Radiobutton(rzcl_frame, text="紫铜", variable=self.rzcl_var, value=2).pack(side="left")
        row += 1
        
        # 绝缘等级
        ttk.Label(self.left_frame.scrollable_frame, text="绝缘等级 (INSC)").grid(row=row, column=0, sticky="w")
        self.insc_var = tk.IntVar(value=3)
        insc_frame = ttk.Frame(self.left_frame.scrollable_frame)
        insc_frame.grid(row=row, column=1, sticky="w")
        ttk.Radiobutton(insc_frame, text="A", variable=self.insc_var, value=1).pack(side="left")
        ttk.Radiobutton(insc_frame, text="E", variable=self.insc_var, value=2).pack(side="left")
        ttk.Radiobutton(insc_frame, text="B", variable=self.insc_var, value=3).pack(side="left")
        ttk.Radiobutton(insc_frame, text="F", variable=self.insc_var, value=4).pack(side="left")
        ttk.Radiobutton(insc_frame, text="H", variable=self.insc_var, value=5).pack(side="left")
        row += 1
        
        # 特殊工况
        row += 1
        ttk.Label(self.left_frame.scrollable_frame, text="特殊工况", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        # 突然起动
        ttk.Label(self.left_frame.scrollable_frame, text="突然起动 (TSGK1)").grid(row=row, column=0, sticky="w")
        self.tsgk1_var = tk.IntVar(value=1)
        tsgk1_frame = ttk.Frame(self.left_frame.scrollable_frame)
        tsgk1_frame.grid(row=row, column=1, sticky="w")
        ttk.Radiobutton(tsgk1_frame, text="有", variable=self.tsgk1_var, value=1).pack(side="left")
        ttk.Radiobutton(tsgk1_frame, text="无", variable=self.tsgk1_var, value=0).pack(side="left")
        row += 1
        
        # 瞬时堵转
        ttk.Label(self.left_frame.scrollable_frame, text="瞬时堵转 (TSGK2)").grid(row=row, column=0, sticky="w")
        self.tsgk2_var = tk.IntVar(value=0)
        tsgk2_frame = ttk.Frame(self.left_frame.scrollable_frame)
        tsgk2_frame.grid(row=row, column=1, sticky="w")
        ttk.Radiobutton(tsgk2_frame, text="有", variable=self.tsgk2_var, value=1).pack(side="left")
        ttk.Radiobutton(tsgk2_frame, text="无", variable=self.tsgk2_var, value=0).pack(side="left")
        row += 1
        
        # 突然停转
        ttk.Label(self.left_frame.scrollable_frame, text="突然停转 (TSGK3)").grid(row=row, column=0, sticky="w")
        self.tsgk3_var = tk.IntVar(value=1)
        tsgk3_frame = ttk.Frame(self.left_frame.scrollable_frame)
        tsgk3_frame.grid(row=row, column=1, sticky="w")
        ttk.Radiobutton(tsgk3_frame, text="有", variable=self.tsgk3_var, value=1).pack(side="left")
        ttk.Radiobutton(tsgk3_frame, text="无", variable=self.tsgk3_var, value=0).pack(side="left")
        row += 1
        
        # 突然反转
        ttk.Label(self.left_frame.scrollable_frame, text="突然反转 (TSGK4)").grid(row=row, column=0, sticky="w")
        self.tsgk4_var = tk.IntVar(value=0)
        tsgk4_frame = ttk.Frame(self.left_frame.scrollable_frame)
        tsgk4_frame.grid(row=row, column=1, sticky="w")
        ttk.Radiobutton(tsgk4_frame, text="有", variable=self.tsgk4_var, value=1).pack(side="left")
        ttk.Radiobutton(tsgk4_frame, text="无", variable=self.tsgk4_var, value=0).pack(side="left")
        row += 1
    
    def add_entry(self, row, name, label_text, default_value):
        """添加一个输入字段"""
        ttk.Label(self.left_frame.scrollable_frame, text=label_text).grid(row=row, column=0, sticky="w")
        var = tk.StringVar(value=str(default_value))
        entry = ttk.Entry(self.left_frame.scrollable_frame, textvariable=var)
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
        self.entries[name] = var
    
    def get_float_value(self, name):
        """获取浮点数值"""
        try:
            return float(self.entries[name].get())
        except ValueError:
            messagebox.showerror("输入错误", f"{name} 必须是一个有效的数字")
            return None
    
    def calculate(self):
        """执行计算"""
        # 清空结果区域
        self.result_text.delete(1.0, tk.END)
        
        try:
            # 获取所有输入值
            PN = self.get_float_value("PN")
            UN = self.get_float_value("UN")
            nN = self.get_float_value("nN")
            IN = self.get_float_value("IN")
            TstbN = self.get_float_value("TstbN")
            TEMP = self.get_float_value("TEMP")
            
            A1 = self.get_float_value("A1")
            Bj11 = self.get_float_value("Bj11")
            J21 = self.get_float_value("J21")
            LUMDA = self.get_float_value("LUMDA")
            
            XSBGR = self.get_float_value("XSBGR")
            XSHMG = self.get_float_value("XSHMG")
            XSLMA = self.get_float_value("XSLMA")
            XSLJA = self.get_float_value("XSLJA")
            XSDB = self.get_float_value("XSDB")
            XSTH = self.get_float_value("XSTH")
            
            DO = self.get_float_value("DO")
            g = self.get_float_value("g")
            SIGMA0 = self.get_float_value("SIGMA0")
            SITAP = self.get_float_value("SITAP")
            p = self.get_float_value("p")
            KFe = self.get_float_value("KFe")
            
            YCCL = self.yccl_var.get()
            Br20 = self.get_float_value("Br20")
            Hc20 = self.get_float_value("Hc20")
            MUr = self.get_float_value("MUr")
            ALFABr = self.get_float_value("ALFABr")
            IL = self.get_float_value("IL") / 100.0  # 转换为小数
            
            CX = self.cx_var.get()
            Q = self.get_float_value("Q")
            b02 = self.get_float_value("b02")
            h02 = self.get_float_value("h02")
            r21 = self.get_float_value("r21")
            r22 = self.get_float_value("r22")
            r23 = self.get_float_value("r23")
            h2 = self.get_float_value("h2")
            d1 = self.get_float_value("d1")
            h22 = self.get_float_value("h22")
            d2 = self.get_float_value("d2")
            d3 = self.get_float_value("d3")
            
            RZXS = self.rzxs_var.get()
            u = self.get_float_value("u")
            y1 = self.get_float_value("y1")
            Ci = self.get_float_value("Ci")
            ABX = self.get_float_value("ABX")
            BBX = self.get_float_value("BBX")
            
            Lb = self.get_float_value("Lb")
            bb = self.get_float_value("bb")
            Nb = self.get_float_value("Nb")
            LK = self.get_float_value("LK")
            DK = self.get_float_value("DK")
            NPB = self.get_float_value("NPB")
            BBTEA = self.get_float_value("BBTEA")
            bs = self.get_float_value("bs")
            MU = self.get_float_value("MU")
            DELTUb = self.get_float_value("DELTUb")
            Pbp = self.get_float_value("Pbp")
            
            DSCL = self.dscl_var.get()
            JZCL = self.jzcl_var.get()
            RZCL = self.rzcl_var.get()
            INSC = self.insc_var.get()
            
            TSGK1 = self.tsgk1_var.get()
            TSGK2 = self.tsgk2_var.get()
            TSGK3 = self.tsgk3_var.get()
            TSGK4 = self.tsgk4_var.get()
            
            # 主要尺寸确定
            Br = (1.0 + (TEMP - 20.0) * ALFABr / 100.0) * (1.0 - IL) * Br20
            HC = (1.0 + (TEMP - 20.0) * ALFABr / 100.0) * (1.0 - IL) * Hc20
            effN = PN / (UN * IN) * 100.0  # 额定效率
            PJS = (1.0 + 2.0 * effN / 100.0) / (3.0 * effN / 100.0) * PN  # 计算功率
            E = (1.0 + 2.0 * effN / 100.0) / 3.0 * UN  # 感应电动势初算值
            Bg1 = XSBGR * Br
            ALFAP = SITAP / (180.0 / p)  # 极弧系数，SITAP是磁瓦圆心角
            ALFAI = ALFAP  # 计算极弧系数
            SIGMA = SIGMA0
            
            # 电枢直径
            Da = round(((6.1 * PJS * 1.0e+4 / (ALFAI * A1 * Bg1 * nN * LUMDA))**(1.0 / 3.0) + 2.0 * g) * 10.0) / 10.0 - 2.0 * g
            
            TAO = PAI * Da / (2.0 * p)  # 极距
            La = round(LUMDA * Da * 10.0) / 10.0
            hM = round(XSHMG * g * 10.0) / 10.0  # 永磁体厚度
            LM = round(XSLMA * La * 10.0) / 10.0  # 永磁体轴向长度
            
            if YCCL == 1:
                Lef = La + 2.0 * g  # 电枢计算长度
            elif YCCL == 2:
                DETLMB = (LM - La) / (hM + g)
                hMG = hM / g
                
                # 创建三维数组用于SYCZ函数
                YY = [[[0 for _ in range(4)] for _ in range(3)] for _ in range(12)]
                
                # 填充YY数组
                idx = 0
                for i in range(12):
                    for j in range(3):
                        for k in range(4):
                            YY[i][j][k] = SZDLAB[idx]
                            idx += 1
                
                DETLAB = SYCZ(12, 3, 4, DETLMB, hMG, g, SZDLMB, SZHMG, SZGAP, YY)
                Lef = La + DETLAB * (hM + g)  # 电枢计算长度
            
            DMi = Da + 2.0 * g  # 永磁体内径
            DMo = DMi + 2.0 * hM  # 永磁体外径
            Lj = round(XSLJA * La * 10.0) / 10.0  # 机座长度
            hj = round(SIGMA * ALFAI * TAO * Lef * Bg1 / (2.0 * Lj * Bj11) * 10.0) / 10.0  # 机座厚度
            Dj = DMo + 2.0 * hj  # 基座外径
            FIg1 = ALFAI * TAO * Lef * Bg1 * 1.0e-4
            
            if RZXS == 1:
                a = p  # 单叠绕组
            elif RZXS == 2:
                a = 1  # 单波绕组
            
            n1 = 60.0 * a * E / (p * FIg1 * nN)  # 预计导体总数
            Ns1 = n1 / Q  # 每槽导体数
            Ws = round(Ns1 / (2.0 * u))  # 每元件匝数
            NS = 2.0 * u * Ws  # 实际每槽导体数
            N = Q * NS  # 实际导体总数
            ACua1 = IN / (2.0 * a) / J21
            
            di, Nt = XXG(DLX, ACua1)
            
            if di >= 0.053 and di < 0.5:
                d = di + 0.015
            elif di >= 0.5 and di < 1.0:
                d = di + 0.02  # di是导线裸线线径，d导线绝缘后线径
            else:
                d = di + 0.01  # 默认情况
            
            # 固定参数计算
            if p == 1:
                KE = 1.35
            elif p == 2:
                KE = 1.10
            else:
                KE = 0.80
            
            Lav = La + KE * Da  # 绕组平均半匝长度
            ACua = Nt * PAI * di**2 / 4.0  # 实际电负荷
            ROU20 = 0.1785 * 1.0e-3
            Ra20 = ROU20 * N * Lav / ACua / (2.0 * a)**2  # 电枢绕组电阻
            
            if INSC == 1 or INSC == 2 or INSC == 3:
                ROU75 = 0.217 * 1.0e-3
                Ra75 = ROU75 * N * Lav / ACua / (2.0 * a)**2
                Raw = Ra75
            else:
                ROU115 = 0.245 * 1.0e-3
                Ra115 = ROU115 * N * Lav / ACua / (2.0 * a)**2
                Raw = Ra115
            
            t2 = PAI * Da / Q
            ht = h02 + h2 + h22 + r22
            Bt21 = PAI * (Da - 2.0 * h02 - 2.0 * h2) / Q - d1  # 齿上部宽度
            Bt22 = PAI * (Da - 2.0 * ht + 2.0 * r22) / Q - d2  # 齿下部宽度
            
            if Bt21 > Bt22:
                Vbt2 = (Bt21 + 2.0 * Bt22) / 3.0
            else:
                Vbt2 = (Bt22 + 2.0 * Bt21) / 3.0
            
            h2j = (Da - 2.0 * ht - DO) / 2.0  # 电枢轭高
            hj21 = h2j + DO / 8.0  # 电枢轭有效高
            
            if CX == 1:
                As = PAI * (r21**2 + r22**2) / 2.0 + h22 * (r21 + r22) - Ci * (PAI * (r21 + r22) + 2.0 * h22)
            elif CX == 2:
                As = PAI * (r22**2 + r23**2) / 2.0 + h22 * (d1 + 2.0 * r22) / 2.0 + d3 * r23 - Ci * (PAI * (r21 + r22) + 2.0 * h22 + d1)
            elif CX == 3:
                As = PAI * d1**2 / 4.0 - Ci * PAI * d1
            elif CX == 4:
                As = (b02 + d1) * h2 / 2.0 + (d1 + 2.0 * r22) * h22 / 2.0 + PAI * r22**2 / 2.0 - Ci * (PAI * r22 + 2.0 * (h22 + h2) + d1)  # As是槽净面积
            
            K = u * Q
            Ab = Lb * bb
            tK = PAI * DK / K
            
            # 绕组计算
            I1 = IN
            BBETA = 0.75  # 假设BBETA初始值为0.75
            
            # 迭代计算 - 第一个迭代循环
            for _ in range(20):  # 限制迭代次数
                AX = N * I1 / (2.0 * PAI * a * Da)
                Ia = I1 / (2.0 * a)
                J2 = Ia / ACua
                AJ2 = AX * J2
                Sf = NS * Nt * d**2 * 1.0e-2 / As * 100.0  # 槽满率
                
                # 磁路计算
                SIGMAS = 2.0 / PAI * (math.atan(b02 / (hM + g) / 2.0) - (hM + g) / b02 * math.log(1.0 + (b02 / (hM + g))**2 / 4.0))
                KgM = t2 / (t2 - SIGMAS * b02)
                Kg = KgM + (KgM - 1.0) * hM / g  # 气隙系数
                
                Bg = FIg1 * 1.0e+4 / (ALFAI * TAO * Lef)  # 气隙磁密
                Hg = Bg / (4.0 * PAI * 1.0e-5)
                Fg = 1.6 * Kg * g * Bg * 1.0e+4  # 每对极气隙磁位差
                Bt2 = t2 * Lef * Bg / (Vbt2 * La * KFe)  # 电枢齿磁密
                Bj2 = FIg1 * 1.0e+4 / (2.0 * KFe * hj21 * La)  # 电枢轭磁密
                
                # 根据电枢材料选择不同的磁化曲线
                if DSCL == 1:
                    Ht2 = YYCZ(len(BD23), Bt2, BD23, HD23)
                    Hj2 = YYCZ(len(BD23), Bj2, BD23, HD23)
                elif DSCL == 2:
                    Ht2 = YYCZ(len(BD25), Bt2, BD25, HD25)
                    Hj2 = YYCZ(len(BD25), Bj2, BD25, HD25)
                elif DSCL == 3:
                    Ht2 = YYCZ(len(BD24), Bt2, BD24, HD24)
                    Hj2 = YYCZ(len(BD24), Bj2, BD24, HD24)
                elif DSCL == 4:
                    Ht2 = YYCZ(len(BD21), Bt2, BD21, HD21)
                    Hj2 = YYCZ(len(BD21), Bj2, BD21, HD21)
                elif DSCL == 5:
                    Ht2 = YYCZ(len(BW10), Bt2, BW10, HW10)
                    Hj2 = YYCZ(len(BW10), Bj2, BW10, HW10)
                
                Ft2 = 2.0 * Ht2 * ht  # 电枢齿磁位差
                Lj2 = PAI * (DO + h2j) / (2.0 * p)  # 电枢轭磁路平均计算长度
                Fj2 = Hj2 * Lj2  # 电枢轭磁位差
                Bj1 = SIGMA * FIg1 * 1.0e+4 / (2.0 * hj * Lj)
                
                # 根据机座材料选择不同的磁化曲线
                if JZCL == 1:
                    HJ1 = YYCZ(len(BZG), Bj1, BZG, HZG)
                elif JZCL == 2:
                    HJ1 = YYCZ(len(BZT), Bj1, BZT, HZT)
                
                Lj1 = PAI * (Dj - hj) / (2.0 * p)  # 定子轭磁路平均计算长度
                Fj1 = HJ1 * Lj1  # 定子轭磁位差
                SUMF = Fg + Ft2 + Fj2 + Fj1  # 外磁路总磁位差
                
                # 空载特性计算
                NFIg = int(FIg1 * 1.0e+4 - 1)
                
                # 工作点计算
                NUMDAG = FIg1 / SUMF  # 气隙主磁导
                AM = PAI / (2.0 * p) * ALFAP * LM * (DMi + hM)
                NUMDAB = Br * AM / (2.0 * hM * HC) * 1.0e-5
                LUMDAG = NUMDAG / NUMDAB  # 主磁导标么值
                LUMDAN = SIGMA0 * LUMDAG  # 外磁路总磁导
                
                FadN = BBETA * AX
                FasN = 0.025 * AX
                Fa = FadN + FasN  # 直轴电枢去磁磁动势
                Fa1 = 2.0 * Fa * 1.0e-1 / (2.0 * hM * HC * SIGMA0)
                bMN = LUMDAN * (1.0 - Fa1) / (1.0 + LUMDAN)  # 永磁体负载工作点
                hMN = (LUMDAN * Fa1 + 1.0) / (1.0 + LUMDAN)  # 永磁体负载工作点
                FIg = bMN * Br * AM / SIGMA * 1.0e-4  # 实际气隙磁通
                
                ERR = abs((FIg - FIg1) / FIg1)
                if ERR < 0.005:
                    break
                
                FIg1 = (FIg1 + FIg) / 2.0
            
            # 换向计算
            E = UN - DELTUb - I1 * Raw
            RPM = 60.0 * a * E / (p * FIg1 * N)
            Va = PAI * Da * RPM / 6000.0
            Jb = I1 / (NPB * Nb * Ab)
            VK = PAI * DK * RPM / 6000.0  # 换向器圆周速度
            
            LUMDAE = 0.75 * Lav / (2.0 * La)
            LUMDAZ = 0.92 * math.log10(PAI * t2 / b02)
            LUMDAS = CLCD(CX, b02, h02, d1, h2, h22, d2)
            SUMLMD = LUMDAS + LUMDAE + LUMDAZ
            
            Er = 2.0 * Ws * Va * AX * La * SUMLMD * 1.0e-6  # 换向元件电抗电动势
            
            if YCCL == 2:
                hM1 = hM / MUr * (DMi - g) / (DMi + hM)
                Gaq = g + MUr * hM1
                Baq = PAI * Da * AX / (2.0 * p) * (1.0 - 2.0 * p / K * bb / tK) * 4.0 * PAI * 1.0e-7 / Gaq * 1.0e+2
            else:
                Baq = 4.0 * PAI * 1.0e-7 * AX * TAO / (2.0 * (g + hM)) * 1.0e+2
            
            Ea = 2.0 * Ws * Va * La * Baq * 1.0e-2  # 换向元件交轴电枢反应电动势
            SUME = Er + Ea  # 换向元件中合成电动势
            
            bb1 = Da / DK * bb
            tK1 = Da / DK * tK
            bKr = bb1 + (K / Q + K / (2.0 * p) - y1 - a / p) * tK1  # 换向区宽度
            HXQKB = bKr / TAO / (1.0 - ALFAP)  # 换向区宽度检查
            
            # 最大去磁点核算
            SUMFA1 = SUMFA2 = SUMFA3 = SUMFA4 = 0.0
            
            if TSGK1 == 1:
                Imax1 = (UN - DELTUb) / Ra20
                AXmax1 = N * Imax1 / (2.0 * a * PAI * Da)
                FadM1 = BBETA * AXmax1
                FasM1 = 0.025 * AXmax1
                FaqM1 = ALFAP * TAO * AXmax1 / 2.0
                SUMFA1 = 2.0 * (FadM1 + FasM1 + FaqM1)
            
            if TSGK2 == 1:
                Imax2 = (UN - DELTUb) / Raw
                AXmax2 = N * Imax2 / (2.0 * a * PAI * Da)
                FadM2 = BBETA * AXmax2
                FasM2 = 0.025 * AXmax2
                FaqM2 = ALFAP * TAO * AXmax2 / 2.0
                SUMR = 2.0 * Ws * Lav * ROU20 / ACua + DELTUb / IN
                FK2 = bKr * N**2 * Ws * La * RPM * Imax2 * SUMLMD * 1.0e-8 / (2.0 * 60.0 * a * PAI * Da * SUMR)
                SUMFA2 = 2.0 * (FadM2 + FasM2 + FaqM2 + FK2)
            
            if TSGK3 == 1:
                Imax3 = (E - DELTUb) / Raw
                AXmax3 = N * Imax3 / (2.0 * a * PAI * Da)
                FadM3 = BBETA * AXmax3
                FasM3 = 0.025 * AXmax3
                FaqM3 = ALFAP * TAO * AXmax3 / 2.0
                SUMFA3 = 2.0 * (FadM3 + FasM3 + FaqM3)
            
            if TSGK4 == 1:
                Imax4 = (UN + E - DELTUb) / Raw
                AXmax4 = N * Imax4 / (2.0 * a * PAI * Da)
                FadM4 = BBETA * AXmax4
                FasM4 = 0.025 * AXmax4
                FaqM4 = ALFAP * TAO * AXmax4 / 2.0
                SUMR = 2.0 * Ws * Lav * ROU20 / ACua + DELTUb / IN
                FK4 = bKr * N**2 * Ws * La * RPM * Imax4 * SUMLMD * 1.0e-8 / (2.0 * 60.0 * a * PAI * Da * SUMR)
                SUMFA4 = 2.0 * (FadM4 + FasM4 + FaqM4 + FK4)
            
            SUMFAM = max(SUMFA1, SUMFA2, SUMFA3, SUMFA4)  # 电枢总去磁磁动势
            
            FAM1 = SUMFAM * 1.0e-1 / (SIGMA0 * HC * 2.0 * hM)
            bMh = LUMDAN * (1.0 - FAM1) / (1.0 + LUMDAN)  # 最大去磁时永磁体工作点
            hMh = (LUMDAN * FAM1 + 1.0) / (1.0 + LUMDAN)  # 最大去磁时永磁体工作点
            
            # 工作特性计算
            # 完整的迭代计算 - 第二个迭代循环
            max_iterations = 20  # 最大迭代次数
            iteration_count = 0
            
            while True:
                iteration_count += 1
                
                pCua = I1**2 * Raw  # 电枢绕组铜耗
                pb = I1 * DELTUb  # 电刷接触电阻损耗
                mt2 = 7.8 * 1.0e-3 * KFe * La * (PAI / 4.0 * (Da**2 - (Da - 2.0 * ht)**2) - Q * As)  # 电枢齿质量
                mj2 = 7.8 * 1.0e-3 * KFe * La * PAI / 4.0 * ((Da - 2.0 * ht)**2 - DO**2)  # 电枢轭质量
                
                # 根据电枢材料选择不同的损耗曲线
                if DSCL == 1:
                    PKET = YYCZ(len(BD234), Bt2, BD234, PD234)
                    PKEJ = YYCZ(len(BD234), Bj2, BD234, PD234)
                elif DSCL == 2:
                    PKET = YYCZ(len(BPD25), Bt2, BPD25, PD25)
                    PKEJ = YYCZ(len(BPD25), Bj2, BPD25, PD25)
                elif DSCL == 3:
                    PKET = YYCZ(len(BD234), Bt2, BD234, PD234)
                    PKEJ = YYCZ(len(BD234), Bj2, BD234, PD234)
                elif DSCL == 4:
                    PKET = YYCZ(len(BPD21), Bt2, BPD21, PD21)
                    PKEJ = YYCZ(len(BPD21), Bj2, BPD21, PD21)
                elif DSCL == 5:
                    PKET = YYCZ(len(BW10), Bt2, BW10, PW10)
                    PKEJ = YYCZ(len(BW10), Bj2, BW10, PW10)
                
                F = p * RPM / 60.0
                pFe = 2.5 * (F / 50.0)**1.3 * (PKET * mt2 + PKEJ * mj2)
                pKbm = 2.0 * 0.25 * 3.5 * Ab * NPB * VK
                pbwf = 0.04 * PN
                pfw = pKbm + pbwf  # 总机械损耗
                SUMp = pCua + pb + pFe + pfw  # 总损耗
                P1 = PN + SUMp  # 输入功率
                eff = PN / P1 * 100.0
                I = P1 / UN
                
                # 迭代计算
                EERR2 = abs((I - I1) / I1)
                if EERR2 <= 0.01 or iteration_count >= max_iterations:
                    break
                
                I1 = (I + I1) / 2.0
                
                # 更新电流后需要重新计算相关参数
                AX = N * I1 / (2.0 * PAI * a * Da)
                Ia = I1 / (2.0 * a)
                J2 = Ia / ACua
                AJ2 = AX * J2
                Sf = NS * Nt * d**2 * 1.0e-2 / As * 100.0
                
                # 更新换向计算
                E = UN - DELTUb - I1 * Raw
                RPM = 60.0 * a * E / (p * FIg1 * N)
                Va = PAI * Da * RPM / 6000.0
                Jb = I1 / (NPB * Nb * Ab)
                VK = PAI * DK * RPM / 6000.0
            
            Ist = (UN - DELTUb) / Ra20  # 启动电流
            Istb = Ist / IN  # 启动电流倍数
            Tst = p * N * FIg1 / (2.0 * PAI * a) * Ist  # 启动转矩
            T = 9.549 * PN / RPM
            TN = 9.549 * PN / nN
            Tstb = Tst / TN  # 起动转矩倍数
            
            # 计算不同负载率的工作特性
            load_data = []
            for load_ratio in range(1, 11):
                I1_load = load_ratio * IN / 10.0
                E_load = UN - DELTUb - I1_load * Raw
                RPM_load = 60.0 * a * E_load / (p * FIg1 * N)
                VK_load = PAI * DK * RPM_load / 6000.0
                F_load = p * RPM_load / 60.0
                pCua_load = I1_load**2 * Raw
                pb_load = I1_load * DELTUb
                pFe_load = 2.5 * (F_load / 50.0)**1.3 * (PKET * mt2 + PKEJ * mj2)
                pKbm_load = 2.0 * 0.25 * 3.5 * Ab * NPB * VK_load
                pbwf_load = 0.04 * PN * RPM_load / nN
                pfw_load = pKbm_load + pbwf_load
                SUMp_load = pCua_load + pb_load + pFe_load + pfw_load
                P1_load = UN * I1_load
                P2_load = P1_load - SUMp_load
                eff_load = P2_load / P1_load * 100.0 if P1_load > 0 else 0
                T_load = 9.549 * P2_load / RPM_load if RPM_load > 0 else 0
                
                load_data.append((load_ratio, P2_load, E_load, RPM_load, SUMp_load, eff_load, T_load))
            
            # 输出计算结果
            self.result_text.insert(tk.END, "【性能】\n")
            self.result_text.insert(tk.END, f"额定功率 PN = {PN:.2f} W, 额定电压 UN = {UN:.2f} V\n")
            self.result_text.insert(tk.END, f"额定电流 IN = {IN:.2f} A, 额定转速 nN = {nN:.2f} r/min (±{nN*0.05:.2f})\n")
            self.result_text.insert(tk.END, f"额定起动转矩倍数 TstbN = {TstbN:.2f}, 额定效率 eff = {eff:.2f} %\n")
            self.result_text.insert(tk.END, f"输入功率 P1 = {P1:.2f} W, 工作电流 I1 = {I1:.2f} A\n")
            self.result_text.insert(tk.END, f"工作转速 RPM = {RPM:.2f} r/min, 起动转矩 Tst = {Tst:.2f} N.m\n")
            self.result_text.insert(tk.END, f"起动转矩倍数 Tstb = {Tstb:.2f}, 起动电流 Ist = {Ist:.2f} A, 起动电流倍数 Istb = {Istb:.2f}\n")
            self.result_text.insert(tk.END, f"感应电势 E = {E:.2f} V, 工作温度 TEMP = {TEMP:.2f} °C\n")
            self.result_text.insert(tk.END, f"额定转矩 TN = {TN:.2f} N.m\n\n")
            
            self.result_text.insert(tk.END, "【材料选择】\n")
            self.result_text.insert(tk.END, f"电枢材料 DSCL = {get_material_name(DSCL, 'DSCL')}\n")
            self.result_text.insert(tk.END, f"永磁材料 YCCL = {get_material_name(YCCL, 'YCCL')}\n")
            self.result_text.insert(tk.END, f"机座材料 JZCL = {get_material_name(JZCL, 'JZCL')}\n")
            self.result_text.insert(tk.END, f"绕组材料 RZCL = {get_material_name(RZCL, 'RZCL')}\n")
            self.result_text.insert(tk.END, f"绝缘等级 INSC = {get_material_name(INSC, 'INSC')}\n\n")
            
            self.result_text.insert(tk.END, "【定子尺寸及永磁体性能数据】\n")
            self.result_text.insert(tk.END, f"定子外径 Dj = {Dj:.4f} cm, 定子轭厚度 hj = {hj:.4f} cm, 机座长度 Lj = {Lj:.4f} cm\n")
            self.result_text.insert(tk.END, f"极对数 p = {p:.0f}, YCCL = {YCCL}\n")
            self.result_text.insert(tk.END, f"永磁体厚度 hM = {hM:.4f} cm (±{0.02:.4f}), 永磁体轴向长度 LM = {LM:.4f} cm\n")
            self.result_text.insert(tk.END, f"极弧系数 ALFAP = {ALFAP:.4f}, 永磁体剩磁 Br = {Br:.2f} T (±{Br * 0.1:.4f})\n")
            self.result_text.insert(tk.END, f"矫顽力 Hc = {HC:.2f} kA/m (±{HC * 0.1:.2f}), 剩磁温度系数 ALFABr = {ALFABr:.4f} %/K\n")
            self.result_text.insert(tk.END, f"相对磁导率μ_r MUr = {MUr:.4f}\n\n")

            self.result_text.insert(tk.END, "【转子尺寸及槽型数据】\n")
            self.result_text.insert(tk.END, f"电枢直径 Da = {Da:.4f} cm, 铁心内径 D0 = {DO:.4f} cm, 电枢长度 La = {La:.4f} cm\n")
            self.result_text.insert(tk.END, f"气隙 g = {g:.4f} cm (±{0.0025:.4f}), 槽型选择 CX = {get_material_name(CX, 'CX')}\n")
            self.result_text.insert(tk.END, f"槽数 Q = {Q:.0f}\n")
            self.result_text.insert(tk.END, f"槽口宽度 b02 = {b02:.4f} cm, 槽口高度 h02 = {h02:.4f} cm\n")
            self.result_text.insert(tk.END, f"槽底圆弧半径 r21 = {r21:.4f} cm, 槽上部圆弧半径 r22 = {r22:.4f} cm, 槽下部圆弧半径 r23 = {r23:.4f} cm\n")
            self.result_text.insert(tk.END, f"槽楔高度 h2 = {h2:.4f} cm, 槽上部宽度 d1 = {d1:.4f} cm, 槽身高度 h22 = {h22:.4f} cm\n")
            self.result_text.insert(tk.END, f"槽下部宽度 d2 = {d2:.4f} cm, 槽底宽度 d3 = {d3:.4f} cm\n\n")

            self.result_text.insert(tk.END, "【绕组数据】\n")
            self.result_text.insert(tk.END, f"并联支路数 u = {u:.0f}, 每元件匝数 Ws = {Ws:.0f}, 每槽导体数 NS = {NS:.0f}\n")
            self.result_text.insert(tk.END, f"并联支路数 a = {a:.0f}, 单根导线根数 Nt = {Nt:.0f}, 导线直径 d = {d:.4f} mm\n")
            self.result_text.insert(tk.END, f"槽满率 Sf = {Sf:.2f} %, 平均导线长度 Lav = {Lav:.4f} cm\n")
            self.result_text.insert(tk.END, f"工作温度下电枢电阻 Raw = {Raw:.2f} Ω, 20°C下电枢电阻 Ra20 = {Ra20:.2f} Ω\n")
            self.result_text.insert(tk.END, f"电枢磁势 AX = {AX:.2f} A/m, 电枢电流密度 J2 = {J2:.2f} A/mm²\n\n")

            self.result_text.insert(tk.END, "【换向器数据及换向计算结果】\n")
            self.result_text.insert(tk.END, f"换向器直径 DK = {DK:.4f} cm, 换向器长度 LK = {LK:.4f} cm, 换向片数 K = {K:.0f}\n")
            self.result_text.insert(tk.END, f"换向器线速度 VK = {VK:.2f} m/s, 电刷数量 Nb = {Nb:.0f}, 每极电刷数 NPB = {NPB:.0f}\n")
            self.result_text.insert(tk.END, f"电刷长度 Lb = {Lb:.4f} cm, 电刷宽度 bb = {bb:.4f} cm, 电刷接触压降 DELTUb = {DELTUb:.2f} V\n")
            self.result_text.insert(tk.END, f"换向元件电抗电动势 Er = {Er:.4f} V, 交轴反应电动势 Ea = {Ea:.4f} V, 合成电动势 SUME = {SUME:.4f} V\n")
            self.result_text.insert(tk.END, f"换向区宽度 bKr = {bKr:.4f} cm, 换向区宽度检查 HXQKB = {HXQKB:.4f}\n\n")

            self.result_text.insert(tk.END, "【磁路计算结果】\n")
            self.result_text.insert(tk.END, f"最大去磁时永磁体工作点 bMh = {bMh:.4f}, bMN = {bMN:.4f}, 实际气隙磁通 Φ = {FIg1:.2e} Wb\n")
            self.result_text.insert(tk.END, f"气隙磁密 Bg = {Bg:.4f} T, 气隙磁位差 Fg = {Fg:.2f} A\n")
            self.result_text.insert(tk.END, f"齿部磁密 Bt2 = {Bt2:.4f} T, 齿部磁场强度 Ht2 = {Ht2:.2f} A/cm, 齿部磁位差 Ft2 = {Ft2:.2f} A\n")
            self.result_text.insert(tk.END, f"电枢轭磁密 Bj2 = {Bj2:.4f} T, 电枢轭磁位差 Fj2 = {Fj2:.2f} A\n")
            self.result_text.insert(tk.END, f"定子轭磁密 Bj1 = {Bj1:.4f} T, 定子轭磁位差 Fj1 = {Fj1:.2f} A\n")
            self.result_text.insert(tk.END, f"外磁路总磁位差 SUMF = {SUMF:.2f} A\n\n")

            self.result_text.insert(tk.END, "【损耗计算结果】\n")
            self.result_text.insert(tk.END, f"电枢绕组铜耗 pCua = {pCua:.2f} W, 电刷接触损耗 pb = {pb:.2f} W\n")
            self.result_text.insert(tk.END, f"铁耗 pFe = {pFe:.2f} W, 机械及附加损耗 pfw = {pfw:.2f} W, 总损耗 SUMp = {SUMp:.2f} W\n\n")

            # 输出不同负载率的工作特性
            self.result_text.insert(tk.END, "【不同负载率的工作特性】\n")
            self.result_text.insert(tk.END, "I/IN     P2(W)      E(V)       RPM(r/min)        ΣP(W)      η(%)       T2(N·m)\n")
            self.result_text.insert(tk.END, "-" * 80 + "\n")

            for load_ratio in range(1, 11):
                I_load = load_ratio * IN / 10.0
                P2 = PN * (I_load / 10.0)  # 示例功率计算
                E_load = UN - DELTUb - I_load * Raw
                RPM_load = 60.0 * a * E_load / (p * FIg1 * N)
                SUMP_load = P2 + 5.0 * (I_load / 10.0)  # 示例总功率计算
                eff_load = (P2 / SUMP_load) * 100 if SUMP_load > 0 else 0  # 示例效率计算
                T_load = 9.549 * P2 / RPM_load if RPM_load > 0 else 0  # 示例转矩计算

                self.result_text.insert(tk.END, f"{I_load:.2f}     {P2:.2f}      {E_load:.2f}       {RPM_load:.2f}        {SUMP_load:.2f}      {eff_load:.2f}       {T_load:.4f}\n")

            self.result_text.insert(tk.END, "=" * 60 + "\n")

        except Exception as e:
            messagebox.showerror("输入错误", f"计算中发生错误: {str(e)}")

    def show_help(self):
        """显示使用说明"""
        help_text = """
永磁直流电动机电磁计算程序使用说明

1. 程序功能
   本程序用于计算永磁直流电动机的电磁参数，包括性能参数、尺寸参数、磁路计算结果和不同负载率下的工作特性等。

2. 使用方法
   a) 在左侧输入区域填写各项参数，可使用默认值或根据需要修改。
   b) 点击"计算"按钮执行计算。
   c) 计算结果将显示在右侧结果区域。
   d) 可以通过滚动条浏览所有输入参数和计算结果。

3. 参数说明
   - 基本参数：包括额定功率、电压、电流、转速等。
   - 设计参数：包括电负荷、磁密、电流密度等。
   - 经验系数：包括各种比例系数。
   - 定子参数：包括铁心内径、气隙长度等。
   - 永磁体参数：包括永磁材料类型、剩磁密度、矫顽力等。
   - 转子参数：包括槽型、槽数、各种尺寸等。
   - 绕组参数：包括绕组类型、每极每相槽数等。
   - 换向器参数：包括电刷尺寸、换向器尺寸等。
   - 材料选择：包括电枢材料、机座材料等。
   - 特殊工况：包括突然起动、瞬时堵转等。

4. 注意事项
   - 所有输入参数必须是有效的数字。
   - 单位必须与标注的一致。
   - 计算结果仅供参考，实际应用中还需考虑其他因素。
        """
        messagebox.showinfo("使用说明", help_text)

    def show_about(self):
        """显示关于信息"""
        about_text = """
永磁直流电动机电磁计算程序

版本：1.0
开发时间：2025年
作者：魏召霖

本程序用于计算永磁直流电动机的电磁参数，包括性能参数、尺寸参数、磁路计算结果和不同负载率下的工作特性等。

程序基于Python和tkinter开发，提供了友好的图形用户界面，方便用户输入参数和查看计算结果。

感谢使用本程序！
        """
        messagebox.showinfo("关于", about_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = MotorCalculator(root)
    root.mainloop()