/* ============================================================
   CICERO — scene.jsx
   Camera viewfinder placeholder scenes + scanning overlays.
   Atmospheric CSS/SVG placeholders; replaceable with real
   photos via <image-slot>. Exported to window.
   ============================================================ */

// Palettes per time-of-day "tone"
const SCENE_TONES = {
  dawn:  { sky: ['#F4C9A0', '#E89B73', '#9C6F8E'], sun: 'rgba(255,221,160,0.65)', sunPos: '72% 28%', ground: '#5B4A52', sil: '#3A2E38' },
  day:   { sky: ['#A9D6E8', '#BFDCE6', '#D8E4DA'], sun: 'rgba(255,250,225,0.55)', sunPos: '24% 22%', ground: '#9CA98F', sil: '#5C6657' },
  dusk:  { sky: ['#33415C', '#7A5C77', '#D88A6A'], sun: 'rgba(255,180,120,0.5)', sunPos: '30% 70%', ground: '#2A2435', sil: '#191522' },
};

// Abstract monument silhouettes (placeholder — far/hazy)
function Silhouette({ kind = 'tower', color, height = '58%' }) {
  const common = { position: 'absolute', bottom: '14%', left: '50%', transform: 'translateX(-50%)', height, filter: 'drop-shadow(0 6px 24px rgba(0,0,0,0.25))' };
  const paths = {
    tower: (
      <svg viewBox="0 0 120 220" preserveAspectRatio="xMidYMax meet" style={{ ...common, aspectRatio: '120/220' }}>
        <path fill={color} d="M54 0h12l4 38 10 70 14 96h-22l-4-40h-24l-4 40H22l14-96 10-70 4-38h4Zm-8 120h28l-5-34H51l-5 34Zm5-50h18l-4-30h-10l-4 30Z"/>
        <path fill={color} d="M30 200h60v8H30z"/>
      </svg>
    ),
    dome: (
      <svg viewBox="0 0 200 180" preserveAspectRatio="xMidYMax meet" style={{ ...common, aspectRatio: '200/180' }}>
        <rect x="16" y="120" width="168" height="60" fill={color}/>
        <path fill={color} d="M100 24c34 0 56 30 56 64H44c0-34 22-64 56-64Z"/>
        <path fill={color} d="M96 4h8v22h-8z"/>
        <rect x="44" y="96" width="112" height="28" fill={color}/>
      </svg>
    ),
    arch: (
      <svg viewBox="0 0 200 150" preserveAspectRatio="xMidYMax meet" style={{ ...common, aspectRatio: '200/150' }}>
        <path fill={color} d="M20 10h160v140h-44V86c0-20-14-34-36-34s-36 14-36 34v64H20V10Z"/>
      </svg>
    ),
    statue: (
      <svg viewBox="0 0 120 230" preserveAspectRatio="xMidYMax meet" style={{ ...common, aspectRatio: '120/230' }}>
        <rect x="38" y="150" width="44" height="80" fill={color}/>
        <rect x="30" y="138" width="60" height="16" fill={color}/>
        <path fill={color} d="M60 30c9 0 15 7 15 16 0 6-3 10-3 16l6 60H46l6-60c0-6-3-10-3-16 0-9 6-16 11-16Z"/>
        <path fill={color} d="M60 8l5 22h-10l5-22Zm0 6l-9-3 9 14 9-14-9 3Z"/>
        <circle cx="60" cy="36" r="7" fill={color}/>
      </svg>
    ),
  };
  return paths[kind] || paths.tower;
}

function CameraScene({ tone = 'dawn', monument = 'tower', slotId, blur = 0, style = {}, children }) {
  const t = SCENE_TONES[tone] || SCENE_TONES.dawn;
  return (
    <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', background: '#000', ...style }}>
      {/* atmospheric placeholder */}
      <div style={{ position: 'absolute', inset: 0, filter: blur ? `blur(${blur}px)` : 'none', transform: blur ? 'scale(1.06)' : 'none' }}>
        <div style={{ position: 'absolute', inset: 0,
          background: `linear-gradient(180deg, ${t.sky[0]} 0%, ${t.sky[1]} 46%, ${t.sky[2]} 100%)` }} />
        <div style={{ position: 'absolute', inset: 0,
          background: `radial-gradient(closest-side at ${t.sunPos}, ${t.sun}, transparent 60%)` }} />
        {/* ground haze */}
        <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, height: '34%',
          background: `linear-gradient(180deg, transparent, ${t.ground})`, opacity: 0.9 }} />
        <Silhouette kind={monument} color={t.sil} />
        {/* faint distant buildings */}
        <div style={{ position: 'absolute', bottom: '14%', left: 0, right: 0, height: 46, opacity: 0.4,
          background: `repeating-linear-gradient(90deg, ${t.sil} 0 14px, transparent 14px 30px)`,
          WebkitMaskImage: 'linear-gradient(180deg, transparent, #000)' }} />
      </div>
      {/* user-replaceable real photo */}
      {slotId && (
        <image-slot id={slotId} fit="cover" placeholder="Déposez une photo du monument"
          style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', display: 'block' }}></image-slot>
      )}
      {/* lens vignette */}
      <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none',
        boxShadow: 'inset 0 0 120px 30px rgba(0,0,0,0.34)' }} />
      {children}
    </div>
  );
}

// Scanning sweep line + grid that appears during "searching"
function ScanOverlay({ active = true }) {
  if (!active) return null;
  return (
    <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none', overflow: 'hidden' }}>
      <div style={{ position: 'absolute', left: '12%', right: '12%', top: '30%', height: '40%' }}>
        <div style={{ position: 'absolute', left: 0, right: 0, height: 2,
          background: 'linear-gradient(90deg, transparent, rgba(43,191,174,0.9), transparent)',
          boxShadow: '0 0 16px 2px rgba(43,191,174,0.6)',
          animation: 'cic-scan-sweep 2.2s var(--ease-out) infinite' }} />
      </div>
    </div>
  );
}

// Detection ripple at a screen point
function DetectionPing({ x = '50%', y = '46%', color = 'var(--teal-400)' }) {
  return (
    <div style={{ position: 'absolute', left: x, top: y, transform: 'translate(-50%,-50%)', pointerEvents: 'none' }}>
      <div style={{ position: 'relative', width: 14, height: 14 }}>
        <span style={{ position: 'absolute', inset: 0, borderRadius: '50%', border: `2px solid ${color}`,
          animation: 'cic-pulse-ring 1.8s var(--ease-out) infinite' }} />
        <span style={{ position: 'absolute', inset: 0, borderRadius: '50%', border: `2px solid ${color}`,
          animation: 'cic-pulse-ring 1.8s var(--ease-out) .9s infinite' }} />
        <span style={{ position: 'absolute', inset: 4, borderRadius: '50%', background: color,
          boxShadow: `0 0 12px ${color}` }} />
      </div>
    </div>
  );
}

Object.assign(window, { SCENE_TONES, Silhouette, CameraScene, ScanOverlay, DetectionPing });
