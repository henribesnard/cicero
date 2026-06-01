/* ============================================================
   CICERO — direction.jsx
   Visual-direction planches for the canvas:
   Manifesto · Palette · Typography · Component library
   Each wraps itself in a data-theme scope so tokens resolve.
   ============================================================ */

function Planche({ theme = 'light', pad = 32, w = 820, children, bg }) {
  return (
    <div data-theme={theme} style={{ width: w, background: bg || 'var(--bg)', padding: pad,
      fontFamily: 'var(--font-ui)', color: 'var(--ink)', borderRadius: 2 }}>
      {children}
    </div>
  );
}
function PLabel({ children }) {
  return <div className="cic-ui" style={{ fontSize: 12, fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase',
    color: 'var(--ink-faint)', marginBottom: 16 }}>{children}</div>;
}

/* ---------- Manifesto ---------- */
function DirectionManifesto() {
  const principles = [
    { icon: 'scan', t: 'La caméra d\'abord', d: "L'image plein écran est l'interface. L'UI se réduit à des surfaces de verre dépoli qui ne masquent jamais la vue." },
    { icon: 'shield', t: 'La confiance, toujours visible', d: "Chaque résultat affiche son score. On dit « probablement » quand on doute — jamais de fausse assurance." },
    { icon: 'sun', t: 'Lisible au soleil', d: "Contrastes renforcés, tailles confortables, surfaces opaques sous le texte. Utilisable d'une seule main, en plein jour." },
    { icon: 'globe', t: 'Chaleureux & culturel', d: "Une serif éditoriale et des neutres « pierre » donnent l'âme d'un guide érudit, pas d'une app IA générique." },
  ];
  return (
    <Planche w={860} pad={44}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 26 }}>
        <CiceroMark size={40} />
        <span className="cic-display" style={{ fontSize: 34, fontWeight: 600, letterSpacing: '-0.01em' }}>Cicero</span>
      </div>
      <h1 className="cic-display" style={{ fontSize: 46, lineHeight: 1.06, fontWeight: 500, letterSpacing: '-0.025em', margin: 0, maxWidth: 680 }}>
        Le scanner de monuments qui se prend pour un <span style={{ fontStyle: 'italic', color: 'var(--teal-600)' }}>cicérone</span>.
      </h1>
      <p className="cic-ui" style={{ fontSize: 17.5, lineHeight: 1.6, color: 'var(--ink-muted)', maxWidth: 620, marginTop: 18, textWrap: 'pretty' }}>
        Un <i>cicérone</i> est ce guide érudit qui montrait jadis les antiquités aux voyageurs — nommé d'après Cicéron pour son éloquence.
        Cicero pointe, identifie en moins d'une seconde, raconte, et reste à portée de pouce. La direction visuelle traduit cette promesse.
      </p>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginTop: 34 }}>
        {principles.map((p, i) => (
          <div key={i} style={{ display: 'flex', gap: 14, padding: 20, background: 'var(--surface)', borderRadius: 'var(--r-card)',
            border: '0.5px solid var(--hairline)' }}>
            <div style={{ width: 44, height: 44, borderRadius: 12, background: 'var(--accent-soft)', flexShrink: 0,
              display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Icon name={p.icon} size={22} stroke="var(--accent)" sw={1.9} /></div>
            <div>
              <div className="cic-ui" style={{ fontSize: 16.5, fontWeight: 700, marginBottom: 5 }}>{p.t}</div>
              <div className="cic-ui" style={{ fontSize: 14, lineHeight: 1.5, color: 'var(--ink-muted)', textWrap: 'pretty' }}>{p.d}</div>
            </div>
          </div>
        ))}
      </div>
    </Planche>
  );
}

/* ---------- Palette ---------- */
function Swatch({ c, name, hex, ink = '#fff', big = false }) {
  return (
    <div style={{ flex: big ? 1.4 : 1 }}>
      <div style={{ height: big ? 86 : 64, background: c, borderRadius: 14, border: '0.5px solid rgba(0,0,0,0.08)',
        display: 'flex', alignItems: 'flex-end', padding: 10 }}>
        <span className="cic-mono" style={{ fontSize: 11, color: ink, fontWeight: 500, opacity: 0.92 }}>{hex}</span>
      </div>
      <div className="cic-ui" style={{ fontSize: 12.5, fontWeight: 600, marginTop: 7, color: 'var(--ink)' }}>{name}</div>
    </div>
  );
}
function PalettePlanche() {
  return (
    <Planche w={860} pad={40}>
      <PLabel>Palette</PLabel>
      <h2 className="cic-display" style={{ fontSize: 26, fontWeight: 500, margin: '0 0 6px', letterSpacing: '-0.01em' }}>
        Sarcelle &amp; pierre</h2>
      <p className="cic-ui" style={{ fontSize: 14.5, color: 'var(--ink-muted)', maxWidth: 600, margin: '0 0 26px', lineHeight: 1.5, textWrap: 'pretty' }}>
        Un seul accent : le <b>teal/sarcelle</b> — couleur de la patine du bronze, de la mer et des dômes oxydés. Calme, culturel, très lisible.
        Les neutres tirent vers la <b>pierre chaude</b> plutôt que le gris froid. Le <b>terracotta</b> et l'<b>ocre</b> n'apparaissent que pour la chaleur et les niveaux de confiance.
      </p>

      <div style={{ fontSize: 12.5, fontWeight: 700, color: 'var(--ink-muted)', marginBottom: 10 }}>Accent · Sarcelle</div>
      <div style={{ display: 'flex', gap: 10, marginBottom: 24 }}>
        <Swatch c="var(--teal-700)" name="Teal 700" hex="#075E56" />
        <Swatch c="var(--teal-600)" name="Teal 600 · primaire" hex="#0A7D72" big />
        <Swatch c="var(--teal-500)" name="Teal 500" hex="#0E9B8E" />
        <Swatch c="var(--teal-400)" name="Teal 400 · sombre" hex="#2BBFAE" ink="#06322E" />
        <Swatch c="var(--teal-50)" name="Teal 50" hex="#E6F6F3" ink="#075E56" />
      </div>

      <div style={{ fontSize: 12.5, fontWeight: 700, color: 'var(--ink-muted)', marginBottom: 10 }}>Chaud · Terracotta &amp; ocre</div>
      <div style={{ display: 'flex', gap: 10, marginBottom: 24 }}>
        <Swatch c="var(--terra-500)" name="Terracotta" hex="#D67A48" />
        <Swatch c="var(--terra-600)" name="Terracotta 600" hex="#B85F33" />
        <Swatch c="var(--ochre-500)" name="Ocre" hex="#C99A3A" />
        <Swatch c="var(--ochre-400)" name="Ocre 400" hex="#E0B24A" ink="#3a2c08" />
      </div>

      <div style={{ display: 'flex', gap: 28 }}>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 12.5, fontWeight: 700, color: 'var(--ink-muted)', marginBottom: 10 }}>Neutres · Clair (pierre)</div>
          <div style={{ display: 'flex', gap: 8 }}>
            <Swatch c="var(--bg)" name="Sable" hex="#F4F0E8" ink="#1E1B16" />
            <Swatch c="var(--surface)" name="Surface" hex="#FFFFFF" ink="#1E1B16" />
            <Swatch c="var(--ink-muted)" name="Encre douce" hex="#6E675B" />
            <Swatch c="var(--ink)" name="Encre" hex="#1E1B16" />
          </div>
        </div>
        <div data-theme="dark" style={{ flex: 1, background: 'var(--bg)', padding: 16, borderRadius: 14, marginTop: -16 }}>
          <div style={{ fontSize: 12.5, fontWeight: 700, color: 'var(--ink-muted)', marginBottom: 10 }}>Neutres · Sombre (charbon chaud)</div>
          <div style={{ display: 'flex', gap: 8 }}>
            <Swatch c="var(--bg)" name="Charbon" hex="#16140F" />
            <Swatch c="var(--surface)" name="Surface" hex="#211E18" />
            <Swatch c="var(--ink-muted)" name="Encre douce" hex="#A79E8D" ink="#16140F" />
            <Swatch c="var(--ink)" name="Encre" hex="#F4F0E7" ink="#16140F" />
          </div>
        </div>
      </div>

      <div style={{ fontSize: 12.5, fontWeight: 700, color: 'var(--ink-muted)', margin: '24px 0 10px' }}>Sémantique de confiance</div>
      <div style={{ display: 'flex', gap: 12 }}>
        {[['var(--conf-high)', 'Identifié ≥ 90 %', '#fff'], ['var(--conf-mid)', 'Probable 70–89 %', '#3a2c08'], ['var(--conf-low)', 'Incertain < 70 %', '#fff']].map(([c, l, ink], i) => (
          <div key={i} style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 10, padding: '12px 16px', background: c, borderRadius: 12 }}>
            <span style={{ width: 10, height: 10, borderRadius: '50%', background: ink, opacity: 0.9 }} />
            <span className="cic-ui" style={{ fontSize: 14, fontWeight: 600, color: ink }}>{l}</span>
          </div>
        ))}
      </div>
    </Planche>
  );
}

/* ---------- Typography ---------- */
function TypePlanche() {
  return (
    <Planche w={860} pad={40}>
      <PLabel>Typographie</PLabel>
      <div style={{ display: 'flex', gap: 40 }}>
        <div style={{ flex: 1 }}>
          <div className="cic-ui" style={{ fontSize: 13, fontWeight: 700, color: 'var(--teal-600)', marginBottom: 4 }}>Display · Newsreader</div>
          <div className="cic-ui" style={{ fontSize: 13, color: 'var(--ink-muted)', marginBottom: 16 }}>Serif éditoriale — noms de monuments, titres, gros chiffres</div>
          <div className="cic-display" style={{ fontSize: 52, fontWeight: 500, lineHeight: 1.02, letterSpacing: '-0.02em' }}>Tour Eiffel</div>
          <div className="cic-display" style={{ fontSize: 30, fontWeight: 500, fontStyle: 'italic', color: 'var(--teal-600)', marginTop: 8 }}>cicérone</div>
          <div className="cic-display" style={{ fontSize: 15, color: 'var(--ink-muted)', marginTop: 16, letterSpacing: '0.04em' }}>
            Aa Bb Cc · àâçéèêëîïô · 0123456789</div>
        </div>
        <div style={{ width: 1, background: 'var(--hairline)' }} />
        <div style={{ flex: 1 }}>
          <div className="cic-ui" style={{ fontSize: 13, fontWeight: 700, color: 'var(--teal-600)', marginBottom: 4 }}>UI · Hanken Grotesk</div>
          <div className="cic-ui" style={{ fontSize: 13, color: 'var(--ink-muted)', marginBottom: 16 }}>Grotesque humaniste — libellés, corps, boutons (multilingue)</div>
          <div className="cic-ui" style={{ fontSize: 22, fontWeight: 700 }}>Pointez. Découvrez.</div>
          <div className="cic-ui" style={{ fontSize: 16, fontWeight: 500, marginTop: 8 }}>Touchez la pastille pour la fiche complète.</div>
          <div className="cic-ui" style={{ fontSize: 14, fontWeight: 400, color: 'var(--ink-muted)', marginTop: 8, lineHeight: 1.5 }}>
            Erigée pour l'Exposition universelle de 1889, la « Dame de fer ».</div>
          <div style={{ display: 'flex', gap: 10, marginTop: 16, alignItems: 'baseline' }}>
            <span className="cic-mono" style={{ fontSize: 13, fontWeight: 700, color: 'var(--ink-muted)' }}>Mono · Geist Mono</span>
            <span className="cic-mono tnum" style={{ fontSize: 20, fontWeight: 600, color: 'var(--teal-600)' }}>98%</span>
            <span className="cic-mono" style={{ fontSize: 13, color: 'var(--ink-faint)' }}>48.8584° N</span>
          </div>
        </div>
      </div>
      <div style={{ display: 'flex', gap: 10, marginTop: 28, flexWrap: 'wrap' }}>
        {[['Display 38–52', 'cic-display', 38, 500], ['Titre 30', 'cic-display', 30, 500], ['Corps 16', 'cic-ui', 16, 400],
          ['Libellé 14', 'cic-ui', 14, 600], ['Légende 12', 'cic-ui', 12, 600]].map(([l, cls, sz, w], i) => (
          <div key={i} style={{ padding: '8px 14px', background: 'var(--surface)', borderRadius: 10, border: '0.5px solid var(--hairline)' }}>
            <span className={cls} style={{ fontSize: sz / 1.6, fontWeight: w, marginRight: 8 }}>Ag</span>
            <span className="cic-ui" style={{ fontSize: 12, color: 'var(--ink-faint)' }}>{l}</span>
          </div>
        ))}
      </div>
    </Planche>
  );
}

/* ---------- Component library ---------- */
function CompBlock({ title, children, dark = false, span = 1 }) {
  return (
    <div style={{ gridColumn: `span ${span}`, background: dark ? 'transparent' : 'var(--surface)', borderRadius: 'var(--r-card)',
      border: '0.5px solid var(--hairline)', padding: 20, overflow: 'hidden' }}>
      <div className="cic-ui" style={{ fontSize: 12.5, fontWeight: 700, letterSpacing: '0.04em', color: 'var(--ink-faint)',
        textTransform: 'uppercase', marginBottom: 16 }}>{title}</div>
      {children}
    </div>
  );
}
// mini camera strip so glass components read correctly
function GlassStage({ children, tone = 'dawn', h = 'auto', pad = 18 }) {
  return (
    <div style={{ position: 'relative', borderRadius: 16, overflow: 'hidden', padding: pad, minHeight: h === 'auto' ? 0 : h,
      display: 'flex', flexWrap: 'wrap', gap: 12, alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ position: 'absolute', inset: 0 }}><CameraScene tone={tone} monument="tower" /></div>
      <div style={{ position: 'relative', display: 'flex', flexWrap: 'wrap', gap: 12, alignItems: 'center', justifyContent: 'center' }}>{children}</div>
    </div>
  );
}
function ComponentsPlanche() {
  return (
    <Planche w={900} pad={36}>
      <PLabel>Bibliothèque de composants</PLabel>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <CompBlock title="Pastille de détection — 3 états" span={2}>
          <GlassStage tone="dawn">
            <DetectionPill state="searching" />
            <DetectionPill state="recognized" name="Tour Eiffel" score={98} />
            <DetectionPill state="uncertain" name="Basilique Saint-Denis" score={71} />
          </GlassStage>
        </CompBlock>

        <CompBlock title="Boutons">
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10, alignItems: 'center' }}>
            <Btn variant="primary">Autoriser</Btn>
            <Btn variant="soft">En savoir plus</Btn>
            <Btn variant="ghost">Plus tard</Btn>
            <Btn variant="primary" icon="download" size="sm">Obtenir</Btn>
          </div>
        </CompBlock>

        <CompBlock title="Boutons sur verre">
          <GlassStage tone="dusk">
            <GlassIconBtn name="book" badge={4} />
            <GlassIconBtn name="flash" />
            <GlassIconBtn name="sliders" />
            <Btn variant="glass" icon="share">Partager</Btn>
          </GlassStage>
        </CompBlock>

        <CompBlock title="Confiance">
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <ConfidenceMeter score={98} />
            <ConfidenceMeter score={82} />
            <ConfidenceMeter score={64} />
          </div>
        </CompBlock>

        <CompBlock title="Tuiles de statistiques">
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
            <StatTile icon="calendar" label="Achèvement" value="1889" accent />
            <StatTile icon="ruler" label="Hauteur" value="330" unit="m" />
            <StatTile icon="person" label="Ingénieur" value="G. Eiffel" />
            <StatTile icon="layers" label="Étages" value="3" />
          </div>
        </CompBlock>

        <CompBlock title="Bulles de chat" span={2}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12, maxWidth: 460 }}>
            <ChatBubble role="user">Pourquoi a-t-elle failli être détruite&nbsp;?</ChatBubble>
            <ChatBubble role="assistant" verified sources="3 sources">Le permis n'autorisait la tour que pour 20&nbsp;ans. Elle fut sauvée par son antenne radio.</ChatBubble>
            <ChatBubble role="typing" />
          </div>
        </CompBlock>

        <CompBlock title="Questions suggérées">
          <div style={{ display: 'flex', flexDirection: 'column', gap: 9 }}>
            <SuggestChip>Combien pèse la structure&nbsp;?</SuggestChip>
            <SuggestChip>Que voit-on au sommet&nbsp;?</SuggestChip>
          </div>
        </CompBlock>

        <CompBlock title="Repères de visée & contrôles">
          <div style={{ display: 'flex', alignItems: 'center', gap: 24, flexWrap: 'wrap' }}>
            <div style={{ position: 'relative', width: 96, height: 96, background: 'var(--bg-2)', borderRadius: 12,
              display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Brackets size={76} color="var(--teal-500)" locked thickness={3} len={22} />
            </div>
            <Segmented value="light" onChange={() => {}} options={[{ v: 'light', label: 'Clair', icon: 'sun' }, { v: 'dark', label: 'Sombre', icon: 'moon' }, { v: 'auto', label: 'Auto', icon: 'refresh' }]} />
            <Toggle value={true} onChange={() => {}} label="demo" />
          </div>
        </CompBlock>
      </div>
    </Planche>
  );
}

Object.assign(window, { Planche, DirectionManifesto, PalettePlanche, TypePlanche, ComponentsPlanche, GlassStage });
