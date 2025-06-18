import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageOps
import requests
import json
import os
import webbrowser
from bs4 import BeautifulSoup
import random

NB_POKEMON = 386
POKEDEX_FILE = "pokedex_gen1_2_3_fr.json"
IMG_FOLDER = "poke_images"
TYPE_ICON_FOLDER = "type_icons"

TYPE_ICONS = {
    # Clés sans accents/espaces pour robustesse
    "acier": "https://www.pokepedia.fr/images/e/e2/Miniature_Type_Acier_LPA.png",
    "combat": "https://www.pokepedia.fr/images/f/fa/Miniature_Type_Combat_LPA.png",
    "dragon": "https://www.pokepedia.fr/images/3/3f/Miniature_Type_Dragon_LPA.png",
    "eau": "https://www.pokepedia.fr/images/b/b1/Miniature_Type_Eau_LPA.png",
    "electrik": "https://www.pokepedia.fr/images/a/a8/Miniature_Type_%C3%89lectrik_LPA.png",
    "électrik": "https://www.pokepedia.fr/images/a/a8/Miniature_Type_%C3%89lectrik_LPA.png",
    "fee": "https://www.pokepedia.fr/images/a/a7/Miniature_Type_F%C3%A9e_LPA.png",
    "fée": "https://www.pokepedia.fr/images/a/a7/Miniature_Type_F%C3%A9e_LPA.png",
    "feu": "https://www.pokepedia.fr/images/9/97/Miniature_Type_Feu_LPA.png",
    "glace": "https://www.pokepedia.fr/images/f/fd/Miniature_Type_Glace_LPA.png",
    "insecte": "https://www.pokepedia.fr/images/9/95/Miniature_Type_Insecte_LPA.png",
    "normal": "https://www.pokepedia.fr/images/d/d7/Miniature_Type_Normal_LPA.png",
    "plante": "https://www.pokepedia.fr/images/2/2b/Miniature_Type_Plante_LPA.png",
    "poison": "https://www.pokepedia.fr/images/1/17/Miniature_Type_Poison_LPA.png",
    "psy": "https://www.pokepedia.fr/images/9/94/Miniature_Type_Psy_LPA.png",
    "roche": "https://www.pokepedia.fr/images/a/a9/Miniature_Type_Roche_LPA.png",
    "sol": "https://www.pokepedia.fr/images/4/47/Miniature_Type_Sol_LPA.png",
    "spectre": "https://www.pokepedia.fr/images/7/7c/Miniature_Type_Spectre_LPA.png",
    "tenebres": "https://www.pokepedia.fr/images/0/05/Miniature_Type_T%C3%A9n%C3%A8bres_LPA.png",
    "ténèbres": "https://www.pokepedia.fr/images/0/05/Miniature_Type_T%C3%A9n%C3%A8bres_LPA.png",
    "vol": "https://www.pokepedia.fr/images/b/b0/Miniature_Type_Vol_LPA.png",
    # fallback anglais
    "steel": "https://www.pokepedia.fr/images/e/e2/Miniature_Type_Acier_LPA.png",
    "fighting": "https://www.pokepedia.fr/images/f/fa/Miniature_Type_Combat_LPA.png",
    "water": "https://www.pokepedia.fr/images/b/b1/Miniature_Type_Eau_LPA.png",
    "electric": "https://www.pokepedia.fr/images/a/a8/Miniature_Type_%C3%89lectrik_LPA.png",
    "fairy": "https://www.pokepedia.fr/images/a/a7/Miniature_Type_F%C3%A9e_LPA.png",
    "fire": "https://www.pokepedia.fr/images/9/97/Miniature_Type_Feu_LPA.png",
    "ice": "https://www.pokepedia.fr/images/f/fd/Miniature_Type_Glace_LPA.png",
    "bug": "https://www.pokepedia.fr/images/9/95/Miniature_Type_Insecte_LPA.png",
    "grass": "https://www.pokepedia.fr/images/2/2b/Miniature_Type_Plante_LPA.png",
    "poison": "https://www.pokepedia.fr/images/1/17/Miniature_Type_Poison_LPA.png",
    "psychic": "https://www.pokepedia.fr/images/9/94/Miniature_Type_Psy_LPA.png",
    "rock": "https://www.pokepedia.fr/images/a/a9/Miniature_Type_Roche_LPA.png",
    "ground": "https://www.pokepedia.fr/images/4/47/Miniature_Type_Sol_LPA.png",
    "ghost": "https://www.pokepedia.fr/images/7/7c/Miniature_Type_Spectre_LPA.png",
    "dark": "https://www.pokepedia.fr/images/0/05/Miniature_Type_T%C3%A9n%C3%A8bres_LPA.png",
    "flying": "https://www.pokepedia.fr/images/b/b0/Miniature_Type_Vol_LPA.png",
}

type_img_cache = {}

# Relations de dégâts pour chaque type (défense)
TYPE_DEFENSE = {
    "Normal": {"weak": ["Fighting"], "resist": [], "immune": ["Ghost"]},
    "Fire": {"weak": ["Water", "Ground", "Rock"], "resist": ["Fire", "Grass", "Ice", "Bug", "Steel", "Fairy"], "immune": []},
    "Water": {"weak": ["Electric", "Grass"], "resist": ["Fire", "Water", "Ice", "Steel"], "immune": []},
    "Electric": {"weak": ["Ground"], "resist": ["Electric", "Flying", "Steel"], "immune": []},
    "Grass": {"weak": ["Fire", "Ice", "Poison", "Flying", "Bug"], "resist": ["Water", "Electric", "Grass", "Ground"], "immune": []},
    "Ice": {"weak": ["Fire", "Fighting", "Rock", "Steel"], "resist": ["Ice"], "immune": []},
    "Fighting": {"weak": ["Flying", "Psychic", "Fairy"], "resist": ["Bug", "Rock", "Dark"], "immune": []},
    "Poison": {"weak": ["Ground", "Psychic"], "resist": ["Fighting", "Poison", "Bug", "Grass", "Fairy"], "immune": []},
    "Ground": {"weak": ["Water", "Grass", "Ice"], "resist": ["Poison", "Rock"], "immune": ["Electric"]},
    "Flying": {"weak": ["Electric", "Ice", "Rock"], "resist": ["Fighting", "Bug", "Grass"], "immune": ["Ground"]},
    "Psychic": {"weak": ["Bug", "Ghost", "Dark"], "resist": ["Fighting", "Psychic"], "immune": []},
    "Bug": {"weak": ["Fire", "Flying", "Rock"], "resist": ["Fighting", "Ground", "Grass"], "immune": []},
    "Rock": {"weak": ["Water", "Grass", "Fighting", "Ground", "Steel"], "resist": ["Normal", "Fire", "Poison", "Flying"], "immune": []},
    "Ghost": {"weak": ["Ghost", "Dark"], "resist": ["Poison", "Bug"], "immune": ["Normal", "Fighting"]},
    "Dragon": {"weak": ["Ice", "Dragon", "Fairy"], "resist": ["Fire", "Water", "Electric", "Grass"], "immune": []},
    "Dark": {"weak": ["Fighting", "Bug", "Fairy"], "resist": ["Ghost", "Dark"], "immune": ["Psychic"]},
    "Steel": {"weak": ["Fire", "Fighting", "Ground"], "resist": ["Normal", "Grass", "Ice", "Flying", "Psychic", "Bug", "Rock", "Dragon", "Steel", "Fairy"], "immune": ["Poison"]},
    "Fairy": {"weak": ["Poison", "Steel"], "resist": ["Fighting", "Bug", "Dark"], "immune": ["Dragon"]},
}

ALL_TYPES = list(TYPE_DEFENSE.keys())
def get_type_icon_img(t):
    tnorm = (
        t.lower()
         .replace("é", "e")
         .replace("è", "e")
         .replace("ê", "e")
         .replace("â", "a")
         .replace("û", "u")
         .replace("ô", "o")
         .replace("î", "i")
         .replace("à", "a")
         .replace("ï", "i")
         .replace("ë", "e")
         .replace("ç", "c")
         .replace("œ", "oe")
         .replace(" ", "")
    )
    if tnorm in type_img_cache:
        return type_img_cache[tnorm]
    url = TYPE_ICONS.get(tnorm)
    if not url:
        return None
    if not os.path.exists(TYPE_ICON_FOLDER):
        os.makedirs(TYPE_ICON_FOLDER)
    ext = url.split('.')[-1].split('?')[0]
    local_path = os.path.join(TYPE_ICON_FOLDER, f"{tnorm}.{ext}")
    if not os.path.exists(local_path):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                with open(local_path, "wb") as f:
                    f.write(resp.content)
        except Exception:
            return None
    try:
        img = Image.open(local_path).resize((82, 22), Image.LANCZOS)
        tkimg = ImageTk.PhotoImage(img)
        type_img_cache[tnorm] = tkimg
        return tkimg
    except Exception:
        return None

def poke_shoutwiki_link(nom_en):
    return f"https://pokemmo.shoutwiki.com/wiki/{nom_en}"

def telecharger_pokedex():
    print("Téléchargement du Pokédex...")
    pokedex = []
    url_fr = f"https://pokeapi.co/api/v2/pokemon-species?limit={NB_POKEMON}&offset=0"
    response_fr = requests.get(url_fr).json()
    mapping_fr_en = {}
    for entry in response_fr["results"]:
        species = requests.get(entry["url"]).json()
        noms = {name['language']['name']: name['name'] for name in species['names']}
        nom_fr = noms.get('fr', '').capitalize()
        nom_en = noms.get('en', '').capitalize()
        if nom_fr and nom_en:
            mapping_fr_en[nom_fr] = nom_en
    for i in range(1, NB_POKEMON + 1):
        d = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}/").json()
        nom_en = d["name"].capitalize()
        nom_fr = next((fr for fr, en in mapping_fr_en.items() if en == nom_en), nom_en)
        types = [t['type']['name'].capitalize() for t in d['types']]
        poke_dico = {
            "num": d["id"],
            "nom_fr": nom_fr,
            "nom_en": nom_en,
            "type": types,
            "defense": d["stats"][2]["base_stat"],
            "defense_spe": d["stats"][4]["base_stat"],
            "img_url": d["sprites"]["other"]["official-artwork"]["front_default"],
            "img_shiny_url": d["sprites"]["other"]["official-artwork"]["front_shiny"],
        }
        pokedex.append(poke_dico)
    with open(POKEDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(pokedex, f, ensure_ascii=False, indent=2)
    print("Base Pokédex prête !")

def charger_pokedex():
    if not os.path.exists(POKEDEX_FILE):
        telecharger_pokedex()
    with open(POKEDEX_FILE, encoding="utf-8") as f:
        return json.load(f)

def telecharger_image(url, numero, shiny=False):
    if not url:
        return None
    if not os.path.exists(IMG_FOLDER):
        os.makedirs(IMG_FOLDER)
    tag = "_shiny" if shiny else ""
    img_path = os.path.join(IMG_FOLDER, f"{numero}{tag}.png")
    if not os.path.exists(img_path):
        try:
            img_data = requests.get(url).content
            with open(img_path, 'wb') as handler:
                handler.write(img_data)
        except Exception:
            return None
    return img_path

def get_pokemmo_shoutwiki_locations(nom_en):
    url = poke_shoutwiki_link(nom_en)
    try:
        r = requests.get(url, timeout=8)
        if r.status_code != 200:
            return ["Aucune info trouvée sur PokéMMO shoutwiki."]
        soup = BeautifulSoup(r.text, 'html.parser')
        for tag in soup.find_all(['h2', 'h3']):
            ttxt = tag.get_text().strip().lower()
            if ttxt.startswith("location") or ttxt.startswith("localisation"):
                tab = tag.find_next("table")
                if tab:
                    entetes = [th.get_text(" ", strip=True) for th in tab.find_all("th")]
                    lines = []
                    if entetes and len(entetes) > 1:
                        lines.append(" | ".join(entetes))
                    for row in tab.find_all("tr")[1:]:
                        cols = [td.get_text(" ", strip=True) for td in row.find_all(["td", "th"])]
                        if cols and any(c.strip() for c in cols):
                            lines.append(" | ".join(cols))
                    return lines if lines else ["Tableau localisation vide."]
                return ["Aucune table de localisation trouvée."]
        return ["Aucune section 'Location' ou 'Localisation' trouvée."]
    except Exception as e:
        return [f"Erreur localisation: {e}"]

def calc_matchups(types):
    dmg = {t: 1.0 for t in ALL_TYPES}
    for t in types:
        info = TYPE_DEFENSE.get(t, {})
        for w in info.get("weak", []):
            dmg[w] *= 2
        for r in info.get("resist", []):
            dmg[r] *= 0.5
        for im in info.get("immune", []):
            dmg[im] *= 0
    return {
        "immunite": [k for k, v in dmg.items() if v == 0],
        "double_res": [k for k, v in dmg.items() if v == 0.25],
        "res": [k for k, v in dmg.items() if v == 0.5],
        "double_faib": [k for k, v in dmg.items() if v == 4],
        "faib": [k for k, v in dmg.items() if v == 2],
    }

# ---- UI -----
pokedex = charger_pokedex()
IS_SHINY = [False]
current_poke_idx = [0]
poke_img_ref = [None]

root = tk.Tk()
root.title("Pokédex Gen 1 à 3 Deluxe")
root.geometry("1150x800")  # Augmente la hauteur de la fenêtre
root.resizable(False, False)
root.configure(bg="#E4ECF9")

header = tk.Label(root, text="Pokédex Générations 1 à 3 [Shiny + Localisation PokéMMO]", 
                  font=("Segoe UI", 21, "bold"), bg="#496B9A", fg="#fff", pady=8)
header.pack(fill="x")

mainzone = tk.Frame(root, bg="#E4ECF9", width=1150, height=800)  # Largeur et hauteur adaptées
mainzone.pack(fill="both", expand=True)

zone_img = tk.Canvas(mainzone, width=320, height=320, bg="#E7F1FF", bd=0, highlightthickness=0)
zone_img.place(x=36, y=38)
zone_img.create_oval(15, 15, 305, 305, fill="#f8fafe", outline="#C0D0E0")

# -- Gestion bouton shiny rond, petit, centré, grisé en shiny --
def make_round_button_img(img_path, size=44, greyscale=False):
    im = Image.open(img_path).resize((size-10, size-10), Image.LANCZOS).convert("RGBA")
    if greyscale:
        im = ImageOps.grayscale(im).convert("RGBA")
        enhancer = Image.new("RGBA", im.size, (230,230,230,90))
        im = Image.alpha_composite(im, enhancer)
    round_canvas = Image.new("RGBA", (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(round_canvas)
    draw.ellipse((0,0,size-1,size-1), fill="#fff", outline="#FFD700", width=2)
    round_canvas.paste(im, (5,5), im)
    return ImageTk.PhotoImage(round_canvas)

shiny_icon_color = make_round_button_img("Pokemon-GO-Shiny.jpg", greyscale=False)
shiny_icon_grey  = make_round_button_img("Pokemon-GO-Shiny.jpg", greyscale=True)

def update_shiny_btn():
    if IS_SHINY[0]:
        btn_shiny.config(image=shiny_icon_grey, width=44, height=44, bg="#ececec", relief="flat", text='')
    else:
        btn_shiny.config(image=shiny_icon_color, width=44, height=44, bg="#f6e7ff", relief="flat", text='')

def toggle_shiny():
    IS_SHINY[0] = not IS_SHINY[0]
    update_shiny_btn()
    show_poke()

btn_shiny = tk.Button(
    mainzone, image=shiny_icon_color, command=toggle_shiny, bg="#f6e7ff", relief="flat",
    borderwidth=0, highlightthickness=0, activebackground="#faf5d6"
)
btn_shiny.place(x=36+160-22, y=38+275)

fiche_bg = tk.Frame(mainzone, bg="white", bd=2, relief="groove")
fiche_bg.place(x=350, y=38, width=530, height=246)

label_nom = tk.Label(fiche_bg, text="", font=("Segoe UI", 21, "bold"), bg="white", fg="#3a3c68")
label_nom.place(x=20, y=10)
label_num = tk.Label(fiche_bg, text="", font=("Calibri", 13, "bold"), bg="white", fg="#8197e6")
label_num.place(x=20, y=52)

frame_types = tk.Frame(fiche_bg, bg="white")
frame_types.place(x=20, y=90)
label_def = tk.Label(fiche_bg, text="", font=("Segoe UI", 15), bg="white", fg="#1d3454")
label_def.place(x=260, y=70)
label_defspe = tk.Label(fiche_bg, text="", font=("Segoe UI", 15), bg="white", fg="#338b8b")
label_defspe.place(x=260, y=110)
frame_match = tk.Frame(fiche_bg, bg="white")
frame_match.place(x=20, y=130)

# Sous-frames pour les différentes catégories de matchups
frame_match_immu = tk.Frame(frame_match, bg="white")
frame_match_immu.pack(anchor="w")
frame_match_dres = tk.Frame(frame_match, bg="white")
frame_match_dres.pack(anchor="w")
frame_match_res = tk.Frame(frame_match, bg="white")
frame_match_res.pack(anchor="w")
frame_match_dfaib = tk.Frame(frame_match, bg="white")
frame_match_dfaib.pack(anchor="w")
frame_match_faib = tk.Frame(frame_match, bg="white")
frame_match_faib.pack(anchor="w")

def txt_color(bg):
    if bg.startswith("#"):
        hexa = bg[1:]
        if len(hexa) == 3:
            hexa = "".join([c*2 for c in hexa])
        if len(hexa) != 6:
            return "black"
        try:
            r = int(hexa[0:2], 16)
            g = int(hexa[2:4], 16)
            b = int(hexa[4:6], 16)
            return "white" if r*0.299+g*0.587+b*0.114 < 170 else "black"
        except Exception:
            return "black"
    return "black"

def next_poke(event=None):
    current_poke_idx[0] = (current_poke_idx[0] + 1) % len(pokedex)
    IS_SHINY[0] = False
    update_shiny_btn()
    show_poke()
    searchbox.focus_set()

def prev_poke(event=None):
    current_poke_idx[0] = (current_poke_idx[0] - 1 + len(pokedex)) % len(pokedex)
    IS_SHINY[0] = False
    update_shiny_btn()
    show_poke()
    searchbox.focus_set()

def first_poke():
    current_poke_idx[0] = 0
    IS_SHINY[0] = False
    update_shiny_btn()
    show_poke()
    searchbox.focus_set()

def last_poke():
    current_poke_idx[0] = len(pokedex) - 1
    IS_SHINY[0] = False
    update_shiny_btn()
    show_poke()
    searchbox.focus_set()

def random_poke():
    current_poke_idx[0] = random.randint(0, len(pokedex) - 1)
    IS_SHINY[0] = False
    update_shiny_btn()
    show_poke()
    searchbox.focus_set()

def show_poke():
    idx = current_poke_idx[0]
    poke = pokedex[idx]
    is_shiny = IS_SHINY[0]

    label_nom.config(text=f"{poke['nom_fr']} ({poke['nom_en']})" + (" [Shiny]" if is_shiny else ""))
    label_num.config(text=f"N°{poke['num']:03d}")

    # Affichage position/total
    label_pos.config(text=f"{idx+1} / {len(pokedex)}")

    # Types : images ou text fallback
    for wid in frame_types.winfo_children():
        wid.destroy()
    for t in poke["type"]:
        imgtype = get_type_icon_img(t)
        if imgtype:
            icon_label = tk.Label(frame_types, image=imgtype, bg="white")
            icon_label.image = imgtype
            icon_label.pack(side="left", padx=5, pady=2)
        else:
            # Fallback si image non trouvée
            lab = tk.Label(frame_types, text=t, bg="#ffbcbc", fg="black",
                           font=("Segoe UI", 13, "bold"), padx=8, pady=2, borderwidth=2, relief="ridge")
            lab.pack(side="left", padx=5, pady=2)

    label_def.config(text=f"Défense : {poke['defense']}")
    label_defspe.config(text=f"Déf. Spé. : {poke['defense_spe']}")

    for fr in [frame_match_immu, frame_match_dres, frame_match_res, frame_match_dfaib, frame_match_faib]:
        for wid in fr.winfo_children():
            wid.destroy()

    matchs = calc_matchups(poke["type"])

    def fill_frame(fr, title, types):
        if not types:
            return
        tk.Label(fr, text=title, font=("Calibri", 12, "bold"), bg="white", fg="#465a8b").pack(side="left")
        for t in types:
            imgtype = get_type_icon_img(t)
            if imgtype:
                lbl = tk.Label(fr, image=imgtype, bg="white")
                lbl.image = imgtype
                lbl.pack(side="left", padx=2)
            else:
                tk.Label(fr, text=t, bg="#ffbcbc", fg="black", font=("Calibri", 12, "bold"),
                         padx=4, pady=2, borderwidth=1, relief="ridge").pack(side="left", padx=2)

    fill_frame(frame_match_immu, "Immunités :", matchs["immunite"])
    fill_frame(frame_match_dres, "Double rés. :", matchs["double_res"])
    fill_frame(frame_match_res, "Résistances :", matchs["res"])
    fill_frame(frame_match_dfaib, "Double faiblesse :", matchs["double_faib"])
    fill_frame(frame_match_faib, "Faiblesses :", matchs["faib"])

    # Image Pokémon principale
    zone_img.delete("pokeimg")
    img_url = poke['img_shiny_url'] if is_shiny else poke['img_url']
    img_path = telecharger_image(img_url, poke["num"], shiny=is_shiny)
    try:
        img = Image.open(img_path).resize((270, 270))
        poke_img = ImageTk.PhotoImage(img)
        poke_img_ref[0] = poke_img
        zone_img.create_image(160, 160, image=poke_img, tags="pokeimg")
    except Exception:
        zone_img.create_text(160, 160, text="Image\nnon\ntrouvée", font=("Calibri", 14), tags="pokeimg")

    # Localisation PokéMMO shoutwiki
    txt_loc.config(state='normal')
    txt_loc.delete("1.0", "end")
    txt_loc.insert("1.0", "Localisations PokéMMO :\n\n")
    lines = get_pokemmo_shoutwiki_locations(poke['nom_en'])
    for line in lines:
        txt_loc.insert(tk.END, line + "\n")
    txt_loc.config(state='disabled')

def search_poke(event=None):
    s = searchbox.get().lower()
    found = False
    for idx, p in enumerate(pokedex):
        if s in p['nom_fr'].lower() or s in p['nom_en'].lower() or s == str(p['num']):
            current_poke_idx[0] = idx
            IS_SHINY[0] = False
            update_shiny_btn()
            show_poke()
            found = True
            break
    if not found:
        searchbox.config(bg="#ffd6d6")
        tk.messagebox.showinfo("Introuvable", "Aucun Pokémon trouvé.")
    else:
        searchbox.config(bg="white")
    searchbox.focus_set()

def clear_placeholder(event):
    if searchbox.get() == "🔍 Rechercher par nom ou numéro...":
        searchbox.delete(0, tk.END)
        searchbox.config(fg="black")

def add_placeholder(event=None):
    if not searchbox.get():
        searchbox.insert(0, "🔍 Rechercher par nom ou numéro...")
        searchbox.config(fg="#888")

# Localisations PokéMMO
cadre_loc = tk.LabelFrame(mainzone, text="📍 Localisations PokéMMO", bg="#e3f1fa", fg="#29677b",
                         font=("Segoe UI", 13, "bold"), bd=2, relief="groove")
cadre_loc.place(x=36, y=370, width=845, height=185)
txt_loc = tk.Text(
    cadre_loc, width=104, height=7, font=("Consolas", 10),
    bg="#ecfaff", fg="#073851", bd=0, relief="flat", wrap="word"
)
txt_loc.pack(padx=8, pady=8)
txt_loc.config(state='disabled')

searchbox = tk.Entry(mainzone, font=("Segoe UI", 14), width=24, fg="#888")
searchbox.place(x=350, y=300)
searchbox.insert(0, "🔍 Rechercher par nom ou numéro...")
searchbox.bind("<FocusIn>", clear_placeholder)
searchbox.bind("<FocusOut>", add_placeholder)
searchbox.bind("<Return>", search_poke)

# Affichage position/total
label_pos = tk.Label(mainzone, text="", font=("Segoe UI", 11, "bold"), bg="#E4ECF9", fg="#496B9A")
label_pos.place(x=650, y=300)

# Boutons navigation améliorés
btn_first = tk.Button(
    mainzone, text="⏮ Premier", font=("Segoe UI", 11),
    bg="#eaeaff", command=first_poke, width=10
)
btn_first.place(x=350, y=340)
btn_prev = tk.Button(
    mainzone, text="⟵ Précédent", font=("Segoe UI", 11),
    bg="#eaeaff", command=prev_poke, width=12
)
btn_prev.place(x=460, y=340)
btn_next = tk.Button(
    mainzone, text="Suivant ⟶", font=("Segoe UI", 11),
    bg="#eaeaff", command=next_poke, width=12
)
btn_next.place(x=600, y=340)
btn_last = tk.Button(
    mainzone, text="Dernier ⏭", font=("Segoe UI", 11),
    bg="#eaeaff", command=last_poke, width=10
)
btn_last.place(x=720, y=340)
btn_random = tk.Button(
    mainzone, text="🎲 Aléatoire", font=("Segoe UI", 11),
    bg="#ffe7b7", command=random_poke, width=12
)
btn_random.place(x=820, y=300)

# Effet hover sur bouton shiny
def on_shiny_enter(e):
    btn_shiny.config(bg="#ffe066")
def on_shiny_leave(e):
    update_shiny_btn()
btn_shiny.bind("<Enter>", on_shiny_enter)
btn_shiny.bind("<Leave>", on_shiny_leave)

def open_shoutwiki():
    poke = pokedex[current_poke_idx[0]]
    webbrowser.open(poke_shoutwiki_link(poke['nom_en']))

def open_type_info():
    webbrowser.open("https://www.pokepedia.fr/Table_des_types")

btn_lien = tk.Button(
    mainzone, text="🌐 Ouvrir la fiche complète PokéMMO shoutwiki", font=("Segoe UI", 11),
    bg="#bfeae5", command=open_shoutwiki, relief="groove"
)
btn_lien.place(x=350, y=380)
btn_types = tk.Button(
    mainzone, text="ℹ️ Tableau des types", font=("Segoe UI", 11),
    bg="#d5e9ff", command=open_type_info, relief="groove"
)
btn_types.place(x=610, y=380)

root.bind("<Right>", next_poke)
root.bind("<Left>", prev_poke)
root.bind("<Home>", lambda e: first_poke())
root.bind("<End>", lambda e: last_poke())
root.bind("<space>", lambda e: random_poke())

update_shiny_btn()
show_poke()
searchbox.focus()
add_placeholder()

root.mainloop()
