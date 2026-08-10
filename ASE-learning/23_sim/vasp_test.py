import os
from datetime import datetime
from pathlib import Path

from ase import Atoms
from ase.calculators.vasp import Vasp


# =========================
# 1. VASP安装位置
# =========================
vasp_binary = "/home/xv/apps/vasp.6.5.0/bin/vasp_std"
vasp_pp_path = "/home/xv/apps/POT"

# 检查VASP程序是否存在
if not Path(vasp_binary).is_file():
    raise FileNotFoundError(f"没有找到VASP程序：{vasp_binary}")

# 检查H的PBE赝势是否存在
h_potcar = Path(vasp_pp_path) / "potpaw_PBE" / "H" / "POTCAR"

if not h_potcar.is_file():
    raise FileNotFoundError(f"没有找到H赝势：{h_potcar}")

# ASE寻找赝势时使用这个环境变量
os.environ["VASP_PP_PATH"] = vasp_pp_path

# 限制每个MPI进程只使用一个线程
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["I_MPI_PIN"] = "0"

# 使用两个MPI进程运行VASP
vasp_command = f"mpirun -np 2 {vasp_binary}"

# 每次使用一个新目录，避免读取以前失败计算留下的文件
run_directory = f"vasp_smoke_h2_{datetime.now():%Y%m%d_%H%M%S}"


# =========================
# 2. 创建H2分子
# =========================
h2 = Atoms(
    symbols="H2",
    positions=[
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.74]
    ],
    cell=[10.0, 10.0, 10.0],
    pbc=True
)

# 把H2放在真空盒中央
h2.center()


# =========================
# 3. 创建VASP计算器
# =========================
calculator = Vasp(
    command=vasp_command,
    directory=run_directory,
    txt="vasp.out",

    xc="PBE",
    encut=300,
    prec="Normal",

    kpts=(1, 1, 1),
    gamma=True,

    ismear=0,
    sigma=0.05,

    ediff=1e-5,
    nelm=60,
    algo="Normal",

    ibrion=-1,
    nsw=0,

    istart=0,
    icharg=2,

    lreal=False,
    lscalapack=False,
    ncore=1,

    lwave=False,
    lcharg=False
)

h2.calc = calculator


# =========================
# 4. 开始计算
# =========================
print("===== VASP smoke test =====", flush=True)
print(f"VASP command: {vasp_command}", flush=True)
print(f"Calculation directory: {run_directory}", flush=True)
print("Starting H2 calculation...", flush=True)

energy = h2.get_potential_energy()
forces = h2.get_forces()

print("\n===== Test passed =====")
print(f"H2 total energy: {energy:.8f} eV")
print("Forces (eV/Å):")
print(forces)
print(f"Results saved in: {run_directory}")