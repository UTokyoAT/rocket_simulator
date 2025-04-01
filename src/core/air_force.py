import numpy as np


def dynamic_pressure(airspeed:np.ndarray, air_density:float) -> float:
    """動圧を計算する

    Args:
        airspeed (np.ndarray): 剛体系での機体速度
        air_density (float): 空気密度

    Returns:
        float: 動圧
    """
    return 0.5 * air_density * sum(airspeed**2)

def axial_force(airspeed:np.ndarray,air_density:float, body_area:float, axial_force_coefficient:float) -> np.ndarray:
    """軸方向の力を計算する

    Args:
        airspeed (np.ndarray): 剛体系での機体の対気速度
        air_density (float): 空気密度
        body_area (float): 断面積
        axial_force_coefficient (float): 軸方向の力係数CA

    Returns:
        float: 軸方向の力
    """
    p = dynamic_pressure(airspeed, air_density)
    return np.array([-p * body_area * axial_force_coefficient,0,0])

def normal_force(airspeed:np.ndarray,air_density:float, body_area:float, normal_force_coefficient:float) -> np.ndarray:
    """法線方向の力を計算する

    Args:
        airspeed (np.ndarray): 剛体系での機体の対気速度
        air_density (float): 空気密度
        body_area (float): 断面積
        normal_force_coefficient (float): 法線方向の力係数CN

    Returns:
        float: 法線方向の力
    """
    normal_velocity_norm = (airspeed[1]**2 + airspeed[2]**2)**0.5
    if normal_velocity_norm < 1e-4:#０除算を防ぐ
        return np.array([0, 0, 0])
    p = dynamic_pressure(airspeed, air_density)
    direction = np.array([0, -airspeed[1], -airspeed[2]]) / normal_velocity_norm
    return p * body_area * normal_force_coefficient * direction

def angle_of_attack(airspeed:np.ndarray) -> float:
    """迎角を計算する

    Args:
        airspeed (np.ndarray): 剛体系での機体速度

    Returns:
        float: 迎角[rad]（速度ベクトルと機体軸とのなす角度）
    """
    return np.arctan2(np.linalg.norm(airspeed[1:],ord=2), airspeed[0])

def air_dumping_moment(rotation:np.ndarray, roll_damping_coefficient:float, pitch_damping_coefficient:float, yaw_damping_coefficient:float,air_velocity:np.ndarray,overall_length:float,air_density:float,body_area:float) -> np.ndarray:
    """空気抵抗によるモーメントを計算する

    Args:
        rotation (np.ndarray): 機体の角速度
        roll_damping_coefficient (float): ロール軸周りの空気抵抗係数
        pitch_damping_coefficient (float): ピッチ軸周りの空気抵抗係数
        yaw_damping_coefficient (float): ヨー軸周りの空気抵抗係数
        air_velocity (np.ndarray): 剛体系での機体速度
        overall_length (float): 機体の全長
        air_density (float): 空気密度
        body_area (float): 断面積

    Returns:
        np.ndarray: 空気抵抗によるモーメント
    """
    p = dynamic_pressure(air_velocity, air_density)
    return p * body_area * overall_length**2 /2 / np.linalg.norm(air_velocity,ord=2) * np.array([roll_damping_coefficient, pitch_damping_coefficient, yaw_damping_coefficient]) * rotation

def air_force_moment(force:np.ndarray, wind_center:np.ndarray,propellant_CG_distance:float,nozzle_CG_distance:float,m_dot:float,rotation:np.ndarray,
                     roll_damping_coefficient:float,pitch_damping_coefficient:float,yaw_damping_coefficient:float,air_velocity:np.ndarray,overall_length:float,air_density:float,body_area:float)-> np.ndarray:
    """力のモーメントを計算する

    Args:
        force (np.ndarray): 剛体系での力
        wind_center (np.ndarray): 重心から見た風圧中心
        propellant_CG_distance (float): 重心から見た推進剤までの距離
        nozzle_CG_distance (float): 重心から見たノズルまでの距離
        m_dot (float): 推進剤の質量流量
        rotation (np.ndarray): 機体の角速度

    Returns:
        np.ndarray: モーメント
    """
    return np.cross(wind_center, force) - m_dot * (nozzle_CG_distance ** 2 - propellant_CG_distance ** 2) * rotation + air_dumping_moment(rotation, roll_damping_coefficient, pitch_damping_coefficient, yaw_damping_coefficient,air_velocity,overall_length,air_density,body_area)

def normal_force_coefficient(angle_of_attack:float,CN_alpha) -> float:
    """法線方向の力係数を計算する

    Args:
        angle_of_attack (float): 迎角[rad]
        CN_alpha (float): 法線方向の力係数の迎角に対する傾き

    Returns:
        float: 法線方向の力係数
    """
    return CN_alpha * angle_of_attack