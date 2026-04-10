const ANA_LABELS = {
    conjugaison: {
        indicatif_present: "Indicatif présent",
        indicatif_imparfait: "Indicatif imparfait",
        indicatif_parfait: "Indicatif parfait",
        indicatif_plus_que_parfait: "Indicatif plus-que-parfait",
        indicatif_futur: "Indicatif futur",
        indicatif_futur_anterieur: "Indicatif futur antérieur",

        subjonctif_present: "Subjonctif présent",
        subjonctif_imparfait: "Subjonctif imparfait",
        subjonctif_parfait: "Subjonctif parfait",
        subjonctif_plus_que_parfait: "Subjonctif plus-que-parfait",

        imperatif_present: "Impératif présent",

        infinitif_present: "Infinitif présent",
        infinitif_present_actif: "Infinitif présent actif",
        infinitif_present_passif: "Infinitif présent passif",
        infinitif_parfait: "Infinitif parfait",
        infinitif_parfait_passif: "Infinitif parfait passif",
        infinitif_futur: "Infinitif futur",

        participe_present: "Participe présent",
        participe_parfait: "Participe parfait",
        participe_futur: "Participe futur",
        participe_substantive: "Participe substantivé",

        adjectif_verbal: "Adjectif verbal",
        gerondif: "Gérondif",

        deponent: "Déponent"
    },

    morphologie: {
        comparatif: "Comparatif",
        comparatif_adverbe: "Comparatif de l'adverbe",
        superlatif: "Superlatif",

        ipse: "ipse, a, um",
        is: "is, ea, id",
        ille: "ille, illa, illud",
        hic: "hic, haec, hoc",
        idem: "idem, eadem, idem",

        qui: "qui, quae, quod",
        quis: "quis, quae, quid"
    },

    syntaxe: {
        proposition_infinitive: "Proposition infinitive",
        proposition_relative_indicatif: "Proposition relative (indicatif)",
        proposition_relative_subjonctif: "Proposition relative (subjonctif)",
        relatif_liaison: "Relatif de liaison",

        completive_ut_subjonctif: "Complétive ut + subjonctif",
        completive_ne_subjonctif: "Complétive ne + subjonctif",

        interrogative_directe: "Interrogative directe",
        interrogative_indirecte: "Interrogative indirecte",
        exclamative: "Exclamative",

        discours_indirect: "Discours indirect",

        circonstancielle_temps_indicatif: "Circonstancielle de temps (indicatif)",
        circonstancielle_causale_indicatif: "Circonstancielle causale (indicatif)",
        circonstancielle_concessive_indicatif: "Circonstancielle concessive (indicatif)",
        circonstancielle_lieu_qua: "Circonstancielle de lieu (qua)",
        circonstancielle_lieu_ubi: "Circonstancielle de lieu (ubi)",

        circonstancielle_finale_subjonctif: "Circonstancielle finale (subjonctif)",
        circonstancielle_consecutive_subjonctif: "Circonstancielle consécutive (subjonctif)",
        circonstancielle_causale_subjonctif: "Circonstancielle causale (subjonctif)",
        circonstancielle_concessive_subjonctif: "Circonstancielle concessive (subjonctif)",

        comparative_indicatif: "Comparative (indicatif)",
        complement_comparatif: "Complément du comparatif",
        quo_comparatif_ut: "quo + comparatif = ut",

        cum_indicatif: "Cum + indicatif",
        cum_subjonctif: "Cum + subjonctif",
        tum_cum: "tum … cum",
        quod_subjonctif: "Quod + subjonctif",
        ut_indicatif: "Ut + indicatif",

        passif_personnel_infinitif: "Passif personnel + infinitif",
        tournure_esse_datif: "Tournure esse + datif",
        attribut_cod: "Attribut du COD",
        accusatif_exclamatif: "Accusatif exclamatif",
        ablatif_absolu: "Ablatif absolu",
        omission_esse: "Omission du verbe esse",

        adjectif_verbal_epithete: "Adjectif verbal épithète",
        adjectif_verbal_attribut: "Adjectif verbal attribut",

        subjonctif_principale: "Subjonctif en principale",

        systeme_hypothetique_reel: "Système hypothétique (réel)",
        systeme_hypothetique_eventuel: "Système hypothétique (éventuel)",
        systeme_hypothetique_irreel_present: "Système hypothétique (irréel du présent)",
        systeme_hypothetique_irreel_passe: "Système hypothétique (irréel du passé)"
    },

    theme: {
    agriculture: "Agriculture et vie rustique",
    amitie: "Amitié",
    amour: "Amour et érotisme",
    argent: "Argent et commerce",
    education: "Éducation et pédagogie",
    eloge: "Éloge et blâme",
    famille: "Famille et ancêtres",
    guerre: "Guerre",
    litterature: "Langue et littérature",
    mort: "Mort",
    nature: "Nature et animaux",
    philosophie: "Philosophie et morale",
    politique: "Politique et pouvoir",
    religion: "Religion et mythologie",
    societe: "Société",
    voyage: "Voyage et exil"
    }
};

document.addEventListener("DOMContentLoaded", async () => {
 
    const compteur     = document.getElementById("compteur");
    const messageVide  = document.getElementById("message-vide");
    const corpus       = document.getElementById("corpus");
 
    let textes = [];
 
    /* =========================
       1. Chargement des fichiers
       ========================= */
 
    const files = await fetch("../data/index.json")
        .then(r => {
            if (!r.ok) throw new Error("index.json introuvable");
            return r.json();
        })
        .catch(e => {
            console.error(e);
            return [];
        });
 
    for (const file of files.filter(f => f.startsWith("la_"))) {
        const html = await fetch(`../data/${file}`)
            .then(r => r.ok ? r.text() : null);
 
        if (!html) continue;
 
        const temp = document.createElement("div");
        temp.innerHTML = html;
 
        const texte = temp.querySelector(".texte");
        if (!texte) continue;
 
        texte.style.display = "none";
        corpus.appendChild(texte);
        textes.push(texte);
    }
 
    /* =========================
       2. Menus déroulants .ana
       ========================= */
 
    // Remplit tous les <select class="ana"> à partir d'ANA_LABELS
    document.querySelectorAll("select.ana").forEach(select => {
        const cat = select.dataset.cat;
        if (!ANA_LABELS[cat]) return;
        select.innerHTML = `<option value="">—</option>`;
        Object.entries(ANA_LABELS[cat]).forEach(([value, label]) => {
            const opt = document.createElement("option");
            opt.value = value;
            opt.textContent = label;
            select.appendChild(opt);
        });
    });
 
    /* =========================
       3. Écouteurs
       ========================= */
 
    document.querySelectorAll("select")
        .forEach(s => s.addEventListener("change", appliquerFiltres));
 
    /* =========================
       4. Filtres
       ========================= */
 
    function appliquerFiltres() {
        const type   = document.getElementById("type").value;
        const genre  = document.getElementById("genre").value;
        const niveau = document.getElementById("niveau").value;
 
        const filtresActifs =
            type || genre || niveau ||
            hasAnaSelection("conjugaison") ||
            hasAnaSelection("morphologie") ||
            hasAnaSelection("syntaxe")     ||
            hasAnaSelection("themes");
 
        let count = 0;
 
        textes.forEach(texte => {
            let visible = true;
 
            // Sans aucun filtre, on n'affiche rien
            if (!filtresActifs) visible = false;
 
            // Filtre type (prose / poésie)
            if (type && texte.dataset.type !== type) visible = false;
 
            // Filtre genre : comparaison exacte sur data-genre
            // data-genre contient une seule valeur (ex. "histoire")
            if (genre && texte.dataset.genre !== genre) visible = false;
 
            // Filtre niveau
            if (niveau && texte.dataset.niveau !== niveau) visible = false;
 
            // Filtres .ana avec opérateurs ET / OU / SANS
            if (!testAnaCat("conjugaison", texte)) visible = false;
            if (!testAnaCat("morphologie", texte)) visible = false;
            if (!testAnaCat("syntaxe",     texte)) visible = false;
            if (!testAnaCat("themes",      texte)) visible = false;
 
            texte.style.display = visible ? "block" : "none";
            if (visible) count++;
        });
 
        compteur.textContent = filtresActifs
            ? `${count} ${count > 1 ? "résultats trouvés" : "résultat trouvé"}`
            : "";
 
        messageVide.style.display =
            filtresActifs && count === 0 ? "block" : "none";
    }
 
    function hasAnaSelection(cat) {
        return [...document.querySelectorAll(`.ana[data-cat="${cat}"]`)]
            .some(s => s.value);
    }
 
    function testAnaCat(cat, texte) {
        const selects = [...document.querySelectorAll(`.ana[data-cat="${cat}"]`)];
        const ops     = [...document.querySelectorAll(`.op[data-cat="${cat}"]`)];
 
        // data-themes contient "agriculture amour nature" (espace séparé)
        const anaSet  = (texte.dataset[cat] || "").split(/\s+/).filter(Boolean);
 
        let result = null;
 
        for (let i = 0; i < selects.length; i++) {
            const value = selects[i].value;
            if (!value) continue;
 
            const present = anaSet.includes(value);
            const op = i > 0 ? ops[i - 1].value : "or";
 
            if (result === null) {
                result = (op === "without") ? !present : present;
            } else {
                if (op === "without") result = result && !present;
                else if (op === "and") result = result && present;
                else                  result = result || present;
            }
        }
 
        return result === null ? true : result;
    }
 
});
