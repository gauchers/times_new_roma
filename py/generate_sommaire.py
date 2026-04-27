import csv
import io
import os
import sys

def ref_sort_key(ref):
    """Sort references numerically, handling formats like '1.1', '3-6', '10.18', '1.47-74'"""
    import re
    # Extract first number sequence
    parts = re.split(r'[-.]', ref)
    result = []
    for p in parts:
        try:
            result.append(int(p))
        except ValueError:
            result.append(0)
    return result if result else [0]

def parse_csv_from_document(text):
    """Parse the CSV content from the document"""
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for row in reader:
        rows.append(row)
    return rows

def generate_html(rows):
    # Separate by language
    grecs = [r for r in rows if r['Langue'].strip().lower() == 'grec']
    latins = [r for r in rows if r['Langue'].strip().lower() == 'latin']

    def sort_key(r):
        return (r['Auteur'].strip().lower(), r['Oeuvre'].strip().lower(), ref_sort_key(r['Référence'].strip()))

    grecs_sorted = sorted(grecs, key=sort_key)
    latins_sorted = sorted(latins, key=sort_key)

    def build_table(items):
        rows_html = ""
        for r in items:
            auteur = r['Auteur'].strip()
            oeuvre = r['Oeuvre'].strip()
            ref = r['Référence'].strip()
            titre = r['Titre du texte'].strip()
            rows_html += f"""
            <tr>
                <td class="auteur">{auteur}</td>
                <td class="oeuvre"><em>{oeuvre}</em></td>
                <td class="ref">{ref}</td>
                <td class="titre">{titre}</td>
            </tr>"""
        return rows_html

    grecs_rows = build_table(grecs_sorted)
    latins_rows = build_table(latins_sorted)

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sommaire des textes</title>
    <link rel="stylesheet" href="../css/style_sommaire.css">
</head>
<body>
    <hr class="top-rule">
    <nav>
        <a href="../index.html" class="nav-btn accueil">← Accueil</a>
    </nav>
    <div class="page-wrapper">

        <header class="som-header">
            <h1>Sommaire des textes</h1>
            <p class="subtitle">Textes grecs et latins — classement par auteur, œuvre et référence</p>
        </header>

        <!-- Textes grecs -->
        <section class="som-section">
            <div class="som-section-header">
                <h2 class="som-section-title grec">Textes grecs <span class="count-badge">({len(grecs_sorted)} textes)</span></h2>
            </div>
            <div class="table-container grec grec-table">
                <table>
                    <thead>
                        <tr>
                            <th>Auteur</th>
                            <th>Œuvre</th>
                            <th>Référence</th>
                            <th>Titre du texte</th>
                        </tr>
                    </thead>
                    <tbody>
                        {grecs_rows}
                    </tbody>
                </table>
            </div>
        </section>

        <div class="ornament"><span>✦</span></div>

        <!-- Textes latins -->
        <section class="som-section">
            <div class="som-section-header">
                <h2 class="som-section-title latin">Textes latins <span class="count-badge">({len(latins_sorted)} textes)</span></h2>
            </div>
            <div class="table-container latin latin-table">
                <table>
                    <thead>
                        <tr>
                            <th>Auteur</th>
                            <th>Œuvre</th>
                            <th>Référence</th>
                            <th>Titre du texte</th>
                        </tr>
                    </thead>
                    <tbody>
                        {latins_rows}
                    </tbody>
                </table>
            </div>
        </section>

        <footer class="som-footer">
            <p>Liste des textes référencés</p>
        </footer>

    </div>
</body>
</html>"""

    return html


def main():
    # Chemin fixe vers le fichier CSV source
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', 'csv', 'tableau.csv')

    try:
        with open(csv_path, encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erreur : fichier introuvable — {csv_path}")
        sys.exit(1)

    reader = csv.DictReader(io.StringIO(content))
    rows = list(reader)

    html = generate_html(rows)

    output_path = os.path.join(script_dir, '..', 'html', 'sommaire.html')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Fichier généré : {output_path}")
    print(f"  - Textes grecs  : {len([r for r in rows if r['Langue'].strip().lower() == 'grec'])}")
    print(f"  - Textes latins : {len([r for r in rows if r['Langue'].strip().lower() == 'latin'])}")


if __name__ == '__main__':
    main()
