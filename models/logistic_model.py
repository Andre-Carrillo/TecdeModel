import numpy as np

def logistic_with_harvest(p0, r, K, tmax, h=5):
    """
    Modelo logístico con cosecha constante.
    
    Parámetros:
    -----------
    p0 : float
        Población inicial
    r : float
        Tasa de crecimiento
    K : float
        Capacidad de carga
    tmax : float
        Tiempo máximo
    h : float
        Tasa de cosecha constante

    Retorna:
    --------
    t : np.ndarray
        Vector de tiempos
    P : np.ndarray
        Vector de poblaciones
    """

    t = np.linspace(0, tmax, 200)
    dt = t[1] - t[0]
    P = np.zeros_like(t)
    P[0] = p0

    # Solución numérica con método de Euler
    for i in range(1, len(t)):
        dPdt = r * P[i-1] * (1 - P[i-1]/K) - h
        P[i] = P[i-1] + dPdt * dt
        if P[i] < 0:
            P[i] = 0  # evitar valores negativos

    return t, P
