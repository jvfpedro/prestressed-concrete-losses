import math

# --- PERDAS IMEDIATAS ---

# dados de entrada

Ac = 1.43 # area da cordoalha (cm2)

A_conc = 8522.99 # cm2

Ix = 0.4656 # m⁴

Mg = 4275 # kN.m

n_cabos = 4 # numero de cabos

f_ptk = 1900 # Valor característico de resistência a tração do aço CP-190-RB (MPa)

n_cord = 14 # numero de cordoalhas

e = math.e # euler

u = 0.2 # coeficiente de atrito aparente entre cabo e bainha

k = 2*10**(-3) # coeficiente de perda por metro provocada por curvaturas não intencionais no cabo
 
l = 40 # tamanho da viga (m)

a = 15  # distancia ate o fim do trecho parabólico (m)

cobrimento_inf = 23 #cm

fck_14 = 0.9016 * 45 # MPa (fck aos 14 dias - pior caso)

fck_28 = 45 # MPa (fck aos 28)

# calculos iniciais de protensao

tensao_i = 0.77 * f_ptk # a tensão da armadura de protensão na saída do aparelho de tração (MPa)

p_i = (tensao_i * 10**6) * (Ac * 10**(-4)) * n_cord / 1000 # forca de protencao inicial (kN)

delta_w = 2 / 1000  # recuo típico da ancoragem (m)

Ep = 210 * 10**6  # módulo de elasticidade do aço (Pa)

Ap = Ac * 12 / 10000 # área da armadura por cabo (m²)


# -----PERDA POR ATRITO-----

def calcPerdaAtrito(alpha, l):

    alpha = math.radians(alpha)

    p_0 = p_i * (1-e**(-(u * alpha + k * l)))
    
    return p_0


# -----PERDA POR ACOMODAÇÃO DA ANCORAGEM-----

# Hipótese 1: w <= a
def calcPerdaAcomodacao(alpha):

    delta_p1 = (p_i - p_i * (e**(-(u * alpha * k * a))))/a  # coeficiente angular da reta
    
    w1 = math.sqrt((delta_w * Ep * Ap) / (delta_p1))  # m

    if w1 <= a:
        perda = 2 * delta_p1 * w1  # perda total (kN)
        return perda, 1, w1

    # Hipótese 2: a < w <= l/2
    A = delta_p1 * 1000
    B = 2 * delta_p1 * 1000 * a
    C = delta_p1 * 1000 * a**2 - delta_w * Ep * Ap

    delta = B**2 - 4 * A * C
    if delta >= 0:
        w_linha = (-B + math.sqrt(delta)) / (2 * A)
        w2 = a + w_linha
        if w2 <= l / 2:
            delta_p2 = delta_p1  # aproximação conservadora
            perda = 2 * delta_p1 * a + 2 * delta_p2 * w_linha  # perda total (kN)
            return perda, 2, w2

    # Hipótese 3: w > l/2, NAO CHEGARA!!
    S1 = 2 * delta_p1 * a
    delta_p2 = delta_p1  # aproximação conservadora
    S2 = 2 * delta_p2 * ((l / 2) - a)
    perda = S1 + S2  # perda total (kN)
    return perda, 3

# Cálculo da perda por acomodação da ancoragem
perda_anc_1, hipotese_1, w_1 = calcPerdaAcomodacao(12)
perda_anc_2, hipotese_2, w_2 = calcPerdaAcomodacao(10)
perda_anc_3, hipotese_3, w_3 = calcPerdaAcomodacao(8)
perda_anc_4, hipotese_4, w_4 = calcPerdaAcomodacao(6)


# ----- PERDA POR ENCURTAMENTO IMEDIATO DO CONCRETO -----

def calcPerdaEncurtamentoImediato():
    Eci_14 = 5600 * math.sqrt(fck_14)      # módulo de elasticidade do concreto em 14 dias (Pa)
    Eci_28 = 5600 * math.sqrt(fck_28)      # módulo de elasticidade do concreto em 28 dias (Pa)
    Eci_media = (Eci_14 + Eci_28) / 2      # média dos módulos entre 14 e 28 dias
    alpha_p = Ep * 10**(-3) / Eci_media
    e_p = 1123.1259 - 200 # distância entre CG seção e CG armadura (mm)
    p_0_cabo1 = p_i - calcPerdaAtrito(12, l/2) - perda_anc_1
    p_0_cabo2 = p_i - calcPerdaAtrito(10, l/2) - perda_anc_2
    p_0_cabo3 = p_i - calcPerdaAtrito(8, l/2) - perda_anc_3
    p_0_cabo4 = p_i - calcPerdaAtrito(6, l/2) - perda_anc_4
    soma_N = -(p_0_cabo1 + p_0_cabo2 + p_0_cabo3 + p_0_cabo4) # kN
    sigma_cp = (soma_N/(A_conc/10000))+((((soma_N * (e_p/1000)) / Ix) * e_p/1000)) # kPa
    sigma_cg = Mg * (e_p/1000) / Ix # kPa
    delta_sigma_p = (2 - 1) / (2 * 2) * alpha_p * (sigma_cg + sigma_cp) # kPa (n = 2 pois é protendido de 2 em 2)
    perda_encurt = 12*Ac*10**(-4)*(-delta_sigma_p)

    return perda_encurt

# ----- RESULTADOS -----

print(f"Força de protensão inicial: {p_i:.2f} kN")
print()
print("Perda por atrito:")
print(f"Cabo 1 AB = {calcPerdaAtrito(12, 15):.2f} kN, BC = {calcPerdaAtrito(0, 5):.2f}")
print(f"Cabo 2 AB = {calcPerdaAtrito(10, 15):.2f} kN, BC = {calcPerdaAtrito(0, 5):.2f}")
print(f"Cabo 3 AB = {calcPerdaAtrito(8, 15):.2f} kN, BC = {calcPerdaAtrito(0, 5):.2f}")
print(f"Cabo 4 AB = {calcPerdaAtrito(6, 15):.2f} kN, BC = {calcPerdaAtrito(0, 5):.2f}")
print()
print("Perda por acomodação da ancoragem:")
print(f"Cabo 1 = {perda_anc_1:.2f} kN, (Hipótese {hipotese_1}) e w = {w_1:.4f} m")
print(f"Cabo 2 = {perda_anc_2:.2f} kN, (Hipótese {hipotese_2}) e w = {w_2:.4f} m")
print(f"Cabo 3 = {perda_anc_3:.2f} kN, (Hipótese {hipotese_3}) e w = {w_3:.4f} m")
print(f"Cabo 4 = {perda_anc_4:.2f} kN, (Hipótese {hipotese_4}) e w = {w_4:.4f} m")
print()
print(f"Perda por encurtamento imediato do concreto por cabo (média): {calcPerdaEncurtamentoImediato():.2f} kN")