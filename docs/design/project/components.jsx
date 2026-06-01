/* ============================================================
   CICERO — components.jsx
   Primitives + icon set. Stateless. Exported to window.
   ============================================================ */

// ---------- Icon set (stroke-based, 24px grid) ----------
const ICONS = {
  scan: 'M4 8V6a2 2 0 0 1 2-2h2M16 4h2a2 2 0 0 1 2 2v2M20 16v2a2 2 0 0 1-2 2h-2M8 20H6a2 2 0 0 1-2-2v-2',
  shutter: '', // drawn specially
  book: 'M5 4.5A1.5 1.5 0 0 1 6.5 3H19v15.5H6.5A1.5 1.5 0 0 0 5 20M5 4.5v15.5M5 4.5V20M19 18.5V21',
  sliders: 'M4 7h10M18 7h2M4 17h2M10 17h10M14 5v4M8 15v4',
  chat: 'M4 5.5A1.5 1.5 0 0 1 5.5 4h13A1.5 1.5 0 0 1 20 5.5v9A1.5 1.5 0 0 1 18.5 16H9l-4 4v-4H5.5A1.5 1.5 0 0 1 4 14.5z',
  send: 'M4.5 12h13M11 5.5 17.5 12 11 18.5',
  download: 'M12 4v11m0 0 4-4m-4 4-4-4M5 19h14',
  check: 'M5 12.5 10 17.5 19 6.5',
  sparkle: 'M12 3.5c.4 3.5 1.5 4.6 5 5-3.5.4-4.6 1.5-5 5-.4-3.5-1.5-4.6-5-5 3.5-.4 4.6-1.5 5-5ZM18.5 13c.2 1.6.7 2.1 2.3 2.3-1.6.2-2.1.7-2.3 2.3-.2-1.6-.7-2.1-2.3-2.3 1.6-.2 2.1-.7 2.3-2.3Z',
  pin: 'M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11Z M12 12.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z',
  ruler: 'M4 14.5 14.5 4l5.5 5.5L9.5 20 4 14.5Z M8 10.5l1.7 1.7M11 7.5l1.7 1.7M5.5 13l1.7 1.7',
  calendar: 'M5 6.5A1.5 1.5 0 0 1 6.5 5h11A1.5 1.5 0 0 1 19 6.5v12A1.5 1.5 0 0 1 17.5 20h-11A1.5 1.5 0 0 1 5 18.5zM5 9.5h14M8.5 3.5v3M15.5 3.5v3',
  person: 'M12 12.5a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM5 20c0-3.3 3.1-5.5 7-5.5s7 2.2 7 5.5',
  close: 'M6 6l12 12M18 6 6 18',
  chevronDown: 'M6 9.5 12 15.5 18 9.5',
  chevronRight: 'M9.5 6 15.5 12 9.5 18',
  chevronLeft: 'M14.5 6 8.5 12 14.5 18',
  info: 'M12 11v6M12 7.5v.01M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z',
  flash: 'M13 3 5 13.5h6L10 21l8-10.5h-6L13 3Z',
  lock: 'M7 10.5V8a5 5 0 0 1 10 0v2.5M6 10.5h12a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1v-7a1 1 0 0 1 1-1Z',
  globe: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18ZM3.5 12h17M12 3c2.5 2.4 3.8 5.6 3.8 9s-1.3 6.6-3.8 9c-2.5-2.4-3.8-5.6-3.8-9S9.5 5.4 12 3Z',
  sun: 'M12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM12 2.5v2.5M12 19v2.5M4.2 4.2l1.8 1.8M18 18l1.8 1.8M2.5 12H5M19 12h2.5M4.2 19.8 6 18M18 6l1.8-1.8',
  moon: 'M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5Z',
  cloudOff: 'M7 18h10a4 4 0 0 0 .9-7.9A6 6 0 0 0 6.5 8.2M3 3l18 18',
  cloudDone: 'M7 18h10a4 4 0 0 0 .5-7.97A6 6 0 0 0 6 8.5 4.5 4.5 0 0 0 7 18ZM9.5 13.5 11 15l3-3.2',
  layers: 'M12 3 3 7.5 12 12l9-4.5L12 3ZM3 12l9 4.5L21 12M3 16.5 12 21l9-4.5',
  shield: 'M12 3 5 5.5v5c0 4.3 3 7.7 7 9 4-1.3 7-4.7 7-9v-5L12 3Z',
  trash: 'M5 7h14M9.5 7V5.5A1.5 1.5 0 0 1 11 4h2a1.5 1.5 0 0 1 1.5 1.5V7M7 7l.8 12a1.5 1.5 0 0 0 1.5 1.4h5.4a1.5 1.5 0 0 0 1.5-1.4L18 7',
  ear: 'M9 6.5A3 3 0 0 1 15 7c0 2-2 2.5-2 4M12 17.5v.01M6 12a6 6 0 1 1 9 5.2c-1 .6-1.5 1.3-1.5 2.3',
  bookmark: 'M7 4.5h10a1 1 0 0 1 1 1V20l-6-3.5L6 20V5.5a1 1 0 0 1 1-1Z',
  arrowUp: 'M12 19V5M12 5l-6 6M12 5l6 6',
  refresh: 'M19 12a7 7 0 1 1-2-4.9M19 4v3.5h-3.5',
  share: 'M12 3v12M12 3 8 7M12 3l4 4M6 11H5a1 1 0 0 0-1 1v7a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-7a1 1 0 0 0-1-1h-1',
  mic: 'M12 14a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v5a3 3 0 0 0 3 3ZM6 11a6 6 0 0 0 12 0M12 17.5V21',
  history: 'M12 8v4l3 2M3.5 12a8.5 8.5 0 1 0 2.5-6M6 6v3.5H2.5',
};

function Icon({ name, size = 22, stroke = 'currentColor', sw = 1.8, fill = 'none', style = {} }) {
  if (name === 'shutter') {
    return (
      <svg width={size} height={size} viewBox="0 0 24 24" style={style}>
        <circle cx="12" cy="12" r="9.2" fill="none" stroke={stroke} strokeWidth={sw}/>
        <circle cx="12" cy="12" r="6.3" fill={stroke}/>
      </svg>
    );
  }
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill={fill}
      stroke={stroke} strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round" style={style}>
      <path d={ICONS[name] || ''} />
    </svg>
  );
}

// ---------- Logo / mark ----------
function CiceroMark({ size = 28, color = 'var(--accent)' }) {
  // a scan-reticle fused with a classical column dot
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" fill="none" aria-hidden="true">
      <circle cx="16" cy="16" r="13" stroke={color} strokeWidth="2" opacity="0.5"/>
      <path d="M16 5v4M16 23v4M5 16h4M23 16h4" stroke={color} strokeWidth="2" strokeLinecap="round"/>
      <circle cx="16" cy="16" r="5.4" fill={color}/>
    </svg>
  );
}

function Logo({ size = 22, onCamera = false }) {
  const c = onCamera ? 'var(--glass-ink)' : 'var(--ink)';
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 9 }}>
      <CiceroMark size={size * 1.25} />
      <span className="cic-display" style={{
        fontSize: size, fontWeight: 600, color: c, letterSpacing: '-0.01em',
        lineHeight: 1,
      }}>Cicero</span>
    </div>
  );
}

// ---------- Confidence helpers ----------
function confLevel(score) {
  if (score >= 90) return { key: 'high', color: 'var(--conf-high)', label: 'Identifié' };
  if (score >= 70) return { key: 'mid', color: 'var(--conf-mid)', label: 'Probable' };
  return { key: 'low', color: 'var(--conf-low)', label: 'Incertain' };
}

// ---------- Button ----------
function Btn({ children, variant = 'primary', size = 'md', icon, iconRight, full, onClick, glass = false, style = {}, ariaLabel }) {
  const pads = { sm: '8px 14px', md: '13px 20px', lg: '16px 24px' };
  const fss = { sm: 14, md: 15.5, lg: 17 };
  const base = {
    display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: 9,
    fontFamily: 'var(--font-ui)', fontWeight: 600, fontSize: fss[size],
    padding: pads[size], borderRadius: 'var(--r-pill)', border: 'none',
    cursor: 'pointer', width: full ? '100%' : 'auto', lineHeight: 1.1,
    letterSpacing: '-0.01em', transition: 'transform .12s var(--ease-out), filter .15s',
    WebkitTapHighlightColor: 'transparent', userSelect: 'none',
  };
  const variants = {
    primary: { background: 'var(--accent)', color: 'var(--accent-ink)',
      boxShadow: '0 6px 18px -6px color-mix(in oklab, var(--accent) 70%, transparent)' },
    solid:   { background: 'var(--ink)', color: 'var(--bg)' },
    soft:    { background: 'var(--accent-soft)', color: 'var(--accent)' },
    ghost:   { background: 'transparent', color: onCameraColor(glass), border: `1.5px solid ${glass ? 'var(--glass-border)' : 'var(--hairline-strong)'}` },
    glass:   { color: 'var(--glass-ink)' },
  };
  const v = variants[variant] || variants.primary;
  const cls = 'cic-ui focusable' + (variant === 'glass' ? ' glass' : '');
  return (
    <button className={cls} aria-label={ariaLabel} onClick={onClick}
      style={{ ...base, ...v, ...style }}
      onMouseDown={e => e.currentTarget.style.transform = 'scale(0.97)'}
      onMouseUp={e => e.currentTarget.style.transform = 'scale(1)'}
      onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}>
      {icon && <Icon name={icon} size={size === 'lg' ? 21 : 18} />}
      {children}
      {iconRight && <Icon name={iconRight} size={size === 'lg' ? 21 : 18} />}
    </button>
  );
}
function onCameraColor(glass) { return glass ? 'var(--glass-ink)' : 'var(--ink)'; }

// ---------- Icon button (glass, round) ----------
function GlassIconBtn({ name, size = 48, iconSize = 22, onClick, ariaLabel, active = false, badge }) {
  return (
    <button className="glass focusable cic-ui" aria-label={ariaLabel} onClick={onClick}
      style={{
        width: size, height: size, borderRadius: 'var(--r-pill)', position: 'relative',
        display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
        color: active ? 'var(--accent)' : 'var(--glass-ink)', cursor: 'pointer',
        flexShrink: 0, padding: 0,
      }}>
      <Icon name={name} size={iconSize} sw={1.9} />
      {badge != null && (
        <span style={{
          position: 'absolute', top: -2, right: -2, minWidth: 18, height: 18, padding: '0 5px',
          background: 'var(--terra-500)', color: '#fff', borderRadius: 9, fontSize: 11,
          fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontFamily: 'var(--font-ui)', border: '2px solid var(--glass-bg)',
        }}>{badge}</span>
      )}
    </button>
  );
}

// ---------- Viewfinder brackets ----------
function Brackets({ color = 'rgba(255,255,255,0.92)', size = 250, active = true, locked = false, thickness = 3, len = 34 }) {
  const corner = (pos) => {
    const m = {
      tl: { top: 0, left: 0, borderTop: `${thickness}px solid`, borderLeft: `${thickness}px solid`, borderTopLeftRadius: 14 },
      tr: { top: 0, right: 0, borderTop: `${thickness}px solid`, borderRight: `${thickness}px solid`, borderTopRightRadius: 14 },
      bl: { bottom: 0, left: 0, borderBottom: `${thickness}px solid`, borderLeft: `${thickness}px solid`, borderBottomLeftRadius: 14 },
      br: { bottom: 0, right: 0, borderBottom: `${thickness}px solid`, borderRight: `${thickness}px solid`, borderBottomRightRadius: 14 },
    };
    return <div style={{ position: 'absolute', width: len, height: len, borderColor: color, ...m[pos] }} />;
  };
  return (
    <div style={{
      position: 'relative', width: size, height: size,
      animation: active && !locked ? 'cic-bracket-breathe 2.4s var(--ease-out) infinite' : 'none',
      transition: 'all .5s var(--ease-spring)',
      filter: 'drop-shadow(0 1px 3px rgba(0,0,0,0.4))',
    }}>
      {corner('tl')}{corner('tr')}{corner('bl')}{corner('br')}
    </div>
  );
}

// ---------- Detection pill (the key component) ----------
function DetectionPill({ state = 'searching', name = '', score = 0, place = '', onClick, compact = false }) {
  const lv = confLevel(score);
  if (state === 'searching') {
    return (
      <div className="glass cic-ui" style={pillWrap(false)}>
        <span style={{ ...dot, background: 'var(--glass-ink-muted)', position: 'relative' }}>
          <span style={{ position: 'absolute', inset: -4, borderRadius: '50%', border: '2px solid var(--glass-ink-muted)',
            borderTopColor: 'transparent', animation: 'cic-spin .8s linear infinite' }} />
        </span>
        <span style={{ color: 'var(--glass-ink)', fontWeight: 600, fontSize: 16 }}>Analyse en cours…</span>
      </div>
    );
  }
  return (
    <button className="glass cic-ui focusable" onClick={onClick} style={{ ...pillWrap(true), border: 'none' }}>
      <span style={{ ...dot, background: lv.color, boxShadow: `0 0 0 4px color-mix(in oklab, ${lv.color} 22%, transparent)` }} />
      <span style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', minWidth: 0 }}>
        {state === 'uncertain' && (
          <span style={{ fontSize: 11.5, fontWeight: 700, letterSpacing: '0.06em', textTransform: 'uppercase',
            color: lv.color, lineHeight: 1.1, marginBottom: 1 }}>Probablement</span>
        )}
        <span className="cic-display" style={{ color: 'var(--glass-ink)', fontWeight: 600, fontSize: 19,
          lineHeight: 1.1, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: 200 }}>{name}</span>
      </span>
      <span style={{ display: 'flex', alignItems: 'center', gap: 6, marginLeft: 2, paddingLeft: 10,
        borderLeft: '1px solid var(--glass-border)' }}>
        <ConfidenceBadge score={score} />
      </span>
      <Icon name="chevronRight" size={18} stroke="var(--glass-ink-muted)" style={{ marginLeft: 2, flexShrink: 0 }} />
    </button>
  );
}
const pillWrap = (clickable) => ({
  display: 'inline-flex', alignItems: 'center', gap: 12, padding: clickable ? '11px 14px 11px 16px' : '13px 20px',
  borderRadius: 'var(--r-pill)', cursor: clickable ? 'pointer' : 'default', maxWidth: 340,
});
const dot = { width: 11, height: 11, borderRadius: '50%', flexShrink: 0 };

// ---------- Confidence badge (compact %) ----------
function ConfidenceBadge({ score, onGlass = true }) {
  const lv = confLevel(score);
  return (
    <span className="cic-mono tnum" style={{
      fontSize: 14.5, fontWeight: 600, color: lv.color, lineHeight: 1, whiteSpace: 'nowrap',
    }}>{score}<span style={{ fontSize: 10, opacity: 0.8 }}>%</span></span>
  );
}

// ---------- Confidence meter (bar + label, used in sheet/components) ----------
function ConfidenceMeter({ score = 98, showLabel = true, width = 168 }) {
  const lv = confLevel(score);
  return (
    <div className="cic-ui" style={{ display: 'flex', flexDirection: 'column', gap: 6, width }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
        {showLabel && <span style={{ fontSize: 12.5, fontWeight: 600, color: lv.color, letterSpacing: '0.02em' }}>
          <span style={{ display: 'inline-block', width: 7, height: 7, borderRadius: '50%', background: lv.color, marginRight: 6 }} />
          Confiance · {lv.label}</span>}
        <span className="cic-mono tnum" style={{ fontSize: 13, fontWeight: 600, color: lv.color }}>{score}%</span>
      </div>
      <div style={{ height: 6, borderRadius: 99, background: 'var(--hairline)', overflow: 'hidden' }}>
        <div style={{ height: '100%', width: `${score}%`, borderRadius: 99,
          background: `linear-gradient(90deg, ${lv.color}, color-mix(in oklab, ${lv.color} 75%, white))`,
          transition: 'width .8s var(--ease-out)' }} />
      </div>
    </div>
  );
}

// ---------- Stat tile ----------
function StatTile({ icon, label, value, unit, accent = false }) {
  return (
    <div className="cic-ui" style={{
      background: accent ? 'var(--accent-soft)' : 'var(--surface-2)',
      border: `0.5px solid var(--hairline)`, borderRadius: 'var(--r-tile)',
      padding: '14px 14px 13px', display: 'flex', flexDirection: 'column', gap: 9, minWidth: 0,
    }}>
      <Icon name={icon} size={19} stroke={accent ? 'var(--accent)' : 'var(--ink-muted)'} sw={1.8} />
      <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <span className="cic-display tnum" style={{ fontSize: 21, fontWeight: 600, color: 'var(--ink)', lineHeight: 1, letterSpacing: '-0.01em' }}>
          {value}{unit && <span className="cic-ui" style={{ fontSize: 13, fontWeight: 600, color: 'var(--ink-muted)', marginLeft: 3 }}>{unit}</span>}
        </span>
        <span style={{ fontSize: 12, fontWeight: 500, color: 'var(--ink-faint)', letterSpacing: '0.01em' }}>{label}</span>
      </div>
    </div>
  );
}

// ---------- Suggested question chip ----------
function SuggestChip({ children, onClick, icon = 'sparkle' }) {
  return (
    <button className="cic-ui focusable" onClick={onClick} style={{
      display: 'inline-flex', alignItems: 'center', gap: 8, padding: '10px 15px',
      background: 'var(--surface)', border: '1px solid var(--hairline-strong)',
      borderRadius: 'var(--r-chip)', cursor: 'pointer', fontSize: 14, fontWeight: 500,
      color: 'var(--ink)', textAlign: 'left', lineHeight: 1.25, transition: 'all .15s',
    }}
      onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.background = 'var(--accent-soft)'; }}
      onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--hairline-strong)'; e.currentTarget.style.background = 'var(--surface)'; }}>
      <Icon name={icon} size={15} stroke="var(--accent)" />
      {children}
    </button>
  );
}

// ---------- Chat bubble ----------
function ChatBubble({ role = 'assistant', children, verified = false, sources }) {
  const isUser = role === 'user';
  if (role === 'typing') {
    return (
      <div style={{ display: 'flex', gap: 10, alignItems: 'flex-end' }}>
        <AssistantAvatar />
        <div className="surface-card" style={{ padding: '14px 16px', borderRadius: '4px 18px 18px 18px', display: 'flex', gap: 5 }}>
          {[0,1,2].map(i => <span key={i} style={{ width: 7, height: 7, borderRadius: '50%', background: 'var(--ink-faint)',
            animation: `cic-dots 1.2s ${i*0.15}s infinite ease-in-out` }} />)}
        </div>
      </div>
    );
  }
  return (
    <div style={{ display: 'flex', gap: 10, alignItems: 'flex-end', flexDirection: isUser ? 'row-reverse' : 'row' }}>
      {!isUser && <AssistantAvatar />}
      <div style={{ maxWidth: '78%', display: 'flex', flexDirection: 'column', gap: 6, alignItems: isUser ? 'flex-end' : 'flex-start' }}>
        <div className={isUser ? '' : 'surface-card'} style={{
          padding: '13px 16px', fontSize: 15.5, lineHeight: 1.5, color: isUser ? 'var(--accent-ink)' : 'var(--ink)',
          background: isUser ? 'var(--accent)' : undefined,
          borderRadius: isUser ? '18px 4px 18px 18px' : '4px 18px 18px 18px',
          fontFamily: 'var(--font-ui)', fontWeight: isUser ? 500 : 400, letterSpacing: '-0.005em',
        }}>{children}</div>
        {verified && !isUser && (
          <div className="cic-ui" style={{ display: 'flex', alignItems: 'center', gap: 6, paddingLeft: 4 }}>
            <Icon name="shield" size={13} stroke="var(--teal-600)" sw={2} />
            <span style={{ fontSize: 11.5, color: 'var(--ink-faint)', fontWeight: 500 }}>
              Vérifié{sources ? ` · ${sources}` : ''}</span>
          </div>
        )}
      </div>
    </div>
  );
}
function AssistantAvatar({ size = 30 }) {
  return (
    <div style={{ width: size, height: size, borderRadius: '50%', flexShrink: 0,
      background: 'linear-gradient(140deg, var(--teal-400), var(--teal-600))',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      boxShadow: '0 2px 8px -2px var(--teal-600)' }}>
      <Icon name="sparkle" size={16} stroke="#fff" sw={1.6} />
    </div>
  );
}

Object.assign(window, {
  Icon, CiceroMark, Logo, confLevel, Btn, GlassIconBtn, Brackets,
  DetectionPill, ConfidenceBadge, ConfidenceMeter, StatTile, SuggestChip,
  ChatBubble, AssistantAvatar,
});
