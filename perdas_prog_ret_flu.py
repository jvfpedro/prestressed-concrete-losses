import math

# --- PERDAS PROGRESSIVAS ---

# dados de entrada
n_cord = 14 # numero de cordoalhas

Ac = 1.43 # area da cordoalha (cm2)

e = math.e

Ep = 210 * 10**3 # modulo de elasticidade aco (kPa)

# --- espessura ficticia da peca ---

U = 70 #umidade relativa (tabela norma)

y = 1.5 # coeficiente dependente da umidade relativa do ambiente

A_conc = 8522.99 * 10**(-4) # m2

u_ar = 10.9608 # perimetro da peca em contato com o ar (m)

h_fic = y * (2 * A_conc/u_ar) # espessura ficticia da peca

# --- idade ficticia da peca ---

alpha = 1 # valor de fluencia e retracao para CP-IV

Ti = 25 # temperatura media diaria da regiao

def calcT_fic(delta_t):
    t_fic = alpha * (Ti + 10) / 30 * delta_t # quantidade de dias que a temperatura media diaria pode ser admitida constante

    return t_fic

# --- RETRACAO ---

e_1s = -4 * 10**(-4) # coeficiente dependente da umidade relativa

e_2s = (33 + 2*h_fic)/(20.8 + 3*h_fic)


# para t entre 3 e infinito

def calcBeta_s(t_fic):
    
    # --- coeficientes ---

    A = 40
    B = 116 * h_fic**3 -282 * h_fic**2 + 220 * h_fic - 4.8
    C = 2.5 * h_fic**3 - 8.8 * h_fic + 40.7
    D = -75 * h_fic**3 + 585 * h_fic**2 + 496 * h_fic - 6.8
    E = -169 * (h_fic**4) + 88 * (h_fic**3) + 584 * (h_fic**3) - 39 * (h_fic) + 0.8
    
    beta_s = (((t_fic/100)**3) + A * ((t_fic/100)**2) + B * (t_fic/100)) / (((t_fic/100)**3) + C * ((t_fic/100)**2) + D * (t_fic/100) + E)

    return beta_s

beta_s = (calcBeta_s(calcT_fic(28)) + calcBeta_s(calcT_fic(14))) / 2 # o beta final sera a media dos betas entre os dias das concretagens

e_cs = e_1s * e_2s * (1 - beta_s) # retracao

delta_T = e_cs / (10**(-5))

perda_retracao = Ep * delta_T * 10**(-5) # perda de retracao (Mpa), no infinito

print(f"Perda por retracao: {perda_retracao*1000*Ac*n_cord/10000} kN")

# --- FLUENCIA ---

phi_1c = 2.5 # coeficiente que depende da umidade relativa

phi_2c = (42 + h_fic)/(20 + h_fic) # coeficiente que depende da espessura ficticia

phi_f_inf = phi_1c * phi_2c # valor final do coeficiente de deformacao lenta irreversivel

e_p = (1123.1259 - 200)/1000 # distância entre CG seção e CG armadura (m)

Ix = 0.4656 # m⁴

Mg_1 = 4275 # momento do peso proprio (kN.m) REVISAR

Mg_2 = 20396.51 # momento com o carrgamento permanente (kN.m) REVISAR

p_i = 2510.51 # forca de protensao inicial

def calcBeta_l(dias):
    s = 0.38 # para concreto CP IV

    beta_l = e**(s * (1 - (28/dias)**(1/2)))

    return beta_l

def calcBeta_f(t_fic):
    
    A = 42 * h_fic**3 - 350 * h_fic**2 + 588 * h_fic + 113
    B = 768 * h_fic**3 - 3060 * h_fic**2 + 3234 * h_fic - 23
    C = -200 * h_fic**3 + 13 * h_fic**2 + 1090 * h_fic + 183
    D = 4579 * h_fic**3 - 31916 * h_fic**2 + 35343 * h_fic + 1931

    beta_f = (t_fic**2 + A*t_fic + B) / (t_fic**2 + C*t_fic + D)

    return beta_f

def calcPhi_a(beta_l):
    phi_a = 0.8 * (1 - beta_l)

    return phi_a

def calcPhi_inf(phi_a, beta_f):
    phi_inf = phi_a + phi_f_inf * (1 - beta_f) + 0.4

    return phi_inf

phi_inf_14 = calcPhi_inf(calcPhi_a(calcBeta_l(14)), calcBeta_f(calcT_fic(14)))
phi_inf_28 = calcPhi_inf(calcPhi_a(calcBeta_l(28)), calcBeta_f(calcT_fic(28)))
phi_inf_60 = calcPhi_inf(calcPhi_a(calcBeta_l(60)), calcBeta_f(calcT_fic(60)))

Np0 = (p_i - 174.14 - 183.08 - 43.57) / n_cord # forca de protencao menos as perdas imediatas POR CORDOALHA

sigma_cP01 = ((n_cord * 2) * (-Np0) / A_conc + (n_cord * 2) * (-Np0) * e_p / Ix) * e_p

sigma_cP02 = sigma_cP01

sigma_cg1 = Mg_1/Ix * e_p

sigma_cg2 = Mg_2/Ix * e_p

e_cc = (1/(5600 * math.sqrt(45)*1000)) * ((sigma_cP01 + sigma_cg1) * phi_inf_14 + sigma_cP02 * phi_inf_28 + sigma_cg2 * phi_inf_60)


perda_fluencia = e_cc * Ep * 10**(-3)

print(f"Perda por fluencia: {perda_fluencia*1000*Ac*n_cord/10000} kN")

alpha_p = Ep/(5600*math.sqrt(45))

sigmap_cs = (e_cs*Ep*10**6 + alpha_p*phi_inf_14*(2327.43/A_conc+sigma_cg1) + alpha_p*phi_inf_28*sigma_cP01 + alpha_p*phi_inf_60*sigma_cg2)/(1 - alpha_p*(2327.43/A_conc)/(2327.43/(Ac/10000))*(1+phi_inf_28/2))

print(f"Perda combinada: {sigmap_cs/1000*Ac*n_cord/10000} kN")