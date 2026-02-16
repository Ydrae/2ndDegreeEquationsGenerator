import streamlit as st

# --- Tes fonctions originales adaptées pour l'affichage UI ---

def gen_int_roots(a=None,b=None,c=None,x_1=None,x_2=None):
    """
    Génère des équations du second degré à racines entières, en fonction des paramètres donnés.
    Si un paramètre est None, il peut prendre n'importe quelle valeur entière de -7 à 7.
    Si un paramètre est une valeur, il doit être égal à cette valeur.
    Si un paramètre est une liste de valeurs, il doit être égal à l'une de ces valeurs.
    
    :param a: None ou nombre voulu ou liste de nombres voulus
    :param b: Nombre voulu
    :param c: Nombre voulu
    :param x_1: None ou nombre voulu ou liste de nombres voulus
    :param x_2: None ou nombre voulu ou liste de nombres voulus
    """
    results = []
    range_a = range_values(a)
    range_x_1 = range_values(x_1)
    range_x_2 = range_values(x_2)
    for candidat_x_1 in range_x_1:
        for candidat_x_2 in range_x_2:
            if (x_1 is None) and (candidat_x_2<=candidat_x_1): continue
            for candidat_a in range_a:
                if candidat_a == 0: continue # Si a = 0, ce n'est pas une équation du second degré
                Delta = (candidat_a*(candidat_x_2-candidat_x_1))**2
                if Delta > 169: continue # Trop grand pour calculer
                candidat_b = -candidat_a*(candidat_x_1+candidat_x_2)
                if (b is not None) and (candidat_b > 13) or (candidat_b < -13): continue # Trop grand pour calculer
                if (b is not None) and (candidat_b != b): # Si l'utilisateur a demandé un b précis et que ce n'est pas celui que nous avons calculé, on continue
                    continue
                candidat_c = candidat_a*candidat_x_1*candidat_x_2 
                if (c is not None) and (candidat_c != c): # Si l'utilisateur a demandé un c précis et que ce n'est pas celui que nous avons calculé, on continue
                    continue
                x_1_print = f"-{candidat_x_1}" if candidat_x_1 >= 0 else f"+{-candidat_x_1}"
                x_2_print = f"-{candidat_x_2}" if candidat_x_2 >= 0 else f"+{-candidat_x_2}"
                b_print = f"+{candidat_b}" if candidat_b >= 0 else f"-{-candidat_b}"
                c_print = f"+{candidat_c}" if candidat_c >= 0 else f"-{-candidat_c}"

                res = f"{candidat_a}x²{b_print}x{c_print} <=> {candidat_a}(x{x_1_print})(x{x_2_print}) et Delta = {Delta}"
                results.append(res)

    return results

def gen_frac_roots(a=None, b=None, c=None, x_1=None, x_2=None):
    """
    Génère des équations du second degré avec exactement une racine fractionnaire.

    On construit les équations sous la forme :
        (a x + e)(x - sol)

    avec :
        - sol entier
        - -e/d non entier

    Si un paramètre est None : valeurs entières de -7 à 7.
    Si un paramètre est une valeur : il doit être égal à cette valeur.
    Si un paramètre est une liste : il doit appartenir à cette liste.

    :param a: None ou nombre voulu ou liste
    :param b: None ou nombre voulu
    :param c: None ou nombre voulu
    :param x_1: None ou nombre fractionnaire voulu ou liste
    :param x_2: None ou nombre entier voulu ou liste
    """

    results = []
    range_a = range_values(a)
    range_sol = range_values(x_1)
    range_e = list(range(-7, 8))

    for candidat_sol in range_sol:
        for candidat_a in range_a:
            if candidat_a == 0:
                continue

            for candidat_e in range_e:
                # Racine fractionnaire = -e/a
                if candidat_e % candidat_a == 0:
                    continue  # racine entière → on exclut

                racine_frac = -candidat_e / candidat_a

                # Racines
                r2 = candidat_sol
                r1 = racine_frac

                candidat_a = candidat_a
                candidat_b = candidat_e - candidat_a * candidat_sol
                if (b is not None) and (candidat_b > 13 or candidat_b < -13):
                    continue  # Trop grand pour calculer
                candidat_c = -candidat_e * candidat_sol

                Delta = candidat_b**2 - 4*candidat_a*candidat_c
                if Delta > 169:
                    continue

                if (b is not None) and (candidat_b != b):
                    continue

                if (c is not None) and (candidat_c != c):
                    continue

                # Gestion des contraintes sur x_2 si fournies
                if x_2 is not None:
                    if isinstance(x_2, list):
                        if r2 not in x_2:
                            continue
                    else:
                        if r2 != x_2:
                            continue
                
                if x_1 is not None:
                    if isinstance(x_1, list):
                        if r1 not in x_1:
                            continue
                    else:
                        if r1 != x_1:
                            continue

                x2_print = f"-{r2}" if r2 >= 0 else f"+{-r2}"
                e_print = f"+{candidat_e}" if candidat_e >= 0 else f"-{-candidat_e}"
                b_print = f"+{candidat_b}" if candidat_b >= 0 else f"-{-candidat_b}"
                c_print = f"+{candidat_c}" if candidat_c >= 0 else f"-{-candidat_c}"

                res = f"{candidat_a}x²{b_print}x{c_print} <=> ({candidat_a}x{e_print})(x{x2_print}) et Delta = {Delta}"
                results.append(res)
    return results

def range_values(t):
    """
    Si t est None : retourne les entiers de -7 à 7.
    Si t est une valeur, retourne la liste ne contenant que la valeur.
    Si t est une liste de valeurs, retourne la liste de ces valeurs.
    
    :param t: la valeur dont on veut choisir les valeurs à itérer.
    """
    if t is None:
        return list(range(-7, 8))
    elif isinstance(t, list):
        return t
    else:
        return [t]

# --- Interface Utilisateur Streamlit ---

st.set_page_config(page_title="Générateur d'Équations", page_icon="🎓", layout="wide")

st.title("🎓 Générateur d'Équations du 2nd Degré")

# 1. Choix du mode et Indications
mode = st.radio(
    "Type de racines souhaitées :", 
    ["Entières", "Fractionnaires"],
    horizontal=True
)

if mode == "Entières":
    st.info("💡 **Mode Entier** : Le programme garantit $x_1 < x_2$.")
else:
    st.info("💡 **Mode Fractionnaire** : $x_1$ est la racine fractionnaire, $x_2$ est la racine entière.")

st.divider()

# 2. Construction dynamique des paramètres
st.subheader("Configuration des paramètres")
st.write("Cochez une case pour fixer une plage de valeurs, sinon le paramètre sera libre.")

# On crée 5 colonnes pour que ce soit visuellement léger
cols = st.columns(5)
params_final = {}

# Configuration des paramètres (a, b, c, x1, x2)
config = [
    ("Valeur de a", "a"),
    ("Valeur de b", "b"),
    ("Valeur de c", "c"),
    ("Valeur de x₁", "x_1"),
    ("Valeur de x₂", "x_2")
]

for i, (label, key) in enumerate(config):
    with cols[i]:
        activated = st.checkbox(f"Fixer {key}", key=f"check_{key}")
        if activated:
            # Double curseur pour définir la plage [min, max]
            # On transforme la plage en liste pour tes fonctions
            val_range = st.select_slider(
                f"Plage {key}",
                options=list(range(-10, 11)),
                value=(-7, 7),
                key=f"slider_{key}"
            )
            params_final[key] = list(range(val_range[0], val_range[1] + 1))
        else:
            params_final[key] = None

st.divider()

# 3. Bouton de génération
if st.button("🚀 Générer les équations", type="primary", use_container_width=True):
    
    with st.spinner("Calcul des combinaisons possibles..."):
        if mode == "Entières":
            # Appel de la fonction pour racines entières
            equations = gen_int_roots(
                a=params_final["a"],
                b=params_final["b"],
                c=params_final["c"],
                x_1=params_final["x_1"],
                x_2=params_final["x_2"]
            )
        else:
            # Appel de la fonction pour racines fractionnaires
            equations = gen_frac_roots(
                a=params_final["a"],
                b=params_final["b"],
                c=params_final["c"],
                x_1=params_final["x_1"],
                x_2=params_final["x_2"]
            )

    # 4. Affichage des résultats
    if equations:
        st.success(f"✅ {len(equations)} équations trouvées.")
        
        # Affichage en grille pour gagner de la place
        res_cols = st.columns(2)
        for idx, eq in enumerate(equations):
            # On alterne entre colonne 1 et 2
            res_cols[idx % 2].code(eq, language="text")
            
            # Sécurité pour ne pas faire ramer le navigateur si trop de résultats
            if idx >= 99:
                st.warning("Affichage limité aux 100 premiers résultats.")
                break
    else:
        st.error("❌ Aucune équation ne correspond à ces critères. Essayez d'élargir les plages de valeurs.")