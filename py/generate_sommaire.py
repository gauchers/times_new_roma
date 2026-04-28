import csv
import io
import os
import re
import sys
import unicodedata

BASE_URL = "https://gauchers.github.io/times_new_roma/data/"

def ref_sort_key(ref):
    """Sort references numerically, handling formats like '1.1', '3-6', '10.18', '1.47-74'"""
    parts = re.split(r'[-.]', ref)
    result = []
    for p in parts:
        try:
            result.append(int(p))
        except ValueError:
            result.append(0)
    return result if result else [0]

def slugify(text):
    """Normalize to lowercase ASCII, replacing spaces/dots/hyphens with underscores."""
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.lower()
    text = re.sub(r'[\s.\-,/]+', '_', text)
    text = re.sub(r'[^\w]', '', text)
    text = re.sub(r'_+', '_', text)
    return text.strip('_')

def langue_code(langue):
    l = langue.strip().lower()
    return 'grc' if l == 'grec' else 'la'

def build_url(langue, auteur, oeuvre, ref):
    code = langue_code(langue)
    filename = '_'.join([code, slugify(auteur), slugify(oeuvre), slugify(ref)]) + '.html'
    return BASE_URL + filename

def generate_html(rows):
    grecs  = [r for r in rows if r['Langue'].strip().lower() == 'grec']
    latins = [r for r in rows if r['Langue'].strip().lower() == 'latin']

    def sort_key(r):
        return (r['Auteur'].strip().lower(), r['Oeuvre'].strip().lower(), ref_sort_key(r['Référence'].strip()))

    grecs_sorted  = sorted(grecs,  key=sort_key)
    latins_sorted = sorted(latins, key=sort_key)

    def build_table(items):
        rows_html = ""
        for r in items:
            auteur = r['Auteur'].strip()
            oeuvre = r['Oeuvre'].strip()
            ref    = r['Référence'].strip()
            titre  = r['Titre du texte'].strip()
            url    = build_url(r['Langue'], auteur, oeuvre, ref)
            rows_html += f"""
            <tr>
                <td class="auteur">{auteur}</td>
                <td class="oeuvre"><em>{oeuvre}</em></td>
                <td class="ref">{ref}</td>
                <td class="titre"><a href="{url}">{titre}</a></td>
            </tr>"""
        return rows_html

    grecs_rows  = build_table(grecs_sorted)
    latins_rows = build_table(latins_sorted)

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Textes référencés – Times New Roma</title>
    <link rel="stylesheet" href="../css/style_sommaire.css">
</head>
<body>
    <hr class="top-rule">
    <nav>
        <a href="../index.html" class="nav-btn accueil">← Accueil</a>
    </nav>

    <!-- Barre de recherche latérale -->
    <aside class="search-panel" id="searchPanel">
        <div class="search-panel-inner">
            <label class="search-label" for="searchInput">Recherche</label>
            <input type="text" id="searchInput" class="search-input" placeholder="Auteur, œuvre, titre…" autocomplete="off">
            <div class="search-results" id="searchResults"></div>
            <p class="search-hint" id="searchHint">Saisissez au moins 2 caractères</p>
        </div>
    </aside>

    <div class="page-wrapper">

        <header class="som-header">
            <h1>Times New Roma</h1>
            <p class="subtitle">Textes grecs et latins référencés — classement par auteur, œuvre et référence</p>
        <div class="ornament"><span>✦</span></div>
        </header>

        <!-- Textes grecs -->
        <section class="som-section">
            <div class="som-section-header grec">
                <button class="toggle-btn" aria-expanded="true" aria-controls="table-grec" data-target="table-grec">
                    <span class="toggle-icon">▸</span>
                    <span class="som-section-title grec">Textes grecs</span>
                    <span class="count-badge">({len(grecs_sorted)} textes)</span>
                </button>
            </div>
            <div class="table-container grec grec-table" id="table-grec">
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
            <div class="som-section-header latin">
                <button class="toggle-btn" aria-expanded="true" aria-controls="table-latin" data-target="table-latin">
                    <span class="toggle-icon">▸</span>
                    <span class="som-section-title latin">Textes latins</span>
                    <span class="count-badge">({len(latins_sorted)} textes)</span>
                </button>
            </div>
            <div class="table-container latin latin-table" id="table-latin">
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

    <script>
    // ── Toggle rétractable ──────────────────────────────────────────
    document.querySelectorAll('.toggle-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
            const targetId = btn.dataset.target;
            const target = document.getElementById(targetId);
            const icon = btn.querySelector('.toggle-icon');
            const expanded = btn.getAttribute('aria-expanded') === 'true';

            btn.setAttribute('aria-expanded', !expanded);
            target.classList.toggle('collapsed', expanded);
            icon.style.transform = expanded ? '' : 'rotate(90deg)';
        }});
    }});

    // ── Recherche plein texte ───────────────────────────────────────
    const allRows = Array.from(document.querySelectorAll('tbody tr')).map(tr => ({{
        el: tr,
        text: tr.innerText.toLowerCase(),
        auteur: tr.querySelector('.auteur')?.innerText || '',
        oeuvre: tr.querySelector('.oeuvre')?.innerText || '',
        ref:    tr.querySelector('.ref')?.innerText || '',
        titre:  tr.querySelector('.titre')?.innerText || '',
        url:    tr.querySelector('.titre a')?.href || '',
        langue: tr.closest('.grec-table') ? 'grec' : 'latin'
    }}));

    const input   = document.getElementById('searchInput');
    const results = document.getElementById('searchResults');
    const hint    = document.getElementById('searchHint');

    input.addEventListener('input', () => {{
        const q = input.value.trim().toLowerCase();
        results.innerHTML = '';
        hint.style.display = 'none';

        if (q.length < 2) {{
            hint.style.display = 'block';
            return;
        }}

        const matches = allRows.filter(r => r.text.includes(q));

        if (matches.length === 0) {{
            results.innerHTML = '<p class="no-result">Aucun résultat</p>';
            return;
        }}

        matches.forEach(r => {{
            const item = document.createElement('div');
            item.className = 'result-item ' + r.langue;
            item.innerHTML = `
                <span class="res-auteur">${{r.auteur}}</span>
                <span class="res-oeuvre">${{r.oeuvre}}</span>
                <span class="res-ref">${{r.ref}}</span>
                <span class="res-titre">${{r.titre}}</span>`;
            item.addEventListener('click', () => {{
                if (r.url) {{
                    window.location.href = r.url;
                }} else {{
                    // Fallback : scroll vers la ligne
                    const tableId = r.langue === 'grec' ? 'table-grec' : 'table-latin';
                    const tableEl = document.getElementById(tableId);
                    const btn = document.querySelector(`[data-target="${{tableId}}"]`);
                    if (tableEl.classList.contains('collapsed')) {{
                        tableEl.classList.remove('collapsed');
                        btn.setAttribute('aria-expanded', 'true');
                        btn.querySelector('.toggle-icon').style.transform = 'rotate(90deg)';
                    }}
                    document.querySelectorAll('tr.highlighted').forEach(el => el.classList.remove('highlighted'));
                    r.el.classList.add('highlighted');
                    r.el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                }}
            }});
            results.appendChild(item);
        }});
    }});
    </script>
</body>
</html>"""

    return html


def main():
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
