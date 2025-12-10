import math

# --- PERDAS PROGRESSIVAS ---

# dados de entrada

n_cord = 14 # numero de cordoalhas

Ac = 1.43 # area da cordoalha (cm2)

fptk = 1900 # MPa

Ep = 210 * 10**3 # modulo de elasticidade aco (kPa)

tensao_i = 0.77 * fptk # a tensão da armadura de protensão na saída do aparelho de tração (MPa)

p_i = (tensao_i * 10**6) * (Ac * 10**(-4)) * n_cord / 1000 # forca de protencao inicial (kN)

Np0 = (p_i - 174.14 - 183.08 - 43.57) / n_cord # forca de protencao menos as perdas imediatas POR CORDOALHA

sigma_p_c_s = 1113980.878342043 # kPa TROCAR PELO VALOR REAL em modulo

sigma_pi = (n_cord*Np0) / (Ac/10000 * n_cord) # tensao inicial em kPa

# --- relaxacao pura ---

tabela = sigma_pi/1000 / fptk

tabela = 0.647073978652926

psi = (3.5 + (7.0 - 3.5) * ((tabela - 0.6) / (0.7 - 0.6))) # interpolacao da tabela (%)

sigma_rp = (psi/100 * sigma_pi)/1000 # MPa

# --- relaxacao relativa ---

sigma_rr = sigma_rp * (1 - 2*sigma_p_c_s/sigma_pi)

perda_relaxacao = sigma_rr * n_cord * Ac/10000 * 1000

print(f"Perda por relaxacao: {perda_relaxacao} kN")