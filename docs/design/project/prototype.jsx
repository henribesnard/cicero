/* ============================================================
   CICERO — prototype.jsx
   Interactive state machine wiring every screen + device frame.
   Exported to window: CiceroApp, CiceroPhone
   ============================================================ */

function useResolvedTheme(theme) {
  const [sys, setSys] = React.useState(() =>
    window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  React.useEffect(() => {
    if (!window.matchMedia) return;
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const fn = e => setSys(e.matches ? 'dark' : 'light');
    mq.addEventListener && mq.addEventListener('change', fn);
    return () => mq.removeEventListener && mq.removeEventListener('change', fn);
  }, []);
  return theme === 'auto' ? sys : theme;
}

function CiceroApp({ startTheme = 'light', startScreen = 'onboarding', startScan = 'searching', startMonument = 'eiffel', autoScan = true }) {
  const D = window.CIC_DATA;
  const [theme, setTheme] = React.useState(startTheme);
  const [screen, setScreen] = React.useState(startScreen);
  const [obStep, setObStep] = React.useState(0);
  const [scanMode, setScanMode] = React.useState(startScan);
  const [monId, setMonId] = React.useState(startMonument);
  const [messages, setMessages] = React.useState([]);
  const [typing, setTyping] = React.useState(false);
  const [draft, setDraft] = React.useState('');
  const resolved = useResolvedTheme(theme);
  const mon = D.MONUMENTS[monId] || D.MONUMENTS.eiffel;

  // auto scan: searching -> recognized
  React.useEffect(() => {
    if (screen === 'scanner' && scanMode === 'searching' && autoScan) {
      const t = setTimeout(() => setScanMode('recognized'), 2000);
      return () => clearTimeout(t);
    }
  }, [screen, scanMode, autoScan]);

  // chat answer engine
  const askQuestion = (q) => {
    setScreen('chat');
    setMessages(prev => [...prev, { role: 'user', text: q }]);
    setDraft('');
    setTyping(true);
    setTimeout(() => {
      const answer = (mon.chat && mon.chat[q]) ||
        "D'après mes sources vérifiées, ce monument recèle bien des détails. Posez-moi une question précise sur son histoire, son architecture ou ses anecdotes.";
      setTyping(false);
      setMessages(prev => [...prev, { role: 'assistant', text: answer, verified: true, sources: '3 sources' }]);
    }, 1500);
  };

  const openMonument = (id) => { setMonId(id); setScreen('sheet'); };
  const startChatFresh = () => { setMessages([]); setScreen('chat'); };

  let content;
  if (screen === 'onboarding') {
    content = <OnboardingScreen step={obStep}
      onNext={() => { if (obStep < 2) setObStep(obStep + 1); else { setScreen('scanner'); setScanMode('searching'); } }}
      onSkip={() => { if (obStep < 2) setObStep(obStep + 1); else { setScreen('scanner'); setScanMode('searching'); } }} />;
  } else if (screen === 'scanner') {
    content = <ScannerScreen mode={scanMode} data={mon}
      onCarnet={() => setScreen('carnet')}
      onSettings={() => setScreen('settings')}
      onShutter={() => setScanMode('recognized')}
      onPill={() => setScreen('sheet')}
      onAlts={() => setScreen('sheet')} />;
  } else if (screen === 'sheet') {
    content = <MonumentSheet data={mon}
      onClose={() => { setScreen('scanner'); setScanMode('recognized'); }}
      onAsk={startChatFresh}
      onSuggest={(q) => { setMessages([]); askQuestion(q); }} />;
  } else if (screen === 'chat') {
    content = <ChatScreen data={mon} messages={messages} typing={typing} draft={draft} onDraft={setDraft}
      onBack={() => setScreen('sheet')}
      onSend={(t) => askQuestion(t)}
      onSuggest={(q) => askQuestion(q)} />;
  } else if (screen === 'carnet') {
    content = <TravelLogScreen onBack={() => setScreen('scanner')} onOpen={openMonument} />;
  } else if (screen === 'offline') {
    content = <OfflineScreen onBack={() => setScreen('settings')} />;
  } else if (screen === 'settings') {
    content = <SettingsScreen theme={theme} onTheme={setTheme} onBack={() => setScreen('scanner')} onOffline={() => setScreen('offline')} />;
  }

  return (
    <div data-theme={resolved} style={{ width: '100%', height: '100%', position: 'relative', background: 'var(--bg)' }}>
      {content}
    </div>
  );
}

// Wrap the app in a device frame. kind: 'ios' | 'android'
function CiceroPhone({ kind = 'ios', appProps = {}, scale = 1 }) {
  const resolved = (appProps.startTheme === 'dark') ? true : false;
  const inner = <CiceroApp {...appProps} />;
  const frame = kind === 'android'
    ? <AndroidDevice dark={resolved}>{inner}</AndroidDevice>
    : <IOSDevice dark={resolved}>{inner}</IOSDevice>;
  if (scale === 1) return frame;
  return <div style={{ transform: `scale(${scale})`, transformOrigin: 'top left' }}>{frame}</div>;
}

Object.assign(window, { CiceroApp, CiceroPhone, useResolvedTheme });
