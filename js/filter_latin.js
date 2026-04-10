const ANA_LABELS = {
    conjugaison: {
        indicatif_present:             "Indicatif présent",
        indicatif_imparfait:           "Indicatif imparfait",
        indicatif_parfait:             "Indicatif parfait",
        indicatif_plus_que_parfait:    "Indicatif plus-que-parfait",
        indicatif_futur:               "Indicatif futur",
        indicatif_futur_anterieur:     "Indicatif futur antérieur",

        subjonctif_present:            "Subjonctif présent",
        subjonctif_imparfait:          "Subjonctif imparfait",
        subjonctif_parfait:            "Subjonctif parfait",
        subjonctif_plus_que_parfait:   "Subjonctif plus-que-parfait",

        imperatif_present:             "Impératif présent",

        infinitif_present:             "Infinitif présent",
        infinitif_present_actif:       "Infinitif présent actif",
        infinitif_present_passif:      "Infinitif présent passif",
        infinitif_parfait:             "Infinitif parfait",
        infinitif_parfait_passif:      "Infinitif parfait passif",
        infinitif_futur:               "Infinitif futur",

        participe_present:             "Participe présent",
        participe_parfait:             "Participe parfait",
        participe_futur:               "Participe futur",
        participe_substantive:         "Participe substantivé",

        adjectif_verbal:               "Adjectif verbal",
        gerondif:                      "Gérondif",

        deponent:                      "Déponent"
    },

    morphologie: {
        comparatif:         "Comparatif",
        comparatif_adverbe: "Comparatif de l'adverbe",
        superlatif:         "Superlatif",

        ipse: "ipse, a, um",
        is:   "is, ea, id",
        ille: "ille, illa, illud",
        hic:  "hic, haec, hoc",
        idem: "idem, eadem, idem",

        qui:  "qui, quae, quod",
        quis: "quis, quae, quid"
    },

    syntaxe: {
        proposition_infinitive:                "Proposition infinitive",
        proposition_relative_indicatif:        "Proposition relative (indicatif)",
        proposition_relative_subjonctif:       "Proposition relative (subjonctif)",
        relatif_liaison:                       "Relatif de liaison",

        completive_ut_subjonctif:              "Complétive ut + subjonctif",
        completive_ne_subjonctif:              "Complétive ne + subjonctif",

        interrogative_directe:                 "Interrogative directe",
        interrogative_indirecte:               "Interrogative indirecte",
        exclamative:                           "Exclamative",

        discours_indirect:                     "Discours indirect",

        circonstancielle_temps_indicatif:      "Circonstancielle de temps (indicatif)",
        circonstancielle_causale_indicatif:    "Circonstancielle causale (indicatif)",
        circonstancielle_concessive_indicatif: "Circonstancielle concessive (indicatif)",
        circonstancielle_lieu_qua:             "Circonstancielle de lieu (qua)",
        circonstancielle_lieu_ubi:             "Circonstancielle de lieu (ubi)",

        circonstancielle_finale_subjonctif:       "Circonstancielle finale (subjonctif)",
        circonstancielle_consecutive_subjonctif:  "Circonstancielle consécutive (subjonctif)",
        circonstancielle_causale_subjonctif:      "Circonstancielle causale (subjonctif)",
        circonstancielle_concessive_subjonctif:   "Circonstancielle concessive (subjonctif)",

        comparative_indicatif:      "Comparative (indicatif)",
        complement_comparatif:      "Complément du comparatif",
        quo_comparatif_ut:          "quo + comparatif = ut",

        cum_indicatif:              "Cum + indicatif",
        cum_subjonctif:             "Cum + subjonctif",
        tum_cum:                    "tum … cum",
        quod_subjonctif:            "Quod + subjonctif",
        ut_indicatif:               "Ut + indicatif",

        passif_personnel_infinitif: "Passif personnel + infinitif",
        tournure_esse_datif:        "Tournure esse + datif",
        attribut_cod:               "Attribut du COD",
        accusatif_exclamatif:       "Accusatif exclamatif",
        ablatif_absolu:             "Ablatif absolu",
        omission_esse:              "Omission du verbe esse",

        adjectif_verbal_epithete:   "Adjectif verbal épithète",
        adjectif_verbal_attribut:   "Adjectif verbal attribut",

        subjonctif_principale:      "Subjonctif en principale",

        systeme_hypothetique_reel:            "Système hypothétique (réel)",
        systeme_hypothetique_eventuel:        "Système hypothétique (éventuel)",
        systeme_hypothetique_irreel_present:  "Système hypothétique (irréel du présent)",
        systeme_hypothetique_irreel_passe:    "Système hypothétique (irréel du passé)"
    },

    genre: {
        comedie:               "Comédie",
        didactique:            "Didactique",
        discours:              "Discours",
        elegie:                "Élégie",
        epigramme:             "Épigramme",
        epistolaire:           "Épistolaire",
        epopee:                "Épopée",
        fable:                 "Fable",
        histoire:              "Histoire",
        philosophie:           "Philosophie",
        roman:                 "Roman",
        satire:                "Satire",
        theatre:               "Théâtre",
        tragedie:              "Tragédie",
        litterature_technique: "Littérature technique",
        compilation:           "Compilation",
        lyrique:               "Lyrique",
        epyllion:              "Épyllion"
    },

    themes: {
        agriculture: "Agriculture",
        amitie:      "Amitié",
        amour:       "Amour",
        education:   "Éducation",
        eloge:       "Éloge",
        famille:     "Famille",
        guerre:      "Guerre",
        litterature: "Littérature",
        mort:        "Mort",
        nature:      "Nature",
        philosophie: "Philosophie",
        politique:   "Politique",
        religion:    "Religion",
        societe:     "Société",
        voyage:      "Voyage",
        argent:      "Argent"
    }
};

document.addEventListener("DOMContentLoaded", async () => {

    const compteur    = document.getElementById("compteur");
    const messageVide = document.getElementById("message-vide");
    const corpus      = document.getElementById("corpus");

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

        // Y a-t-il au moins un select .ana renseigné ?
        const anaActive = [...document.querySelectorAll("select.ana")].some(s => s.value);

        const filtresActifs = type || genre || niveau || anaActive;

        let count = 0;

        textes.forEach(texte => {
            let visible = true;

            if (!filtresActifs)                          visible = false;
            if (type  && texte.dataset.type   !== type)  visible = false;
            if (genre && texte.dataset.genre  !== genre) visible = false;
            if (niveau && texte.dataset.niveau !== niveau) visible = false;

            // Test de tous les selects .ana en séquence,
            // opérateurs appliqués entre eux sans distinction de catégorie
            if (anaActive && !testAnaGlobal(texte))      visible = false;

            texte.style.display = visible ? "block" : "none";
            if (visible) count++;
        });

        compteur.textContent = filtresActifs
            ? `${count} ${count > 1 ? "résultats trouvés" : "résultat trouvé"}`
            : "";

        messageVide.style.display =
            filtresActifs && count === 0 ? "block" : "none";
    }

    /* -------------------------------------------------------
       testAnaGlobal : parcourt TOUS les selects .ana du DOM
       dans l'ordre où ils apparaissent, et applique les
       opérateurs .op qui les séparent — toutes catégories
       confondues.

       Structure attendue dans le HTML (ordre dans le DOM) :
         [select.ana]  [select.op]  [select.ana]  [select.op]  [select.ana]
                        ↑ op entre 0 et 1          ↑ op entre 1 et 2

       Pour connaître la valeur d'un select .ana, on a besoin
       de savoir dans quel data-* du texte chercher.
       On utilise dataset[cat] où cat = select.dataset.cat.
    ------------------------------------------------------- */
    function testAnaGlobal(texte) {

        // Récupère tous les selects .ana dans l'ordre du DOM
        const selects = [...document.querySelectorAll("select.ana")];

        // Récupère tous les selects .op dans l'ordre du DOM
        // Il doit y avoir (selects.length - 1) opérateurs par bloc,
        // mais comme ils sont entremêlés on les récupère tous à plat.
        const ops = [...document.querySelectorAll("select.op")];

        // On construit une liste plate de tokens actifs :
        // [{ value, cat }, op, { value, cat }, op, { value, cat }, ...]
        // en ignorant les selects vides (on les saute ainsi que leur op associé)
        //
        // Stratégie : on itère sur les selects .ana dans l'ordre.
        // Entre le select i et le select i+1 se trouve ops[i] dans le DOM.
        // Si le select i est vide, on le saute (et son op suivant).

        let result = null;       // null = aucun token actif rencontré encore
        let pendingOp = null;    // opérateur à appliquer au prochain token actif

        let opIndex = 0;         // index courant dans ops[]

        for (let i = 0; i < selects.length; i++) {
            const sel = selects[i];
            const cat = sel.dataset.cat;

            // L'opérateur qui suit ce select dans le DOM
            // (undefined s'il n'y en a pas, c'est-à-dire pour le dernier select)
            const opAfter = ops[opIndex] || null;

            // Si ce select est vide, on avance l'index d'op et on continue
            if (!sel.value) {
                if (opAfter) opIndex++;
                continue;
            }

            // Le data-* dans lequel chercher (ex. dataset.conjugaison, dataset.themes…)
            const anaSet = (texte.dataset[cat] || "").split(/\s+/).filter(Boolean);
            const present = anaSet.includes(sel.value);

            if (result === null) {
                // Premier token actif : on initialise result
                result = (pendingOp === "without") ? !present : present;
            } else {
                // Tokens suivants : on applique l'opérateur en attente
                const op = pendingOp || "or";
                if      (op === "without") result = result && !present;
                else if (op === "and")     result = result && present;
                else                       result = result || present;
            }

            // L'opérateur qui suit ce select devient le pendingOp pour le prochain
            if (opAfter) {
                pendingOp = opAfter.value;
                opIndex++;
            }
        }

        // Si aucun select n'était renseigné, on laisse passer
        return result === null ? true : result;
    }

});
