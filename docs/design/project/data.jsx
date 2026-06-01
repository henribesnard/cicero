/* ============================================================
   CICERO — data.jsx
   Monument records, travel log, offline cities, canned chat.
   Facts are real & kept concise. Exported to window.
   ============================================================ */

const MONUMENTS = {
  eiffel: {
    id: 'eiffel',
    name: 'Tour Eiffel',
    place: 'Champ de Mars, Paris',
    country: 'France',
    type: 'Tour · Fer puddlé',
    tone: 'dawn', monument: 'tower',
    score: 98,
    blurb: "Érigée pour l'Exposition universelle de 1889, la « Dame de fer » devait être démontée au bout de 20 ans. Elle est devenue l'emblème de Paris.",
    stats: [
      { icon: 'calendar', label: 'Achèvement', value: '1889' },
      { icon: 'ruler', label: 'Hauteur', value: '330', unit: 'm' },
      { icon: 'person', label: 'Ingénieur', value: 'G. Eiffel' },
      { icon: 'layers', label: 'Étages', value: '3' },
    ],
    suggested: [
      'Pourquoi a-t-elle failli être détruite ?',
      'Combien pèse la structure ?',
      'Que se passe-t-il au sommet ?',
    ],
    chat: {
      'Pourquoi a-t-elle failli être détruite ?':
        "Le permis n'autorisait la tour que pour 20 ans, le temps de l'Exposition de 1889. Beaucoup d'artistes la jugeaient laide. Elle a été sauvée par son utilité : une immense antenne pour la télégraphie militaire, puis la radio.",
      'Combien pèse la structure ?':
        "La charpente de fer pèse environ 7 300 tonnes, et l'ensemble près de 10 100 tonnes. Malgré cela, la pression au sol équivaut à celle d'une personne assise sur une chaise.",
      'Que se passe-t-il au sommet ?':
        "À 276 m se trouve le 3ᵉ étage, avec le bureau reconstitué de Gustave Eiffel. Par temps clair, on voit jusqu'à 70 km. La tour grandit d'environ 15 cm l'été, le fer se dilatant à la chaleur.",
    },
  },
  sacrecoeur: {
    id: 'sacrecoeur',
    name: 'Basilique du Sacré-Cœur',
    place: 'Butte Montmartre, Paris',
    country: 'France',
    type: 'Basilique · Style romano-byzantin',
    tone: 'day', monument: 'dome',
    score: 94,
    blurb: "Perchée au sommet de Montmartre, sa pierre de travertin blanchit avec la pluie. Sa construction s'étala de 1875 à 1914.",
    stats: [
      { icon: 'calendar', label: 'Achèvement', value: '1914' },
      { icon: 'ruler', label: 'Hauteur', value: '83', unit: 'm' },
      { icon: 'person', label: 'Architecte', value: 'P. Abadie' },
      { icon: 'layers', label: 'Altitude', value: '130', unit: 'm' },
    ],
    suggested: [
      'Pourquoi la pierre reste-t-elle si blanche ?',
      'Que voit-on depuis le parvis ?',
      'Quelle est cette grande cloche ?',
    ],
    chat: {
      'Pourquoi la pierre reste-t-elle si blanche ?':
        "Elle est bâtie en travertin de Château-Landon. Au contact de l'eau de pluie, cette pierre sécrète du calcin, un dépôt blanc qui la nettoie naturellement et la garde immaculée.",
    },
  },
  // Uncertain-state demo subject
  saintdenis: {
    id: 'saintdenis',
    name: 'Basilique Saint-Denis',
    place: 'Saint-Denis, Île-de-France',
    country: 'France',
    type: 'Basilique · Art gothique',
    tone: 'dusk', monument: 'dome',
    score: 71,
    blurb: "Berceau de l'art gothique et nécropole des rois de France. La vue partielle réduit la certitude de l'identification.",
    stats: [
      { icon: 'calendar', label: 'Consécration', value: '1144' },
      { icon: 'ruler', label: 'Flèche (disparue)', value: '90', unit: 'm' },
      { icon: 'person', label: 'Initiateur', value: 'Abbé Suger' },
      { icon: 'history', label: 'Rois inhumés', value: '43' },
    ],
    suggested: [
      "Pourquoi l'identification est-elle incertaine ?",
      'En quoi est-ce le berceau du gothique ?',
    ],
    chat: {
      "Pourquoi l'identification est-elle incertaine ?":
        "La façade est vue de biais et partiellement masquée. Deux édifices gothiques d'Île-de-France présentent un portail proche. Rapprochez-vous ou cadrez la rosace pour confirmer.",
    },
  },
};

// Alternative guesses shown in the "uncertain" state
const UNCERTAIN_ALTS = [
  { name: 'Basilique Saint-Denis', score: 71 },
  { name: 'Cathédrale de Senlis', score: 19 },
];

const TRAVEL_LOG = [
  { id: 'eiffel', name: 'Tour Eiffel', place: 'Paris', date: "Aujourd'hui · 09:41", tone: 'dawn', monument: 'tower', score: 98, fav: true },
  { id: 'sacrecoeur', name: 'Basilique du Sacré-Cœur', place: 'Paris', date: 'Hier · 17:20', tone: 'day', monument: 'dome', score: 94, fav: false },
  { id: 'arc', name: 'Arc de Triomphe', place: 'Paris', date: '30 mai · 14:05', tone: 'day', monument: 'arch', score: 96, fav: true },
  { id: 'colonne', name: 'Colonne de Juillet', place: 'Bastille, Paris', date: '29 mai · 11:32', tone: 'dusk', monument: 'statue', score: 88, fav: false },
];

const OFFLINE_CITIES = [
  { id: 'paris', name: 'Paris', country: 'France', count: 540, size: '210 Mo', state: 'downloaded' },
  { id: 'rome', name: 'Rome', country: 'Italie', count: 480, size: '198 Mo', state: 'downloading', progress: 64 },
  { id: 'athenes', name: 'Athènes', country: 'Grèce', count: 220, size: '95 Mo', state: 'available' },
  { id: 'istanbul', name: 'Istanbul', country: 'Turquie', count: 310, size: '142 Mo', state: 'available' },
  { id: 'kyoto', name: 'Kyoto', country: 'Japon', count: 260, size: '120 Mo', state: 'available' },
];

const LANGUAGES = ['Français', 'English', 'Español', 'Deutsch', '日本語', 'العربية'];

window.CIC_DATA = { MONUMENTS, UNCERTAIN_ALTS, TRAVEL_LOG, OFFLINE_CITIES, LANGUAGES };
