/* ============================================================
   CICERO — screens2.jsx  (app-context screens)
   Chat · Travel log (Carnet) · Offline · Settings
   Pure components driven by props. Exported to window.
   ============================================================ */

// ---------- shared header for solid screens ----------
function ScreenHeader({ title, onBack, trailing, subtitle, large = true }) {
  return (
    <div style={{ flexShrink: 0, paddingTop: SAFE_TOP, background: 'var(--bg)',
      borderBottom: large ? 'none' : '1px solid var(--hairline)' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '6px 16px 8px', minHeight: 44 }}>
        {onBack && (
          <button className="focusable" onClick={onBack} aria-label="Retour" style={{ width: 38, height: 38, borderRadius: '50%',
            border: 'none', background: 'var(--surface)', boxShadow: '0 1px 3px rgba(0,0,0,0.06)', cursor: 'pointer',
            display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, color: 'var(--ink)' }}>
            <Icon name="chevronLeft" size={20} />
          </button>
        )}
        {!large && <div className="cic-display" style={{ flex: 1, fontSize: 19, fontWeight: 600, color: 'var(--ink)',
          letterSpacing: '-0.01em', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{title}</div>}
        <div style={{ flex: large ? 1 : 'none' }} />
        {trailing}
      </div>
      {large && (
        <div style={{ padding: '2px 20px 16px' }}>
          <h1 className="cic-display" style={{ margin: 0, fontSize: 32, fontWeight: 500, color: 'var(--ink)',
            letterSpacing: '-0.02em', lineHeight: 1.05 }}>{title}</h1>
          {subtitle && <p className="cic-ui" style={{ margin: '6px 0 0', fontSize: 14.5, color: 'var(--ink-muted)', fontWeight: 500 }}>{subtitle}</p>}
        </div>
      )}
    </div>
  );
}

// mini scene thumbnail
function SceneThumb({ tone, monument, size = 60, radius = 16 }) {
  return (
    <div style={{ width: size, height: size, borderRadius: radius, overflow: 'hidden', position: 'relative', flexShrink: 0,
      boxShadow: 'inset 0 0 0 1px var(--hairline)' }}>
      <CameraScene tone={tone} monument={monument} />
    </div>
  );
}

/* ====================== CHAT ====================== */
function ChatScreen({ data, messages = [], typing = false, onBack = () => {}, onSend = () => {}, onSuggest = () => {}, draft = '', onDraft = () => {} }) {
  const m = data || window.CIC_DATA.MONUMENTS.eiffel;
  const listRef = React.useRef(null);
  React.useEffect(() => { if (listRef.current) listRef.current.scrollTop = listRef.current.scrollHeight; }, [messages.length, typing]);
  const showSuggest = messages.filter(x => x.role === 'user').length === 0;

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', display: 'flex', flexDirection: 'column',
      background: 'var(--bg)' }}>
      {/* header */}
      <div style={{ flexShrink: 0, paddingTop: SAFE_TOP, background: 'var(--surface)', borderBottom: '1px solid var(--hairline)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 11, padding: '8px 14px 12px' }}>
          <button className="focusable" onClick={onBack} aria-label="Retour" style={{ width: 38, height: 38, borderRadius: '50%',
            border: 'none', background: 'var(--surface-2)', cursor: 'pointer', display: 'flex', alignItems: 'center',
            justifyContent: 'center', flexShrink: 0, color: 'var(--ink)' }}>
            <Icon name="chevronLeft" size={20} />
          </button>
          <SceneThumb tone={m.tone} monument={m.monument} size={40} radius={12} />
          <div style={{ flex: 1, minWidth: 0 }}>
            <div className="cic-display" style={{ fontSize: 17, fontWeight: 600, color: 'var(--ink)', lineHeight: 1.1,
              whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{m.name}</div>
            <div className="cic-ui" style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: 12.5, color: 'var(--teal-600)', fontWeight: 600, marginTop: 1 }}>
              <Icon name="shield" size={12} stroke="var(--teal-600)" sw={2.2} /> Guide vérifié
            </div>
          </div>
          <ConfidenceBadge score={m.score} />
        </div>
      </div>

      {/* messages */}
      <div ref={listRef} style={{ flex: 1, overflow: 'auto', padding: '18px 16px', display: 'flex', flexDirection: 'column', gap: 14 }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ animation: 'cic-fade-up .35s var(--ease-out)' }}>
            <ChatBubble role={msg.role} verified={msg.verified} sources={msg.sources}>{msg.text}</ChatBubble>
          </div>
        ))}
        {typing && <div style={{ animation: 'cic-fade-up .3s' }}><ChatBubble role="typing" /></div>}
      </div>

      {/* suggested + input */}
      <div style={{ flexShrink: 0, background: 'var(--surface)', borderTop: '1px solid var(--hairline)',
        padding: '12px 14px', paddingBottom: SAFE_BOTTOM + 4 }}>
        {showSuggest && (
          <div style={{ display: 'flex', gap: 8, overflowX: 'auto', paddingBottom: 12, margin: '0 -2px' }}>
            {m.suggested.map((q, i) => (
              <button key={i} className="cic-ui focusable" onClick={() => onSuggest(q)} style={{ flexShrink: 0, padding: '9px 14px',
                borderRadius: 99, border: '1px solid var(--hairline-strong)', background: 'var(--surface-2)', cursor: 'pointer',
                fontSize: 13.5, fontWeight: 500, color: 'var(--ink)', whiteSpace: 'nowrap' }}>{q}</button>
            ))}
          </div>
        )}
        <div style={{ display: 'flex', alignItems: 'center', gap: 9 }}>
          <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 8, padding: '6px 8px 6px 16px',
            borderRadius: 'var(--r-pill)', border: '1px solid var(--hairline-strong)', background: 'var(--surface-2)' }}>
            <input value={draft} onChange={e => onDraft(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter' && draft.trim()) onSend(draft); }}
              placeholder="Écrivez votre question…" className="cic-ui" aria-label="Votre question"
              style={{ flex: 1, border: 'none', outline: 'none', background: 'transparent', fontSize: 15.5,
                color: 'var(--ink)', minWidth: 0 }} />
            <button aria-label="Dictée" className="focusable" style={{ border: 'none', background: 'transparent', cursor: 'pointer',
              color: 'var(--ink-muted)', display: 'flex', padding: 2 }}><Icon name="mic" size={20} /></button>
          </div>
          <button aria-label="Envoyer" onClick={() => draft.trim() && onSend(draft)} className="focusable" style={{ width: 46, height: 46,
            borderRadius: '50%', border: 'none', background: draft.trim() ? 'var(--accent)' : 'var(--hairline-strong)',
            cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
            transition: 'background .2s' }}>
            <Icon name="send" size={20} stroke={draft.trim() ? 'var(--accent-ink)' : 'var(--ink-faint)'} sw={2} />
          </button>
        </div>
      </div>
    </div>
  );
}

/* ====================== TRAVEL LOG (Carnet) ====================== */
function TravelLogScreen({ onBack = () => {}, onOpen = () => {} }) {
  const log = window.CIC_DATA.TRAVEL_LOG;
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', display: 'flex', flexDirection: 'column', background: 'var(--bg)' }}>
      <ScreenHeader title="Carnet de voyage" subtitle={`${log.length} monuments · 1 ville`} onBack={onBack}
        trailing={<GlassIconBtnSolid name="share" ariaLabel="Partager le carnet" />} />
      <div style={{ flex: 1, overflow: 'auto', padding: '4px 16px', paddingBottom: SAFE_BOTTOM + 16 }}>
        {/* search */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 9, padding: '11px 15px', borderRadius: 'var(--r-pill)',
          background: 'var(--surface)', border: '1px solid var(--hairline)', marginBottom: 18 }}>
          <Icon name="scan" size={17} stroke="var(--ink-faint)" />
          <span className="cic-ui" style={{ color: 'var(--ink-faint)', fontSize: 15 }}>Rechercher dans le carnet</span>
        </div>

        {/* journal entries */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          {log.map((e, i) => (
            <button key={i} onClick={() => onOpen(e.id)} className="focusable" style={{ display: 'flex', gap: 14, alignItems: 'center',
              padding: 12, borderRadius: 'var(--r-card)', background: 'var(--surface)', border: '0.5px solid var(--hairline)',
              cursor: 'pointer', textAlign: 'left', boxShadow: '0 1px 3px rgba(40,34,24,0.04)' }}>
              <SceneThumb tone={e.tone} monument={e.monument} size={66} radius={18} />
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 7 }}>
                  <h3 className="cic-display" style={{ margin: 0, fontSize: 18, fontWeight: 600, color: 'var(--ink)',
                    letterSpacing: '-0.01em', lineHeight: 1.1, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{e.name}</h3>
                  {e.fav && <Icon name="bookmark" size={14} stroke="var(--terra-500)" fill="var(--terra-500)" sw={1.5} />}
                </div>
                <div className="cic-ui" style={{ display: 'flex', alignItems: 'center', gap: 5, marginTop: 4, color: 'var(--ink-muted)', fontSize: 13.5 }}>
                  <Icon name="pin" size={13} stroke="var(--ink-faint)" sw={2} /> {e.place}
                </div>
                <div className="cic-ui" style={{ marginTop: 6, fontSize: 12.5, color: 'var(--ink-faint)', fontWeight: 500 }}>{e.date}</div>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 4 }}>
                <ConfidenceBadge score={e.score} />
                <Icon name="chevronRight" size={16} stroke="var(--ink-faint)" />
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

// solid-bg round icon button (for headers)
function GlassIconBtnSolid({ name, onClick, ariaLabel }) {
  return (
    <button className="focusable" onClick={onClick} aria-label={ariaLabel} style={{ width: 38, height: 38, borderRadius: '50%',
      border: 'none', background: 'var(--surface)', boxShadow: '0 1px 3px rgba(0,0,0,0.06)', cursor: 'pointer',
      display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--ink)' }}>
      <Icon name={name} size={19} />
    </button>
  );
}

/* ====================== OFFLINE ====================== */
function OfflineScreen({ onBack = () => {} }) {
  const cities = window.CIC_DATA.OFFLINE_CITIES;
  const cityRow = (c) => {
    const stateUI = {
      downloaded: { label: `${c.count} sites · ${c.size}`, action: <Icon name="cloudDone" size={22} stroke="var(--teal-600)" sw={1.9} /> },
      downloading: { label: `Téléchargement… ${c.progress}%`, action: <Spinner /> },
      available: { label: `${c.count} sites · ${c.size}`, action: <DownloadBtn /> },
    }[c.state];
    return (
      <div key={c.id} style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 13, padding: '14px 16px' }}>
          <div style={{ width: 42, height: 42, borderRadius: 12, background: c.state === 'available' ? 'var(--surface-2)' : 'var(--accent-soft)',
            display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
            <Icon name="pin" size={20} stroke={c.state === 'available' ? 'var(--ink-muted)' : 'var(--accent)'} sw={1.9} />
          </div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div className="cic-ui" style={{ fontSize: 16, fontWeight: 600, color: 'var(--ink)' }}>{c.name} <span style={{ color: 'var(--ink-faint)', fontWeight: 500 }}>· {c.country}</span></div>
            <div className="cic-ui" style={{ fontSize: 13, color: c.state === 'downloading' ? 'var(--accent)' : 'var(--ink-muted)', marginTop: 2, fontWeight: 500 }}>{stateUI.label}</div>
          </div>
          {stateUI.action}
        </div>
        {c.state === 'downloading' && (
          <div style={{ padding: '0 16px 12px' }}>
            <div style={{ height: 6, borderRadius: 99, background: 'var(--hairline)', overflow: 'hidden' }}>
              <div style={{ height: '100%', width: `${c.progress}%`, background: 'var(--accent)', borderRadius: 99 }} />
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', display: 'flex', flexDirection: 'column', background: 'var(--bg)' }}>
      <ScreenHeader title="Hors-ligne" subtitle="Explorez sans connexion ni frais de données" onBack={onBack} />
      <div style={{ flex: 1, overflow: 'auto', padding: '4px 16px', paddingBottom: SAFE_BOTTOM + 16 }}>
        {/* storage summary */}
        <div style={{ borderRadius: 'var(--r-card)', padding: '18px 18px 16px', marginBottom: 20,
          background: 'linear-gradient(150deg, var(--teal-600), var(--teal-800))', color: '#fff' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
            <span className="cic-ui" style={{ fontSize: 13.5, fontWeight: 600, opacity: 0.85 }}>Stockage utilisé</span>
            <span className="cic-mono tnum" style={{ fontSize: 13.5, fontWeight: 600, opacity: 0.85 }}>408 Mo / 2 Go</span>
          </div>
          <div className="cic-display" style={{ fontSize: 27, fontWeight: 500, margin: '8px 0 12px' }}>2 villes prêtes</div>
          <div style={{ height: 7, borderRadius: 99, background: 'rgba(255,255,255,0.25)', overflow: 'hidden' }}>
            <div style={{ height: '100%', width: '20%', background: '#fff', borderRadius: 99 }} />
          </div>
        </div>

        <SectionTitle>Sur cet appareil</SectionTitle>
        <div className="surface-card" style={{ borderRadius: 'var(--r-card)', overflow: 'hidden', marginBottom: 20, divideStyle: 'x' }}>
          {cities.filter(c => c.state !== 'available').map((c, i, a) => (
            <div key={c.id} style={{ borderTop: i ? '1px solid var(--hairline)' : 'none' }}>{cityRow(c)}</div>
          ))}
        </div>

        <SectionTitle>Disponibles au téléchargement</SectionTitle>
        <div className="surface-card" style={{ borderRadius: 'var(--r-card)', overflow: 'hidden' }}>
          {cities.filter(c => c.state === 'available').map((c, i) => (
            <div key={c.id} style={{ borderTop: i ? '1px solid var(--hairline)' : 'none' }}>{cityRow(c)}</div>
          ))}
        </div>
      </div>
    </div>
  );
}
function SectionTitle({ children }) {
  return <div className="cic-ui" style={{ fontSize: 12.5, fontWeight: 700, letterSpacing: '0.06em', textTransform: 'uppercase',
    color: 'var(--ink-faint)', padding: '0 6px 10px' }}>{children}</div>;
}
function Spinner() {
  return <div style={{ width: 22, height: 22, borderRadius: '50%', border: '2.5px solid var(--accent-soft)',
    borderTopColor: 'var(--accent)', animation: 'cic-spin .8s linear infinite' }} />;
}
function DownloadBtn() {
  return <button className="cic-ui focusable" aria-label="Télécharger" style={{ display: 'flex', alignItems: 'center', gap: 6,
    padding: '8px 14px', borderRadius: 99, border: 'none', background: 'var(--accent-soft)', color: 'var(--accent)',
    fontSize: 14, fontWeight: 600, cursor: 'pointer' }}><Icon name="download" size={16} sw={2} /> Obtenir</button>;
}

/* ====================== SETTINGS ====================== */
function SettingsScreen({ theme = 'light', onTheme = () => {}, onBack = () => {}, onOffline = () => {} }) {
  const [loc, setLoc] = React.useState(true);
  const [bigText, setBigText] = React.useState(false);
  const [contrast, setContrast] = React.useState(true);
  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', display: 'flex', flexDirection: 'column', background: 'var(--bg)' }}>
      <ScreenHeader title="Réglages" onBack={onBack} />
      <div style={{ flex: 1, overflow: 'auto', padding: '4px 16px', paddingBottom: SAFE_BOTTOM + 16 }}>
        {/* appearance segmented */}
        <SectionTitle>Apparence</SectionTitle>
        <div className="surface-card" style={{ borderRadius: 'var(--r-card)', padding: 14, marginBottom: 20 }}>
          <Segmented value={theme} onChange={onTheme} options={[
            { v: 'light', label: 'Clair', icon: 'sun' },
            { v: 'dark', label: 'Sombre', icon: 'moon' },
            { v: 'auto', label: 'Auto', icon: 'refresh' },
          ]} />
        </div>

        <SectionTitle>Langue & lecture</SectionTitle>
        <div className="surface-card" style={{ borderRadius: 'var(--r-card)', overflow: 'hidden', marginBottom: 20 }}>
          <Row icon="globe" label="Langue de l'app" detail="Français" chevron />
          <Row icon="ear" label="Lecture à voix haute" detail="VoiceOver prêt" chevron border />
          <ToggleRow icon="info" label="Texte plus grand" value={bigText} onChange={setBigText} border />
          <ToggleRow icon="shield" label="Contraste renforcé" sub="Meilleure lisibilité au soleil" value={contrast} onChange={setContrast} border />
        </div>

        <SectionTitle>Confidentialité & données</SectionTitle>
        <div className="surface-card" style={{ borderRadius: 'var(--r-card)', overflow: 'hidden', marginBottom: 12 }}>
          <div style={{ display: 'flex', gap: 12, padding: '14px 16px', alignItems: 'flex-start' }}>
            <div style={{ width: 34, height: 34, borderRadius: 9, background: 'var(--accent-soft)', display: 'flex',
              alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
              <Icon name="lock" size={18} stroke="var(--accent)" sw={1.9} /></div>
            <div style={{ flex: 1 }}>
              <div className="cic-ui" style={{ fontSize: 15.5, fontWeight: 600, color: 'var(--ink)' }}>Analyse sur l'appareil</div>
              <div className="cic-ui" style={{ fontSize: 13, color: 'var(--ink-muted)', marginTop: 3, lineHeight: 1.45 }}>
                La reconnaissance s'effectue localement. Vos photos ne sont jamais envoyées sans votre accord.</div>
            </div>
          </div>
          <ToggleRow icon="pin" label="Utiliser ma position" value={loc} onChange={setLoc} border />
          <Row icon="download" label="Gérer les téléchargements" detail="408 Mo" chevron border onClick={onOffline} />
          <Row icon="trash" label="Effacer l'historique" danger border />
        </div>

        <p className="cic-ui" style={{ textAlign: 'center', color: 'var(--ink-faint)', fontSize: 12.5, marginTop: 18 }}>
          Cicero · version 1.0 · Données © OpenStreetMap</p>
      </div>
    </div>
  );
}

function Segmented({ value, onChange, options }) {
  return (
    <div style={{ display: 'flex', gap: 6, background: 'var(--surface-2)', borderRadius: 14, padding: 5 }}>
      {options.map(o => {
        const active = value === o.v;
        return (
          <button key={o.v} onClick={() => onChange(o.v)} className="cic-ui focusable" style={{ flex: 1, display: 'flex',
            flexDirection: 'column', alignItems: 'center', gap: 5, padding: '10px 4px', borderRadius: 10, border: 'none',
            background: active ? 'var(--surface)' : 'transparent', cursor: 'pointer', color: active ? 'var(--accent)' : 'var(--ink-muted)',
            fontSize: 13, fontWeight: 600, boxShadow: active ? '0 1px 4px rgba(0,0,0,0.1)' : 'none', transition: 'all .15s' }}>
            <Icon name={o.icon} size={18} sw={1.9} /> {o.label}
          </button>
        );
      })}
    </div>
  );
}

function Row({ icon, label, detail, chevron, border, danger, onClick }) {
  return (
    <button className="cic-ui focusable" onClick={onClick} style={{ width: '100%', display: 'flex', alignItems: 'center', gap: 12,
      padding: '13px 16px', border: 'none', borderTop: border ? '1px solid var(--hairline)' : 'none', background: 'transparent',
      cursor: onClick ? 'pointer' : 'default', textAlign: 'left' }}>
      <div style={{ width: 34, height: 34, borderRadius: 9, background: danger ? 'rgba(214,122,72,0.14)' : 'var(--surface-2)',
        display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
        <Icon name={icon} size={18} stroke={danger ? 'var(--terra-600)' : 'var(--ink-muted)'} sw={1.9} /></div>
      <span style={{ flex: 1, fontSize: 15.5, fontWeight: 500, color: danger ? 'var(--terra-600)' : 'var(--ink)' }}>{label}</span>
      {detail && <span style={{ fontSize: 14.5, color: 'var(--ink-faint)', fontWeight: 500 }}>{detail}</span>}
      {chevron && <Icon name="chevronRight" size={17} stroke="var(--ink-faint)" />}
    </button>
  );
}

function ToggleRow({ icon, label, sub, value, onChange, border }) {
  return (
    <div className="cic-ui" style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '13px 16px',
      borderTop: border ? '1px solid var(--hairline)' : 'none' }}>
      <div style={{ width: 34, height: 34, borderRadius: 9, background: 'var(--surface-2)', display: 'flex',
        alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
        <Icon name={icon} size={18} stroke="var(--ink-muted)" sw={1.9} /></div>
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 15.5, fontWeight: 500, color: 'var(--ink)' }}>{label}</div>
        {sub && <div style={{ fontSize: 12.5, color: 'var(--ink-muted)', marginTop: 2 }}>{sub}</div>}
      </div>
      <Toggle value={value} onChange={onChange} label={label} />
    </div>
  );
}
function Toggle({ value, onChange, label }) {
  return (
    <button role="switch" aria-checked={value} aria-label={label} onClick={() => onChange(!value)} className="focusable" style={{ width: 50, height: 30,
      borderRadius: 99, border: 'none', background: value ? 'var(--accent)' : 'var(--hairline-strong)', cursor: 'pointer',
      position: 'relative', transition: 'background .2s', flexShrink: 0 }}>
      <span style={{ position: 'absolute', top: 3, left: value ? 23 : 3, width: 24, height: 24, borderRadius: '50%',
        background: '#fff', boxShadow: '0 1px 3px rgba(0,0,0,0.25)', transition: 'left .2s var(--ease-out)' }} />
    </button>
  );
}

Object.assign(window, { ScreenHeader, SceneThumb, ChatScreen, TravelLogScreen, OfflineScreen, SettingsScreen,
  Segmented, Row, ToggleRow, Toggle, SectionTitle, GlassIconBtnSolid });
