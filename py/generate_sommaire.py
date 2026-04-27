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
    <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Cormorant+SC:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --parchment: #f5f0e8;
            --parchment-dark: #ede5d0;
            --ink: #1a1208;
            --ink-light: #3d2e0e;
            --ink-faded: #6b5533;
            --red-accent: #8b1a1a;
            --gold: #b8860b;
            --gold-light: #d4a017;
            --border: #c8b888;
            --border-light: #ddd0a8;
            --shadow: rgba(26, 18, 8, 0.12);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background-color: var(--parchment-dark);
            background-image: 
                radial-gradient(ellipse at 20% 50%, rgba(180,150,80,0.08) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 20%, rgba(139,26,26,0.05) 0%, transparent 50%),
                url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='400' height='400' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
            color: var(--ink);
            font-family: 'EB Garamond', Georgia, serif;
            font-size: 16px;
            line-height: 1.6;
            min-height: 100vh;
        }}

        .page-wrapper {{
            max-width: 920px;
            margin: 0 auto;
            padding: 60px 40px 80px;
        }}

        /* Header */
        .header {{
            text-align: center;
            margin-bottom: 64px;
            padding-bottom: 40px;
            border-bottom: 1px solid var(--border);
            position: relative;
        }}

        .header::before {{
            content: '✦';
            display: block;
            font-size: 18px;
            color: var(--gold);
            margin-bottom: 20px;
            letter-spacing: 12px;
        }}

        .header h1 {{
            font-family: 'Cormorant SC', serif;
            font-size: 2.8rem;
            font-weight: 500;
            letter-spacing: 0.08em;
            color: var(--ink);
            margin-bottom: 10px;
            line-height: 1.2;
        }}

        .header .subtitle {{
            font-family: 'EB Garamond', serif;
            font-size: 1rem;
            font-style: italic;
            color: var(--ink-faded);
            letter-spacing: 0.05em;
        }}

        .ornament {{
            text-align: center;
            color: var(--gold);
            font-size: 14px;
            letter-spacing: 8px;
            margin: 28px 0;
        }}

        /* Section */
        .section {{
            margin-bottom: 60px;
        }}

        .section-header {{
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 28px;
        }}

        .section-header::before,
        .section-header::after {{
            content: '';
            flex: 1;
            height: 1px;
            background: linear-gradient(to right, transparent, var(--border), transparent);
        }}

        .section-title {{
            font-family: 'Cormorant SC', serif;
            font-size: 1.4rem;
            font-weight: 600;
            color: var(--red-accent);
            letter-spacing: 0.12em;
            white-space: nowrap;
            text-transform: uppercase;
        }}

        .langue-badge {{
            display: inline-block;
            font-family: 'EB Garamond', serif;
            font-style: italic;
            font-size: 0.85rem;
            color: var(--ink-faded);
            background: var(--parchment);
            border: 1px solid var(--border-light);
            padding: 2px 12px;
            border-radius: 2px;
            margin-left: 8px;
        }}

        .count-badge {{
            font-family: 'Cormorant SC', serif;
            font-size: 0.75rem;
            font-weight: 300;
            color: var(--ink-faded);
            letter-spacing: 0.05em;
        }}

        /* Table */
        .table-container {{
            border: 1px solid var(--border);
            border-radius: 2px;
            overflow: hidden;
            box-shadow: 0 2px 16px var(--shadow), 0 1px 3px rgba(26,18,8,0.06);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--parchment);
        }}

        thead {{
            background: var(--ink);
        }}

        thead th {{
            font-family: 'Cormorant SC', serif;
            font-size: 0.72rem;
            font-weight: 500;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--parchment-dark);
            padding: 12px 18px;
            text-align: left;
        }}

        thead th:last-child {{
            color: rgba(245, 240, 232, 0.75);
        }}

        tbody tr {{
            border-bottom: 1px solid var(--border-light);
            transition: background 0.15s ease;
        }}

        tbody tr:last-child {{
            border-bottom: none;
        }}

        tbody tr:hover {{
            background: rgba(184, 134, 11, 0.06);
        }}

        tbody tr:nth-child(even) {{
            background: rgba(200, 184, 136, 0.08);
        }}

        tbody tr:nth-child(even):hover {{
            background: rgba(184, 134, 11, 0.08);
        }}

        td {{
            padding: 12px 18px;
            vertical-align: top;
            line-height: 1.45;
        }}

        td.auteur {{
            font-family: 'Cormorant SC', serif;
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--ink-light);
            letter-spacing: 0.02em;
            white-space: nowrap;
            width: 16%;
        }}

        td.oeuvre {{
            font-size: 0.92rem;
            color: var(--ink-light);
            width: 26%;
        }}

        td.oeuvre em {{
            font-style: italic;
        }}

        td.ref {{
            font-family: 'Cormorant SC', serif;
            font-size: 0.82rem;
            color: var(--red-accent);
            letter-spacing: 0.04em;
            white-space: nowrap;
            width: 12%;
            font-weight: 500;
        }}

        td.titre {{
            font-size: 0.9rem;
            color: var(--ink-faded);
            font-style: italic;
            width: 46%;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            margin-top: 64px;
            padding-top: 28px;
            border-top: 1px solid var(--border-light);
            font-size: 0.8rem;
            color: var(--ink-faded);
            font-style: italic;
            letter-spacing: 0.04em;
        }}

        /* Print */
        @media print {{
            body {{ background: white; }}
            .table-container {{ box-shadow: none; border: 1px solid #999; }}
        }}
    </style>
</head>
<body>
    <div class="page-wrapper">

        <header class="header">
            <h1>Sommaire des textes</h1>
            <p class="subtitle">Textes grecs et latins — classement par auteur, œuvre et référence</p>
        </header>

        <!-- Textes grecs -->
        <section class="section">
            <div class="section-header">
                <h2 class="section-title">Textes grecs <span class="count-badge">({len(grecs_sorted)} textes)</span></h2>
            </div>
            <div class="table-container">
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

        <div class="ornament">— ✦ —</div>

        <!-- Textes latins -->
        <section class="section">
            <div class="section-header">
                <h2 class="section-title">Textes latins <span class="count-badge">({len(latins_sorted)} textes)</span></h2>
            </div>
            <div class="table-container">
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

        <footer class="footer">
            Généré automatiquement à partir du corpus de textes
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
