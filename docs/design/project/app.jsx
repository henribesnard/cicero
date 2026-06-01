/* ============================================================
   CICERO — app.jsx
   Static phone shell + the full DesignCanvas document.
   ============================================================ */

// Lightweight phone shell for static screen boards (no heavy bezel)
function StatusBar({ camera }) {
  const c = camera ? 'rgba(255,255,255,0.96)' : 'var(--ink)';
  return (
    <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 50, zIndex: 40, pointerEvents: 'none',
      display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 26px' }}>
      <span className="cic-ui tnum" style={{ fontSize: 15.5, fontWeight: 700, color: c, marginTop: 6 }}>9:41</span>
      <div style={{ display: 'flex', gap: 6, alignItems: 'center', marginTop: 6 }}>
        <svg width="18" height="12" viewBox="0 0 19 12"><rect x="0" y="7.5" width="3.2" height="4.5" rx="0.7" fill={c}/><rect x="4.8" y="5" width="3.2" height="7" rx="0.7" fill={c}/><rect x="9.6" y="2.5" width="3.2" height="9.5" rx="0.7" fill={c}/><rect x="14.4" y="0" width="3.2" height="12" rx="0.7" fill={c}/></svg>
        <svg width="24" height="12" viewBox="0 0 27 13"><rect x="0.5" y="0.5" width="23" height="12" rx="3.5" stroke={c} strokeOpacity="0.4" fill="none"/><rect x="2" y="2" width="18" height="9" rx="2" fill={c}/><path d="M25 4.5V8.5C25.8 8.2 26.5 7.2 26.5 6.5C26.5 5.8 25.8 4.8 25 4.5Z" fill={c} fillOpacity="0.5"/></svg>
      </div>
    </div>
  );
}
function StaticPhone({ theme = 'light', camera = false, children, w = 384, h = 812 }) {
  return (
    <div data-theme={theme} style={{ width: w, height: h, position: 'relative', overflow: 'hidden',
      background: 'var(--bg)', borderRadius: 0 }}>
      {/* dynamic island */}
      <div style={{ position: 'absolute', top: 11, left: '50%', transform: 'translateX(-50%)', width: 118, height: 34,
        borderRadius: 20, background: '#000', zIndex: 45 }} />
      <StatusBar camera={camera} />
      <div style={{ position: 'absolute', inset: 0 }}>{children}</div>
      {/* home indicator */}
      <div style={{ position: 'absolute', bottom: 8, left: '50%', transform: 'translateX(-50%)', width: 134, height: 5,
        borderRadius: 99, background: camera ? 'rgba(255,255,255,0.7)' : 'var(--ink-faint)', zIndex: 45 }} />
    </div>
  );
}

const SAMPLE_CHAT = [
  { role: 'user', text: 'Pourquoi a-t-elle failli être détruite ?' },
  { role: 'assistant', verified: true, sources: '3 sources',
    text: "Le permis n'autorisait la tour que pour 20 ans, le temps de l'Exposition de 1889. Elle fut sauvée par son utilité : une immense antenne pour la radio et l'armée." },
  { role: 'user', text: 'Et combien pèse-t-elle ?' },
  { role: 'assistant', verified: true, sources: '2 sources',
    text: "Environ 10 100 tonnes au total, dont 7 300 de fer. La pression au sol équivaut pourtant à celle d'une personne assise sur une chaise." },
];

function ScreenBoard({ theme }) {
  const cam = theme; // pass-through
  const D = window.CIC_DATA;
  const phones = [
    { id: 'ob0', label: 'Onboarding · Accueil', camera: true, el: <OnboardingScreen step={0} /> },
    { id: 'ob1', label: 'Onboarding · Caméra', camera: false, el: <OnboardingScreen step={1} /> },
    { id: 'ob2', label: 'Onboarding · Position', camera: false, el: <OnboardingScreen step={2} /> },
    { id: 'scan-s', label: 'Scanner · Recherche', camera: true, el: <ScannerScreen mode="searching" data={D.MONUMENTS.eiffel} /> },
    { id: 'scan-r', label: 'Scanner · Reconnu', camera: true, el: <ScannerScreen mode="recognized" data={D.MONUMENTS.eiffel} /> },
    { id: 'scan-u', label: 'Scanner · Incertain', camera: true, el: <ScannerScreen mode="uncertain" data={D.MONUMENTS.saintdenis} /> },
    { id: 'sheet', label: 'Fiche monument', camera: true, el: <MonumentSheet data={D.MONUMENTS.eiffel} embedded /> },
    { id: 'chat', label: 'Assistant IA', camera: false, el: <ChatScreen data={D.MONUMENTS.eiffel} messages={SAMPLE_CHAT} /> },
    { id: 'carnet', label: 'Carnet de voyage', camera: false, el: <TravelLogScreen /> },
    { id: 'offline', label: 'Hors-ligne', camera: false, el: <OfflineScreen /> },
    { id: 'settings', label: 'Réglages', camera: false, el: <SettingsScreen theme={theme} /> },
  ];
  return phones.map(p => (
    <DCArtboard key={p.id} id={`${theme}-${p.id}`} label={p.label} width={384} height={812} style={{ background: '#000' }}>
      <StaticPhone theme={theme} camera={p.camera}>{p.el}</StaticPhone>
    </DCArtboard>
  ));
}

function DarkScreenBoard() {
  const D = window.CIC_DATA;
  const phones = [
    { id: 'd-scan', label: 'Scanner · Reconnu', camera: true, el: <ScannerScreen mode="recognized" data={D.MONUMENTS.eiffel} /> },
    { id: 'd-sheet', label: 'Fiche monument', camera: true, el: <MonumentSheet data={D.MONUMENTS.sacrecoeur} embedded /> },
    { id: 'd-chat', label: 'Assistant IA', camera: false, el: <ChatScreen data={D.MONUMENTS.eiffel} messages={SAMPLE_CHAT} /> },
    { id: 'd-carnet', label: 'Carnet de voyage', camera: false, el: <TravelLogScreen /> },
    { id: 'd-settings', label: 'Réglages', camera: false, el: <SettingsScreen theme="dark" /> },
  ];
  return phones.map(p => (
    <DCArtboard key={p.id} id={p.id} label={p.label} width={384} height={812} style={{ background: '#000' }}>
      <StaticPhone theme="dark" camera={p.camera}>{p.el}</StaticPhone>
    </DCArtboard>
  ));
}

function CiceroDoc() {
  return (
    <DesignCanvas>
      <DCSection id="direction" title="01 · Direction visuelle" subtitle="L'app caméra-d'abord qui se prend pour un cicérone">
        <DCArtboard id="manifesto" label="Manifeste" width={860} height={712} style={{ background: '#F4F0E8' }}>
          <DirectionManifesto />
        </DCArtboard>
        <DCArtboard id="palette" label="Palette · Sarcelle & pierre" width={860} height={776} style={{ background: '#F4F0E8' }}>
          <PalettePlanche />
        </DCArtboard>
        <DCArtboard id="type" label="Typographie" width={860} height={414} style={{ background: '#F4F0E8' }}>
          <TypePlanche />
        </DCArtboard>
      </DCSection>

      <DCSection id="composants" title="02 · Bibliothèque de composants" subtitle="Pastille, confiance, tuiles, bulles de chat, contrôles">
        <DCArtboard id="components" label="Composants" width={900} height={1252} style={{ background: '#F4F0E8' }}>
          <ComponentsPlanche />
        </DCArtboard>
      </DCSection>

      <DCSection id="ecrans-clair" title="03 · Écrans · Mode clair" subtitle="Tous les écrans clés et leurs états — lisibles au soleil">
        {ScreenBoard({ theme: 'light' })}
      </DCSection>

      <DCSection id="ecrans-sombre" title="04 · Écrans · Mode sombre" subtitle="Charbon chaud — confort en intérieur et de nuit">
        {DarkScreenBoard()}
      </DCSection>

      <DCSection id="proto" title="05 · Prototype interactif" subtitle="Cliquable de bout en bout — autorisez, scannez, ouvrez la fiche, discutez. Changez le thème dans Réglages.">
        <DCArtboard id="ios-light" label="iOS · Clair — interactif" width={446} height={918} style={{ background: '#EDE7DC' }}>
          <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <CiceroPhone kind="ios" appProps={{ startTheme: 'light', startScreen: 'onboarding' }} />
          </div>
        </DCArtboard>
        <DCArtboard id="ios-dark" label="iOS · Sombre — interactif" width={446} height={918} style={{ background: '#1A1813' }}>
          <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <CiceroPhone kind="ios" appProps={{ startTheme: 'dark', startScreen: 'scanner', startScan: 'searching' }} />
          </div>
        </DCArtboard>
        <DCArtboard id="android-light" label="Android · Clair — interactif" width={456} height={936} style={{ background: '#EDE7DC' }}>
          <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <CiceroPhone kind="android" appProps={{ startTheme: 'light', startScreen: 'scanner', startScan: 'searching' }} />
          </div>
        </DCArtboard>
      </DCSection>
    </DesignCanvas>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<CiceroDoc />);
