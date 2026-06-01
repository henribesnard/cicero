/* ============================================================
   CICERO — screens.jsx  (camera-context screens)
   Onboarding · Scanner (3 states) · Monument sheet
   Pure components driven by props. Exported to window.
   ============================================================ */

const SAFE_TOP = 58, SAFE_BOTTOM = 34;

// ---------- generic privacy reassurance chip ----------
function PrivacyNote({ icon = 'lock', children, onCamera = false }) {
  return (
    <div className="cic-ui" style={{
      display: 'inline-flex', alignItems: 'center', gap: 9, padding: '9px 14px',
      borderRadius: 'var(--r-pill)',
      background: onCamera ? 'var(--glass-bg)' : 'var(--accent-soft)',
      color: onCamera ? 'var(--glass-ink)' : 'var(--accent)',
      fontSize: 13, fontWeight: 600, lineHeight: 1.2,
    }}>
      <Icon name={icon} size={15} sw={2} />
      <span>{children}</span>
    </div>
  );
}

/* ====================== ONBOARDING ====================== */
function OnboardingScreen({ step = 0, onNext = () => {}, onSkip = () => {} }) {
  const steps = [
    {
      tone: 'dawn', monument: 'tower',
      eyebrow: 'Bienvenue',
      title: 'Votre cicérone\nde poche',
      body: "Pointez votre appareil vers un monument. Cicero l'identifie en moins d'une seconde et vous raconte son histoire.",
      cta: 'Commencer',
      foot: null,
    },
    {
      icon: 'scan',
      eyebrow: 'Permission · 1 sur 2',
      title: 'Activez\nla caméra',
      body: "Cicero a besoin de la caméra pour reconnaître ce que vous regardez. L'analyse se fait directement sur l'appareil.",
      cta: 'Autoriser la caméra',
      foot: { icon: 'lock', text: "Vos photos ne quittent jamais votre téléphone." },
    },
    {
      icon: 'pin',
      eyebrow: 'Permission · 2 sur 2',
      title: 'Position\n(optionnel)',
      body: "La localisation affine les résultats et suggère les monuments proches. Vous pouvez l'activer plus tard.",
      cta: 'Autoriser la position',
      foot: { icon: 'cloudOff', text: 'Fonctionne aussi hors-ligne pour les villes téléchargées.' },
    },
  ];
  const s = steps[step] || steps[0];
  const isWelcome = step === 0;

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', overflow: 'hidden',
      background: 'var(--bg)', display: 'flex', flexDirection: 'column' }}>
      {/* hero visual */}
      <div style={{ position: 'relative', height: isWelcome ? '52%' : '40%', overflow: 'hidden',
        borderBottomLeftRadius: 34, borderBottomRightRadius: 34 }}>
        {isWelcome ? (
          <CameraScene tone={s.tone} monument={s.monument} blur={1.5}>
            {/* faux viewfinder peek */}
            <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Brackets size={150} color="rgba(255,255,255,0.9)" />
            </div>
            <div style={{ position: 'absolute', left: '50%', bottom: 26, transform: 'translateX(-50%)' }}>
              <DetectionPill state="recognized" name="Tour Eiffel" score={98} place="Paris" />
            </div>
          </CameraScene>
        ) : (
          <div style={{ position: 'absolute', inset: 0,
            background: 'linear-gradient(160deg, var(--teal-600), var(--teal-800))',
            display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <div className="glass" style={{ width: 116, height: 116, borderRadius: 32,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              animation: 'cic-pop-in .5s var(--ease-spring)' }}>
              <Icon name={s.icon} size={52} stroke="#fff" sw={1.6} />
            </div>
            {/* step dots */}
            <div style={{ position: 'absolute', bottom: 18, left: '50%', transform: 'translateX(-50%)',
              display: 'flex', gap: 7 }}>
              {[1,2].map(i => <span key={i} style={{ width: i === step ? 22 : 7, height: 7, borderRadius: 99,
                background: i === step ? '#fff' : 'rgba(255,255,255,0.45)', transition: 'all .3s' }} />)}
            </div>
          </div>
        )}
        <div style={{ position: 'absolute', top: SAFE_TOP - 18, left: 22 }}><Logo size={19} onCamera /></div>
        {!isWelcome && (
          <button className="cic-ui focusable" onClick={onSkip} style={{ position: 'absolute', top: SAFE_TOP - 22, right: 18,
            background: 'rgba(255,255,255,0.18)', border: 'none', color: '#fff', fontWeight: 600, fontSize: 14,
            padding: '8px 14px', borderRadius: 99, cursor: 'pointer' }}>Plus tard</button>
        )}
      </div>

      {/* copy + actions */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: '28px 26px',
        paddingBottom: SAFE_BOTTOM + 18 }}>
        <span className="cic-ui" style={{ fontSize: 13, fontWeight: 700, letterSpacing: '0.08em',
          textTransform: 'uppercase', color: 'var(--accent)' }}>{s.eyebrow}</span>
        <h1 className="cic-display" style={{ margin: '12px 0 0', fontSize: 38, lineHeight: 1.04, fontWeight: 500,
          color: 'var(--ink)', letterSpacing: '-0.02em', whiteSpace: 'pre-line' }}>{s.title}</h1>
        <p className="cic-ui" style={{ margin: '16px 0 0', fontSize: 16.5, lineHeight: 1.5, color: 'var(--ink-muted)',
          fontWeight: 400, maxWidth: 320, textWrap: 'pretty' }}>{s.body}</p>

        <div style={{ flex: 1 }} />

        {s.foot && (
          <div style={{ marginBottom: 16 }}>
            <PrivacyNote icon={s.foot.icon}>{s.foot.text}</PrivacyNote>
          </div>
        )}
        <Btn variant="primary" size="lg" full iconRight={isWelcome ? 'chevronRight' : 'check'} onClick={onNext}>{s.cta}</Btn>
        {isWelcome && (
          <p className="cic-ui" style={{ textAlign: 'center', marginTop: 14, fontSize: 13, color: 'var(--ink-faint)' }}>
            En continuant, vous acceptez nos <u>conditions</u>.</p>
        )}
      </div>
    </div>
  );
}

/* ====================== SCANNER ====================== */
function ScannerTopBar({ offline = true }) {
  return (
    <div style={{ position: 'absolute', top: SAFE_TOP - 10, left: 16, right: 16, zIndex: 10,
      display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
      <Logo size={18} onCamera />
      <div style={{ display: 'flex', gap: 9, alignItems: 'center' }}>
        {offline && (
          <div className="glass cic-ui" style={{ display: 'flex', alignItems: 'center', gap: 7, padding: '8px 12px',
            borderRadius: 99, color: 'var(--glass-ink)', fontSize: 12.5, fontWeight: 600 }}>
            <Icon name="cloudDone" size={15} stroke="var(--teal-400)" sw={2} /> Paris · hors-ligne
          </div>
        )}
        <GlassIconBtn name="flash" size={40} iconSize={19} ariaLabel="Flash" />
      </div>
    </div>
  );
}

function ScannerBottomBar({ onCarnet, onShutter, onSettings }) {
  return (
    <div style={{ position: 'absolute', left: 0, right: 0, bottom: SAFE_BOTTOM + 10, zIndex: 10,
      display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 34 }}>
      <GlassIconBtn name="book" size={54} iconSize={24} onClick={onCarnet} ariaLabel="Carnet de voyage" badge={4} />
      {/* shutter */}
      <button className="focusable" onClick={onShutter} aria-label="Capturer" style={{
        width: 78, height: 78, borderRadius: '50%', border: 'none', cursor: 'pointer', padding: 0,
        background: 'transparent', position: 'relative' }}>
        <span className="glass" style={{ position: 'absolute', inset: 0, borderRadius: '50%' }} />
        <span style={{ position: 'absolute', inset: 7, borderRadius: '50%', background: '#fff',
          boxShadow: '0 2px 8px rgba(0,0,0,0.3), inset 0 0 0 3px rgba(0,0,0,0.06)' }} />
        <span style={{ position: 'absolute', inset: 13, borderRadius: '50%',
          border: '2.5px solid var(--teal-500)' }} />
      </button>
      <GlassIconBtn name="sliders" size={54} iconSize={24} onClick={onSettings} ariaLabel="Réglages" />
    </div>
  );
}

function ScannerScreen({ mode = 'searching', data, onCarnet = () => {}, onSettings = () => {}, onShutter = () => {}, onPill = () => {}, onAlts = () => {} }) {
  const m = data || window.CIC_DATA.MONUMENTS.eiffel;
  const recognized = mode === 'recognized';
  const uncertain = mode === 'uncertain';
  const lv = recognized ? 'var(--teal-400)' : uncertain ? 'var(--ochre-400)' : 'rgba(255,255,255,0.92)';
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', overflow: 'hidden' }}>
      <CameraScene tone={m.tone} monument={m.monument} slotId="cam-scanner" blur={mode === 'searching' ? 0.4 : 0} />
      <ScanOverlay active={mode === 'searching'} />

      {/* brackets */}
      <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', paddingBottom: 40 }}>
        <Brackets size={recognized ? 230 : uncertain ? 250 : 264} color={lv} active={mode === 'searching'} locked={recognized} thickness={recognized ? 3.5 : 3} />
        {recognized && <DetectionPing y="44%" />}
      </div>

      <ScannerTopBar />

      {/* hint + detection pill stack */}
      <div style={{ position: 'absolute', left: 0, right: 0, bottom: SAFE_BOTTOM + 104, zIndex: 9,
        display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12, padding: '0 18px' }}>
        {mode === 'searching' && (
          <div className="cic-ui glass" style={{ padding: '9px 16px', borderRadius: 99, color: 'var(--glass-ink)',
            fontSize: 14, fontWeight: 600 }}>Pointez vers un monument</div>
        )}
        {mode === 'searching'
          ? <DetectionPill state="searching" />
          : <div style={{ animation: 'cic-pop-in .45s var(--ease-spring)' }}>
              <DetectionPill state={mode} name={m.name} score={m.score} place={m.place} onClick={onPill} />
            </div>}
        {recognized && (
          <span className="cic-ui" style={{ color: 'rgba(255,255,255,0.9)', fontSize: 13, fontWeight: 500,
            textShadow: '0 1px 4px rgba(0,0,0,0.5)' }}>Touchez la pastille pour la fiche complète</span>
        )}
        {uncertain && (
          <button className="cic-ui focusable" onClick={onAlts} style={{ background: 'rgba(0,0,0,0.32)', border: '1px solid rgba(255,255,255,0.3)',
            color: '#fff', fontSize: 13, fontWeight: 600, padding: '8px 14px', borderRadius: 99, cursor: 'pointer',
            backdropFilter: 'blur(8px)' }}>
            Voir les autres possibilités ({window.CIC_DATA.UNCERTAIN_ALTS.length})</button>
        )}
      </div>

      <ScannerBottomBar onCarnet={onCarnet} onShutter={onShutter} onSettings={onSettings} />
    </div>
  );
}

/* ====================== MONUMENT SHEET ====================== */
function MonumentSheet({ data, onClose = () => {}, onAsk = () => {}, onSuggest = () => {}, embedded = false }) {
  const m = data || window.CIC_DATA.MONUMENTS.eiffel;
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', overflow: 'hidden' }}>
      {/* dimmed camera behind */}
      <CameraScene tone={m.tone} monument={m.monument} blur={3} />
      <div style={{ position: 'absolute', inset: 0, background: 'rgba(10,8,6,0.32)' }} />
      <ScannerTopBar />

      {/* close */}
      <div style={{ position: 'absolute', top: SAFE_TOP + 30, right: 16, zIndex: 12 }}>
        <GlassIconBtn name="close" size={40} iconSize={20} onClick={onClose} ariaLabel="Fermer la fiche" />
      </div>

      {/* sheet */}
      <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, top: 132, zIndex: 11,
        background: 'var(--surface)', borderTopLeftRadius: 'var(--r-sheet)', borderTopRightRadius: 'var(--r-sheet)',
        boxShadow: '0 -10px 40px rgba(0,0,0,0.25)', animation: embedded ? 'none' : 'cic-sheet-rise .5s var(--ease-out)',
        display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {/* grab handle */}
        <div style={{ display: 'flex', justifyContent: 'center', padding: '10px 0 4px', flexShrink: 0 }}>
          <div style={{ width: 40, height: 5, borderRadius: 99, background: 'var(--hairline-strong)' }} />
        </div>

        <div style={{ flex: 1, overflow: 'auto', padding: '8px 22px', paddingBottom: SAFE_BOTTOM + 16 }}>
          {/* title block */}
          <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 12 }}>
            <div style={{ minWidth: 0 }}>
              <h2 className="cic-display" style={{ margin: 0, fontSize: 30, fontWeight: 500, lineHeight: 1.06,
                color: 'var(--ink)', letterSpacing: '-0.02em' }}>{m.name}</h2>
              <div className="cic-ui" style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 8,
                color: 'var(--ink-muted)', fontSize: 14.5, fontWeight: 500 }}>
                <Icon name="pin" size={15} stroke="var(--accent)" sw={2} /> {m.place}
              </div>
            </div>
            <button className="cic-ui focusable" aria-label="Enregistrer" style={{ flexShrink: 0, background: 'var(--accent-soft)',
              border: 'none', borderRadius: 14, width: 42, height: 42, display: 'flex', alignItems: 'center',
              justifyContent: 'center', cursor: 'pointer', color: 'var(--accent)' }}>
              <Icon name="bookmark" size={20} sw={1.9} />
            </button>
          </div>

          {/* type + confidence */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12,
            marginTop: 16, padding: '12px 0', borderTop: '1px solid var(--hairline)', borderBottom: '1px solid var(--hairline)' }}>
            <span className="cic-ui" style={{ fontSize: 13.5, fontWeight: 600, color: 'var(--ink-muted)' }}>{m.type}</span>
            <ConfidenceMeter score={m.score} width={150} />
          </div>

          {/* stat tiles */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginTop: 16 }}>
            {m.stats.map((st, i) => <StatTile key={i} {...st} accent={i === 0} />)}
          </div>

          {/* blurb */}
          <p className="cic-ui" style={{ margin: '18px 0 0', fontSize: 15.5, lineHeight: 1.55, color: 'var(--ink)',
            fontWeight: 400, textWrap: 'pretty' }}>{m.blurb}</p>

          {/* assistant entry */}
          <div style={{ marginTop: 22 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
              <AssistantAvatar size={26} />
              <span className="cic-ui" style={{ fontSize: 14, fontWeight: 700, color: 'var(--ink)' }}>Demandez au guide</span>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 9 }}>
              {m.suggested.map((q, i) => <SuggestChip key={i} onClick={() => onSuggest(q)}>{q}</SuggestChip>)}
            </div>
          </div>
        </div>

        {/* ask input pinned */}
        <div style={{ flexShrink: 0, padding: '12px 18px', paddingBottom: SAFE_BOTTOM + 6,
          borderTop: '1px solid var(--hairline)', background: 'var(--surface)' }}>
          <button className="cic-ui focusable" onClick={onAsk} style={{ width: '100%', display: 'flex', alignItems: 'center',
            gap: 10, padding: '13px 16px', borderRadius: 'var(--r-pill)', border: '1px solid var(--hairline-strong)',
            background: 'var(--surface-2)', cursor: 'pointer', color: 'var(--ink-faint)', fontSize: 15, fontWeight: 500 }}>
            <Icon name="sparkle" size={18} stroke="var(--accent)" />
            <span style={{ flex: 1, textAlign: 'left' }}>Posez une question…</span>
            <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: 34, height: 34,
              borderRadius: '50%', background: 'var(--accent)' }}>
              <Icon name="send" size={17} stroke="var(--accent-ink)" sw={2} />
            </span>
          </button>
        </div>
      </div>
    </div>
  );
}

Object.assign(window, { PrivacyNote, OnboardingScreen, ScannerScreen, ScannerTopBar, ScannerBottomBar, MonumentSheet, SAFE_TOP, SAFE_BOTTOM });
