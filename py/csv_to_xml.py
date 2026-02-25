import csv
import os
import re
import unicodedata
from xml.sax.saxutils import escape

# =========================
# 0. Chemins robustes
# =========================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

CSV_FILE = os.path.join(BASE_DIR, "csv", "tableau.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "tei")

os.makedirs(OUTPUT_DIR, exist_ok=True)

if not os.path.exists(CSV_FILE):
    raise FileNotFoundError(f"CSV introuvable : {CSV_FILE}")

# =========================
# 1. Dictionnaire ANA
# =========================

ANA_LABELS = {
    "conjugaison": {
        "indicatif_present": "Indicatif présent",
        "indicatif_imparfait": "Indicatif imparfait",
        "indicatif_parfait": "Indicatif parfait",
        "indicatif_plus_que_parfait": "Indicatif plus-que-parfait",
        "indicatif_aoriste": "Indicatif aoriste",
        "indicatif_futur": "Indicatif futur",
        "indicatif_futur_anterieur": "Indicatif futur antérieur",

        "subjonctif_present": "Subjonctif présent",
        "subjonctif_imparfait": "Subjonctif imparfait",
        "subjonctif_parfait": "Subjonctif parfait",
        "subjonctif_plus_que_parfait": "Subjonctif plus-que-parfait",

        "imperatif_present": "Impératif présent",

        "infinitif_present": "Infinitif présent",
        "infinitif_present": "Infinitif présent actif",
        "infinitif_present": "Infinitif présent passif",
        "infinitif_parfait": "Infinitif parfait",
        "infinitif_parfait": "Infinitif parfait passif",
        "infinitif_futur": "Infinitif futur",

        "participe_present": "Participe présent",
        "participe_parfait": "Participe parfait",
        "participe_futur": "Participe futur",
        "participe_substantive": "Participe substantivé",

        "adjectif_verbal": "Adjectif verbal",
        "gerondif": "Gérondif",

        "deponent": "Déponent"
    },
        "morphologie": {
        "comparatif": "Comparatif",
        "comparatif_adverbe": "Comparatif de l'adverbe",
        "superlatif": "Superlatif",

        "ipse": "ipse, a, um",
        "is": "is, ea, id",
        "ille": "ille, illa, illud",
        "hic": "hic, haec, hoc",
        "idem": "idem, eadem, idem",

        "qui": "qui, quae, quod",
        "quis": "quis, quae, quid"
    },

    "syntaxe": {
        "proposition_infinitive": "Proposition infinitive",
        "proposition_relative_indicatif": "Proposition relative (indicatif)",
        "proposition_relative_subjonctif": "Proposition relative (subjonctif)",
        "relatif_liaison": "Relatif de liaison",

        "completive_ut_subjonctif": "Complétive ut + subjonctif",
        "completive_ne_subjonctif": "Complétive ne + subjonctif",

        "interrogative_directe": "Interrogative directe",
        "interrogative_indirecte": "Interrogative indirecte",
        "exclamative": "Exclamative",

        "discours_indirect": "Discours indirect",

        "circonstancielle_temps_indicatif": "Circonstancielle de temps (indicatif)",
        "circonstancielle_causale_indicatif": "Circonstancielle causale (indicatif)",
        "circonstancielle_concessive_indicatif": "Circonstancielle concessive (indicatif)",
        "circonstancielle_lieu_qua": "Circonstancielle de lieu (qua)",
        "circonstancielle_lieu_ubi": "Circonstancielle de lieu (ubi)",

        "circonstancielle_finale_subjonctif": "Circonstancielle finale (subjonctif)",
        "circonstancielle_consecutive_subjonctif": "Circonstancielle consécutive (subjonctif)",
        "circonstancielle_causale_subjonctif": "Circonstancielle causale (subjonctif)",
        "circonstancielle_concessive_subjonctif": "Circonstancielle concessive (subjonctif)",

        "comparative_indicatif": "Comparative (indicatif)",
        "complement_comparatif": "Complément du comparatif",
        "quo_comparatif_ut": "quo + comparatif = ut",

        "cum_indicatif": "Cum + indicatif",
        "cum_subjonctif": "Cum + subjonctif",
        "tum_cum": "tum ... cum",
        "quod_subjonctif": "Quod + subjonctif",
        "ut_indicatif": "Ut + indicatif",

        "passif_personnel_infinitif": "Passif personnel + infinitif",
        "tournure_esse_datif": "Tournure esse + datif",
        "attribut_cod": "Attribut du COD",
        "accusatif_exclamatif": "Accusatif exclamatif",
        "ablatif_absolu": "Ablatif absolu",
        "omission_esse": "Omission du verbe esse",

        "adjectif_verbal_epithete": "Adjectif verbal épithète",
        "adjectif_verbal_attribut": "Adjectif verbal attribut",

        "subjonctif_principale": "Subjonctif en principale",

        "systeme_hypothetique_reel": "Système hypothétique (réel)",
        "systeme_hypothetique_eventuel": "Système hypothétique (éventuel)",
        "systeme_hypothetique_irreel_present": "Système hypothétique (irréel du présent)",
        "systeme_hypothetique_irreel_passe": "Système hypothétique (irréel du passé)"
    }
}

# =========================
# 2. Fonctions utilitaires
# =========================

def slug(text):
    if not text:
        return "inconnu"

    text = text.replace(".", "_")
    text = text.replace("'", "_")

    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")

    text = text.lower()
    text = re.sub(r"[^\w]+", "_", text)

    return re.sub(r"_+", "_", text).strip("_")


def xml_safe(text):
    return escape(text.strip()) if text else ""


def normalize(text):
    return re.sub(r"\s+", " ", text.strip()) if text else ""


def build_ana(field_value, category):
    if not field_value:
        return ""

    field_value = normalize(field_value)
    result = []

    for key, label in ANA_LABELS[category].items():
        if label in field_value:
            result.append(key)

    return " ".join(result)


def prose_poesie(value):
    return slug(value) if value else ""


def langue(value):
    codes = {"Latin": "la", "Grec": "grc"}
    return codes.get(value, value.lower() if value else "")


def lines_to_l(text):
    """
    Transforme un texte avec sauts de ligne en balises <l>
    """
    if not text:
        return ""

    lines = re.split(r"\r?\n+", text.strip())

    return "\n        ".join(
        f"<l>{xml_safe(line)}</l>"
        for line in lines
        if line.strip()
    )

# =========================
# 3. Lecture CSV → TEI
# =========================

with open(CSV_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for i, row in enumerate(reader, start=1):

        auteur = row.get("Auteur", "")
        oeuvre = row.get("Oeuvre", "")
        ref = row.get("Référence", "")
        langue_code = langue(row.get("Langue", ""))

        filename = os.path.join(
            OUTPUT_DIR,
            f"{slug(langue_code)}_{slug(auteur)}_{slug(oeuvre)}_{slug(ref)}.xml"
        )

        title_fichier = (
            f"{slug(langue_code)}_{slug(auteur)}_{slug(oeuvre)}_{slug(ref)}.xml"
        )

        ana_conj = build_ana(row.get("Conj"), "conjugaison")
        ana_morph = build_ana(row.get("Morphologie"), "morphologie")
        ana_syn = build_ana(row.get("Syntaxe"), "syntaxe")

        tei = f'''<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>{xml_safe(row.get("Titre du texte"))}</title>

        <respStmt>
          <resp>Contributeur</resp>
          <name role="contributeur">{xml_safe(row.get("Contributrice"))}</name>
        </respStmt>

        <respStmt>
          <resp>Traducteur</resp>
          <name role="traducteur">{xml_safe(row.get("Crédit Traduction"))}</name>
        </respStmt>

        <respStmt>
          <resp>Encodage</resp>
          <name>Sarah GAUCHER</name>
        </respStmt>

        <principal>Sarah GAUCHER</principal>
      </titleStmt>

      <publicationStmt>
        <p>Publication interne</p>
      </publicationStmt>

      <sourceDesc>
        <listBibl>
          <bibl>
            <author>{xml_safe(auteur)}</author>
            <title type="oeuvre">{xml_safe(oeuvre)}</title>
            <title type="fichier">{xml_safe(title_fichier)}</title>
            <biblScope>{xml_safe(ref)}</biblScope>

            <term type="prose/poésie" subtype="{prose_poesie(row.get('Prose/poésie'))}"/>
            <term type="mots" n="{row.get('Nombre de mots','')}"/>
            <term type="niveau" n="{row.get('Niveau','')}"/>
            <term type="coupe" subtype="{'oui' if row.get('Coupes') == 'TRUE' else 'non'}"/>

            {f'<term type="conjugaison" ana="{ana_conj}"/>' if ana_conj else ''}
            {f'<term type="morphologie" ana="{ana_morph}"/>' if ana_morph else ''}
            {f'<term type="syntaxe" ana="{ana_syn}"/>' if ana_syn else ''}
          </bibl>
        </listBibl>
      </sourceDesc>
    </fileDesc>

    <profileDesc>
      <langUsage>
        <language ident="{langue_code}"/>
      </langUsage>
    </profileDesc>
  </teiHeader>

  <text>
    <body>
      <ab type="orig" xml:id="texte_{i}">
        {lines_to_l(row.get('Texte latin/grec'))}
      </ab>

      <ab type="trad" corresp="#texte_{i}">
        {lines_to_l(row.get('Traduction'))}
      </ab>
    </body>
  </text>
</TEI>
'''

        with open(filename, "w", encoding="utf-8") as out:
            out.write(tei)

        print(f"✔ TEI créé : {filename}")

