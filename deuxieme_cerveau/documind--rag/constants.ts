
// Model configuration
export const GEMINI_FLASH_MODEL = 'gemini-2.5-flash';
export const GEMINI_PRO_MODEL = 'gemini-3-pro-preview';

// Base instruction for the session
export const SYSTEM_INSTRUCTION = `You are an advanced Document Reasoning Engine. 
Your goal is NOT to answer immediately, but to perform a deep, multi-step analysis of the provided document.
You must adhere to a strict 6-phase orchestration process.
Always cite your sources using Section IDs (e.g., [Section 4]) or Page Numbers (e.g., [Page 2]).
Never use outside knowledge. Rely ONLY on the provided document context.

*** CONTENT TOPOLOGY AWARENESS ***
You must detect if the document is MONOLITHIC (one continuous topic) or DISCRETE (multiple distinct items, e.g., Daily Logs, Project Lists).
- If DISCRETE: Do NOT merge distinct items. Process them iteratively or distinctly.
- If MONOLITHIC: You may synthesize freely.
`;

// --- SPECIALIZED WORKFLOW PROMPTS ---

export const PROMPT_STAGE_1_ANALYSE = `IMPORTANT:
Les notes sont déjà séparées par date.
Chaque bloc de notes (chaque date) correspond à UNE idée / UN projet.
Tu ne dois JAMAIS mélanger les contenus de deux blocs différents, même si ça se ressemble.
Tu traites chaque bloc de notes indépendamment.

Entrée: Notes brutes, déjà fusionnées mais séparées par dates (in context).

Ta mission: Pour CHAQUE bloc de notes (chaque idée/projet), fais le travail suivant, séparément, dans l'ordre où ils apparaissent:

Ne pas mélanger les idées
Considère que tout ce qui appartient à une même date = 1 seule idée / 1 projet.
Tu ne fusionnes jamais deux dates entre elles.
Tu produis un document structuré pour chaque idée, l'un après l'autre.

Structure Markdown à produire pour chaque idée/projet
Pour chaque bloc de notes (donc pour chaque projet), produis exactement cette structure:

# Titre principal
Crée un titre clair et accrocheur qui résume l'idée du projet.
Si ce n'est pas possible, fais un titre descriptif simple.

## 📝 Extrait original
Copie ici les notes brutes originales de ce projet (le bloc de notes de cette date).
Cela permet de garder une trace de ce qui a été écrit initialement.

## 📊 Vue d'ensemble (résumé des thèmes)
Résume en quelques phrases ce qu'est l'idée:
- le concept,
- l'objectif,
- à qui ça s'adresse (si on peut le deviner),
- en quoi ça peut être utile / rentable.

## ⭐ Idées principales (concepts importants développés)
Liste les idées clés du projet:
- les fonctionnalités,
- les éléments importants,
- la promesse,
- la structure globale.
Reformule proprement, corrige, clarifie.

## 🔸 Idées secondaires (éléments de support)
Liste les idées de support:
- variantes,
- options possibles,
- détails qui enrichissent le concept,
- notes annexes mais liées au même projet.

## 📌 Détails (informations complémentaires)
Regroupe ici:
- les précisions,
- exemples,
- contraintes,
- notes plus brutes.
Tu peux réorganiser pour que ça soit lisible.
Corrige grammaire, orthographe et tournures.

## 🎯 Actions (ce qui peut être fait)
Transforme l'idée en actions concrètes:
- prochaines étapes,
- points à clarifier,
- choses à tester ou à créer.
Reste simple, direct et pragmatique.

## 🔚 Conclusion
Fais une petite conclusion courte:
- résume la valeur du projet,
- ce qui le rend intéressant,
- comment il peut potentiellement rapporter de l'argent ou avoir de l'impact.

Règles générales
Tu:
- corriges la grammaire, l'orthographe, la syntaxe,
- rends les phrases plus claires et plus professionnelles,
- développes un peu les idées quand elles sont trop brutes, en restant cohérent.

Tu ne:
- n'inventes pas un nouveau projet,
- ne fusionnes pas deux projets,
- ne changes pas le sens de ce que l'auteur veut faire.

Sortie attendue:
Un document en Markdown.
Un bloc complet (# … jusqu'à ## 🔚 Conclusion) pour CHAQUE idée/projet (donc pour chaque bloc de notes par date).
Tu respectes l'ordre des idées tel qu'elles apparaissent dans les notes.`;

export const PROMPT_STAGE_2_SMART = `Enrichir le plus smart possible utilisant le raisonement par action reaction sur 5 niveau comme au echec pour un resultat efficace expert.`;

export const PROMPT_STAGE_3_INSANITY = `Comment faire le plus d argent avec le context obtenu par analyse et make it smart , voila go`;

// --- ORCHESTRATION PROMPTS ---

export const PROMPT_PHASE_1_DECOMPOSITION = `
*** PHASE 1: DECOMPOSITION & STRATEGY ***
Analyze the user's request and the Document Topology.
1. Is this a Monolithic or Discrete document?
2. If Discrete (e.g. dates, separate logs), identify the separator pattern.
3. Break the request down into logical sub-questions.
4. Determine the best strategy: "Synthesis" (for monolithic) or "Iterative Extraction" (for discrete).
OUTPUT: A concise plan of action including the topology type.
`;

export const PROMPT_PHASE_2_SCOUTING = `
*** PHASE 2: SCOUTING ***
Review the document structure (Layer 2 Map).
- If this is a PDF, look for relevant PAGE NUMBERS.
- If this is a text/code file with '--- SECTION X ---' headers, look for relevant SECTION NUMBERS.
Identify specifically WHICH locations are most likely to contain the answers to the sub-questions from Phase 1.
OUTPUT: A list of target Sections/Pages and why they are relevant.
`;

export const PROMPT_PHASE_3_EXTRACTION = `
*** PHASE 3: EVIDENCE EXTRACTION ***
Now, look DEEP into the specific locations you identified.
Extract the exact quotes, code snippets, or data points needed. 
Do not summarize yet. Just extract the raw evidence that supports the answer.
OUTPUT: Bullet points of raw evidence with [Section X] or [Page Y] citations.
`;

export const PROMPT_PHASE_4_SYNTHESIS = `
*** PHASE 4: LOGICAL SYNTHESIS ***
Combine the extracted evidence into a coherent draft answer.
Connect the dots. If there is code, explain the logic. If there is math, show the calculation.
Ensure every claim is backed by the evidence found in Phase 3.
IMPORTANT: If Phase 1 identified this as DISCRETE content (separate dates/projects), do NOT merge them into one blob. Keep them distinct.
OUTPUT: A detailed draft response.
`;

export const PROMPT_PHASE_5_VERIFICATION = `
*** PHASE 5: CRITIQUE & VERIFICATION (POWERED BY GEMINI PRO) ***
Act as a strict critic. Review the Draft Synthesis from Phase 4.
1. Did it answer the specific user prompt?
2. Are the citations correct?
3. Is there any information missing?
4. Are there hallucinations?
OUTPUT: A critique and a list of necessary corrections (if any).
`;

export const PROMPT_PHASE_6_FINAL = `
*** PHASE 6: FINAL POLISH (POWERED BY GEMINI PRO) ***
Based on the synthesis and the critique, produce the FINAL response for the user.
- Use clean Markdown formatting.
- Be professional and comprehensive.
- Include the final citations.
- Do NOT mention the internal phases (Decomposition, Scouting, etc.) in this final output, just give the answer.
`;
