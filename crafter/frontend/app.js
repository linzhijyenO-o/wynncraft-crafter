'use strict';

const $ = (sel) => document.querySelector(sel);
const el = (tag, cls, html) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (html !== undefined) n.innerHTML = html;
  return n;
};
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const fmt = (n) => (typeof n === 'number' ? (Number.isInteger(n) ? String(n) : String(Math.round(n * 10) / 10)) : String(n));
const sameArr = (a, b) => a.length === b.length && a.every((x, i) => Number(x) === Number(b[i]));

const TIER_COLORS_DARK = ['#ffffff', '#ffdc50', '#ff50e8', '#50fdff'];
const TIER_COLORS_LIGHT = ['#9aa0a6', '#a8760c', '#c2185b', '#00838f'];
const PRESET_KEY = 'crafter-presets-v1';
const LANG_KEY = 'crafter-lang';

// ---------------------------------------------------------------- 文案
const I18N = {
  en: {
    'app.title': 'Wynncraft Crafting Calculator',
    'app.subtitle': 'Custom item crafting · 6-ingredient search',
    'app.ingredients': '{n} ingredients in the database',
    'ui.type': 'Item type',
    'ui.professions': 'Professions: {list}',
    'ui.base': 'Base durability (6 tiers · per item type)',
    'ui.applyAll': 'Apply to all types',
    'ui.applied': 'Applied ✓',
    'ui.tier': 'Tier',
    'ui.tierN': 'T{n}',
    'ui.current': 'current {v}',
    'ui.baseHint': 'Final durability = base durability of the chosen tier + sum of ingredient durability modifiers (not affected by adjacency). Negative ingredients cost durability, a few positive ones add it.',
    'ui.minDur': 'Minimum durability',
    'ui.minDurC': 'Minimum duration',
    'ui.minDurPh': 'e.g. 300, blank = no limit',
    'ui.minDurPhC': 'e.g. 400, blank = no limit',
    'ui.baseDur': 'Base duration (consumables)',
    'ui.baseDurHint': 'Final duration = base + sum of ingredient duration modifiers',
    'ui.minCharges': 'Minimum charges',
    'ui.minChargesPh': 'e.g. 5, blank = no limit',
    'ui.baseCharges': 'Base charges (consumables)',
    'ui.baseChargesHint': 'Final charges = base + sum of ingredient charge modifiers (base defaults to 3)',
    'ui.points': 'Skill requirements (per skill, blank = no limit)',
    'ui.targets': 'Target IDs (multi-select)',
    'ui.searchId': 'Search IDs, e.g. health / spell…',
    'ui.compare': 'Compare',
    'ui.cmpMax': 'Range max',
    'ui.cmpMin': 'Range min',
    'ui.topN': 'Top N',
    'ui.effort': 'Search effort',
    'ui.fast': 'Fast',
    'ui.normal': 'Normal',
    'ui.thorough': 'Thorough (slow)',
    'ui.allowDupes': 'Allow duplicates',
    'ui.search': 'Search',
    'ui.searching': 'Searching…',
    'ui.results': 'Results',
    'ui.bans': 'Banned ingredients',
    'ui.banPlaceholder': 'Search ingredient…',
    'ui.noBan': 'No ingredients banned',
    'ui.noMatch': 'No match',
    'ui.more': '{n} more — keep typing',
    'ui.presets': 'Presets',
    'ui.presetName': 'Preset name',
    'ui.export': 'Save & export',
    'ui.codePlaceholder': 'Click the button above to generate a code',
    'ui.copy': 'Copy',
    'ui.clear': 'Clear',
    'ui.noPreset': 'No saved presets',
    'ui.load': 'Load',
    'ui.del': 'Del',
    'ui.importPlaceholder': 'Paste a code to import',
    'ui.how': 'How it works',
    'ui.weightHint': 'Score = Σ weight × value ÷ reachable cap. Weight 0 = constraint only, negative = lower is better.',
    'ui.weightHintZero': 'All weights are 0 — nothing to rank by. Give at least one non-zero weight.',
    'ui.pickTarget': 'Pick at least one target ID',
    'ui.noTarget': 'No target IDs yet',
    'ui.remove': 'Remove',
    'ui.restore': 'Click to restore',
    'ui.weight': 'Weight (0 or negative allowed)',
    'ui.min': 'Min',
    'ui.max': 'Max',
    'ui.maxHint': 'Upper bound on this ID (blank = no limit)',
    'calc.1': 'Adjacency: each cell receives the percentages granted by the other cells depending on relative position (left/right/above/under, touching, not touching) — the same 5×3 grid as the official item guide.',
    'calc.2': 'IDs and skill requirements: Σ floor(value × (1 + bonus/100)); negatives round down (further negative).',
    'calc.3': 'Durability: base durability (item type + tier) + Σ ingredient durability modifiers, not affected by adjacency.',
    'calc.4': 'Requirements: the five skills are summed separately, each compared with its own limit.',
    'calc.5': 'Multiple targets: Σ weight × value ÷ reachable cap, with an optional lower bound per ID.',
    'res.summary': '{n} results · {c} candidates · {s} layouts · {ms} ms',
    'res.durability': 'Durability {v}',
    'res.time': 'Duration {v}',
    'res.charges': 'Charges {v}',
    'res.skills': 'Skills {list}',
    'res.noResults': 'No results',
    'res.durMinus': 'Durability = base {b} (tier {t}) − {m} = {d}',
    'res.durPlus': 'Durability = base {b} (tier {t}) + {m} = {d}',
    'res.durationLine': 'Duration = base {b} + modifier {m} = {d}',
    'res.chargesLine': 'Charges = base {b} + modifier {m} = {d}',
    'res.empty': 'no IDs',
    'res.noIds': 'No IDs',
    'err.no_candidates': 'No usable ingredients',
    'err.all_zero_weights': 'All target weights are 0 — nothing to rank by',
    'err.no_feasible': 'No combination matches the constraints — try relaxing durability / points / ID minimums',
    'msg.saved': 'Saved "{name}" · {n} chars',
    'msg.copied': 'Copied to clipboard',
    'msg.selectCopy': 'Selected — press Ctrl+C',
    'msg.badCode': 'Unrecognized code',
    'msg.imported': 'Imported: {n} target IDs{ban}',
    'msg.importedBan': ', {m} banned',
    'msg.importFail': 'Import failed: {e}',
    'msg.initFail': 'Init failed: {e}',
    'msg.reqFail': 'Request failed: {e}',
    'theme.dark': '🌙 Night',
    'theme.light': '☀️ Day',
  },
  zh: {
    'app.title': '自制装备制作器',
    'app.subtitle': '功能一 · 6 原料配方搜索',
    'app.ingredients': '原料库 {n} 个',
    'ui.type': '自制物品种类',
    'ui.professions': '可用职业：{list}',
    'ui.base': '基础耐久（6 档 · 按物品种类）',
    'ui.applyAll': '应用到所有种类',
    'ui.applied': '已应用 ✓',
    'ui.tier': '使用档位',
    'ui.tierN': '{n} 档',
    'ui.current': '当前 {v}',
    'ui.baseHint': '成品耐久 = 该档基础耐久 + 6 个原料的耐久修正之和（不受相邻加成影响）。多数原料会扣耐久，少数正数原料补耐久。',
    'ui.minDur': '装备最低耐久',
    'ui.minDurC': '最低持续时间',
    'ui.minDurPh': '例如 300，不限留空',
    'ui.minDurPhC': '例如 400，不限留空',
    'ui.baseDur': '基础持续时间（消耗品）',
    'ui.baseDurHint': '成品时间 = 基础值 + 6 个原料的时长修正之和',
    'ui.minCharges': '最低使用次数',
    'ui.minChargesPh': '例如 5，不限留空',
    'ui.baseCharges': '基础使用次数（消耗品）',
    'ui.baseChargesHint': '成品次数 = 基础值 + 6 个原料的次数修正之和（基础默认 3）',
    'ui.points': '点数上限（五项分别限制，留空不限）',
    'ui.targets': '目标词条（可多选）',
    'ui.searchId': '搜索词条，例如 health / spell…',
    'ui.compare': '比较口径',
    'ui.cmpMax': '范围最高值',
    'ui.cmpMin': '范围最低值',
    'ui.topN': '返回前 n 条',
    'ui.effort': '搜索强度',
    'ui.fast': '快',
    'ui.normal': '标准',
    'ui.thorough': '彻底（慢）',
    'ui.allowDupes': '允许重复原料',
    'ui.search': '开始搜索',
    'ui.searching': '搜索中…',
    'ui.results': '搜索结果',
    'ui.bans': '禁用素材',
    'ui.banPlaceholder': '搜索素材名…',
    'ui.noBan': '没有禁用任何素材',
    'ui.noMatch': '没有匹配的素材',
    'ui.more': '还有 {n} 条，继续输入缩小范围',
    'ui.presets': '预设配置',
    'ui.presetName': '预设名称',
    'ui.export': '生成并保存',
    'ui.codePlaceholder': '点上面按钮生成代码，可复制保存',
    'ui.copy': '复制代码',
    'ui.clear': '清空',
    'ui.noPreset': '还没有保存的预设',
    'ui.load': '载入',
    'ui.del': '删',
    'ui.importPlaceholder': '粘贴代码，自动识别导入',
    'ui.how': '计算口径',
    'ui.weightHint': '排名 = Σ 权重 × 数值 ÷ 该词条可达上限；权重 0 = 只保留下限约束，负数 = 越低越好。',
    'ui.weightHintZero': '所有目标权重都是 0：只做约束筛选，没有排序依据（至少给一个非 0 权重）。',
    'ui.pickTarget': '请至少选一个目标词条',
    'ui.noTarget': '还没有选目标词条',
    'ui.remove': '移除',
    'ui.restore': '点击恢复',
    'ui.weight': '权重（可为 0 或负数）',
    'ui.min': '下限',
    'ui.max': '上限',
    'ui.maxHint': '该词条的上界（留空不限）',
    'calc.1': '相邻加成：每格受到其它格按相对位置授予的百分比之和（左/右/上/下、相邻、不相邻），与官方图鉴的 5×3 效果网格一致。',
    'calc.2': '词条与点数：Σ floor(数值 × (1 + 加成/100))，向下取整（负数往更小的方向）。',
    'calc.3': '耐久：基础耐久（种类 + 档位）+ Σ 原料耐久修正，不受相邻加成影响。',
    'calc.4': '点数：五项属性需求分别累加，各自与自己的上限比较。',
    'calc.5': '多目标：Σ 权重 × 数值 ÷ 该词条可达上限，每条可单独设下限。',
    'res.summary': '{n} 条 · 候选 {c} · 评估 {s} 种排布 · {ms} ms',
    'res.durability': '耐久 {v}',
    'res.time': '时间 {v}',
    'res.charges': '次数 {v}',
    'res.skills': '点数 {list}',
    'res.noResults': '没有结果',
    'res.durMinus': '耐久 = 基础 {b}（{t} 档） − 消耗 {m} = {d}',
    'res.durPlus': '耐久 = 基础 {b}（{t} 档） + 补正 {m} = {d}',
    'res.durationLine': '时间 = 基础 {b} + 原料修正 {m} = {d}',
    'res.chargesLine': '次数 = 基础 {b} + 原料修正 {m} = {d}',
    'res.empty': '无词条',
    'res.noIds': '无词条',
    'err.no_candidates': '没有可用原料',
    'err.all_zero_weights': '所有目标词条的权重都是 0，无法排序',
    'err.no_feasible': '没有满足约束的组合，试试放宽耐久 / 点数 / 词条下限',
    'msg.saved': '已保存「{name}」，代码 {n} 字符',
    'msg.copied': '已复制到剪贴板',
    'msg.selectCopy': '已选中，按 Ctrl+C 复制',
    'msg.badCode': '无法识别的代码',
    'msg.imported': '已导入：{n} 个目标词条{ban}',
    'msg.importedBan': '，禁用 {m} 个素材',
    'msg.importFail': '导入失败：{e}',
    'msg.initFail': '初始化失败：{e}',
    'msg.reqFail': '请求失败：{e}',
    'theme.dark': '🌙 夜晚',
    'theme.light': '☀️ 白天',
  },
};

function t(key, params) {
  const dict = I18N[state.lang] || I18N.en;
  let s = dict[key];
  if (s === undefined) s = I18N.en[key] !== undefined ? I18N.en[key] : key;
  if (params) {
    Object.keys(params).forEach((k) => { s = s.split('{' + k + '}').join(String(params[k])); });
  }
  return s;
}

// ---------------------------------------------------------------- 状态
const state = {
  lang: document.documentElement.getAttribute('data-lang') === 'zh' ? 'zh' : 'en',
  meta: null,
  labels: {},
  baseTable: {},
  baseTier: {},
  selected: [],
  weights: {},
  mins: {},
  maxs: {},
  disabled: [],
  busy: false,
  last: null,
};

function applyI18n() {
  document.querySelectorAll('[data-i18n]').forEach((n) => {
    n.textContent = t(n.getAttribute('data-i18n'));
  });
  document.querySelectorAll('[data-i18n-ph]').forEach((n) => {
    n.setAttribute('placeholder', t(n.getAttribute('data-i18n-ph')));
  });
}

function loc(obj) {
  return state.lang === 'zh' ? (obj.zh || obj.en) : (obj.en || obj.zh);
}

// ---------------------------------------------------------------- 主题
function currentTheme() {
  return document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  try { localStorage.setItem('crafter-theme', theme); } catch (e) { /* 忽略 */ }
  const btn = $('#themeBtn');
  if (btn) btn.textContent = theme === 'light' ? t('theme.light') : t('theme.dark');
  if (state.last) renderResults(state.last.data, state.last.payload, state.last.ms);
}

function toggleTheme() {
  applyTheme(currentTheme() === 'light' ? 'dark' : 'light');
}

function tierColor(tier) {
  const arr = currentTheme() === 'light' ? TIER_COLORS_LIGHT : TIER_COLORS_DARK;
  return arr[tier] || (currentTheme() === 'light' ? '#9aa0a6' : '#888888');
}

// 权重解析：0 / 负数都要原样保留，只有空值或非法值才回落到 1
function parseWeight(raw, fallback) {
  const s = String(raw === undefined || raw === null ? '' : raw).trim();
  if (s === '' || s === '-') return fallback === undefined ? 1 : fallback;
  const n = Number(s);
  return Number.isFinite(n) ? n : (fallback === undefined ? 1 : fallback);
}

function weightOf(key) {
  return parseWeight(state.weights[key], 1);
}

// ---------------------------------------------------------------- 语言
function applyLang(lang) {
  state.lang = lang === 'zh' ? 'zh' : 'en';
  try { localStorage.setItem(LANG_KEY, state.lang); } catch (e) { /* 忽略 */ }
  document.documentElement.setAttribute('data-lang', state.lang);
  document.documentElement.lang = state.lang === 'zh' ? 'zh-CN' : 'en';
  const btn = $('#langBtn');
  if (btn) btn.textContent = state.lang === 'zh' ? 'EN' : '中文';
  applyI18n();
  if (state.meta) {
    $('#ingLine').textContent = t('app.ingredients', { n: state.meta.ingredientCount });
    const tierSel = $('#baseTier');
    Array.prototype.forEach.call(tierSel.options, (o, i) => { o.textContent = t('ui.tierN', { n: i + 1 }); });
    updateTypeOptions();
    updateSkillLabels();
    updateTypeUi();
    renderStars();
    buildBanList($('#banFilter').value);
    renderBanChips();
    renderPresetList();
    renderSelected();
    updateWeightHint();
    if (state.last) renderResults(state.last.data, state.last.payload, state.last.ms);
  }
  if ($('#themeBtn')) $('#themeBtn').textContent = currentTheme() === 'light' ? t('theme.light') : t('theme.dark');
}

// ---------------------------------------------------------------- 初始化
async function boot() {
  applyTheme(currentTheme());
  $('#themeBtn').addEventListener('click', toggleTheme);
  $('#langBtn').addEventListener('click', () => applyLang(state.lang === 'zh' ? 'en' : 'zh'));

  const meta = await (await fetch('/api/meta')).json();
  state.meta = meta;
  meta.ids.forEach((i) => { state.labels[i.key] = i.label; });

  // 物品种类
  const typeSel = $('#type');
  meta.types.forEach(() => typeSel.appendChild(document.createElement('option')));
  updateTypeOptions();

  meta.types.forEach((ty) => {
    state.baseTable[ty.id] = meta.defaultBaseTable.slice();
    state.baseTier[ty.id] = 1;
  });

  // 档位选择
  const tierSel = $('#baseTier');
  for (let i = 1; i <= meta.baseTiers; i++) {
    const o = document.createElement('option');
    o.value = i;
    o.textContent = t('ui.tierN', { n: i });
    tierSel.appendChild(o);
  }

  // 五项点数上限
  updateSkillLabels();

  buildIdList('');
  renderSelected();
  buildBanList('');
  renderBanChips();
  renderPresetList();
  renderStars();
  updateTypeUi();
  applyLang(state.lang);

  typeSel.addEventListener('change', () => { renderStars(); updateTypeUi(); });
  tierSel.addEventListener('change', () => {
    state.baseTier[$('#type').value] = Number(tierSel.value);
    renderStars();
  });
  $('#applyAll').addEventListener('click', applyAll);
  $('#idFilter').addEventListener('input', (e) => buildIdList(e.target.value));
  $('#banFilter').addEventListener('input', (e) => buildBanList(e.target.value));
  $('#form').addEventListener('submit', onSubmit);

  $('#presetExport').addEventListener('click', onPresetExport);
  $('#presetCopy').addEventListener('click', onPresetCopy);
  $('#presetClear').addEventListener('click', () => { $('#presetCode').value = ''; });
  let importTimer = null;
  const onImport = () => {
    clearTimeout(importTimer);
    importTimer = setTimeout(tryImport, 350);
  };
  $('#presetImport').addEventListener('input', onImport);
  $('#presetImport').addEventListener('paste', () => setTimeout(onImport, 30));

  $('#ingLine').textContent = t('app.ingredients', { n: meta.ingredientCount });

  // ?demo=1 自动跑一次（截图 / 分享用）
  if (/[?&]demo=1/.test(location.search)) {
    if (!state.selected.length) toggleTarget('rawHealth');
    setTimeout(() => $('#form').requestSubmit(), 150);
  }
}

function currentType() {
  const id = $('#type').value;
  return state.meta.types.find((x) => x.id === id);
}

function updateTypeOptions() {
  const groups = { weapon: 'weapon', armour: 'armour', accessory: 'accessory', consumable: 'consumable' };
  const groupLabel = {
    en: { weapon: 'Weapons', armour: 'Armour', accessory: 'Accessories', consumable: 'Consumables' },
    zh: { weapon: '武器', armour: '防具', accessory: '饰品', consumable: '消耗品' },
  };
  const typeSel = $('#type');
  const current = typeSel.value || state.meta.types[0].id;
  typeSel.innerHTML = '';
  const kinds = Object.keys(groupLabel[state.lang] || groupLabel.en);
  kinds.forEach((kind) => {
    const items = state.meta.types.filter((x) => x.kind === kind);
    if (!items.length) return;
    const og = document.createElement('optgroup');
    og.label = groupLabel[state.lang][kind];
    items.forEach((ty) => {
      const o = document.createElement('option');
      o.value = ty.id;
      o.textContent = state.lang === 'zh' ? ty.cn : ty.en;
      og.appendChild(o);
    });
    typeSel.appendChild(og);
  });
  typeSel.value = current;
}

function updateSkillLabels() {
  const box = $('#skillLimits');
  const existing = {};
  box.querySelectorAll('input').forEach((inp) => { existing[inp.dataset.skill] = inp.value; });
  box.innerHTML = '';
  state.meta.skills.forEach((s) => {
    const wrap = el('div', 'skill');
    wrap.appendChild(el('span', 'skill-label', state.lang === 'zh' ? s.cn : s.en));
    const inp = document.createElement('input');
    inp.type = 'number';
    inp.dataset.skill = s.key;
    inp.placeholder = state.lang === 'zh' ? '不限' : 'any';
    if (existing[s.key] !== undefined) inp.value = existing[s.key];
    wrap.appendChild(inp);
    box.appendChild(wrap);
  });
}

// ---------------------------------------------------------------- 基础耐久档位
function renderStars() {
  const ty = currentType();
  const box = $('#stars');
  box.innerHTML = '';
  const table = state.baseTable[ty.id];
  $('#baseTier').value = String(state.baseTier[ty.id]);

  for (let i = 0; i < state.meta.baseTiers; i++) {
    const cell = el('div', 'star' + (i + 1 === state.baseTier[ty.id] ? ' active' : ''));
    cell.appendChild(el('span', 'star-label', t('ui.tierN', { n: i + 1 })));
    const inp = document.createElement('input');
    inp.type = 'number';
    inp.value = table[i];
    inp.addEventListener('input', () => {
      const raw = inp.value.trim();
      const n = Number(raw);
      table[i] = raw === '' || !Number.isFinite(n) ? 0 : n;
      markActive(i + 1);
    });
    inp.addEventListener('focus', () => {
      state.baseTier[ty.id] = i + 1;
      $('#baseTier').value = String(i + 1);
      markActive(i + 1);
    });
    cell.appendChild(inp);
    box.appendChild(cell);
  }
  updateBasePreview();
}

// 只切高亮，不重建 DOM（否则输入框会丢焦点）
function markActive(n) {
  const box = $('#stars');
  Array.prototype.forEach.call(box.children, (c, idx) => {
    c.classList.toggle('active', idx + 1 === n);
  });
  updateBasePreview();
}

function updateBasePreview() {
  const ty = currentType();
  const v = state.baseTable[ty.id][state.baseTier[ty.id] - 1];
  $('#baseDuraPreview').textContent = t('ui.current', { v: fmt(v) });
}

function applyAll() {
  const ty = currentType();
  const vals = state.baseTable[ty.id].slice();
  state.meta.types.forEach((x) => { state.baseTable[x.id] = vals.slice(); });
  const btn = $('#applyAll');
  btn.textContent = t('ui.applied');
  setTimeout(() => { btn.textContent = t('ui.applyAll'); }, 1200);
}

function updateTypeUi() {
  const ty = currentType();
  const isConsumable = ty.kind === 'consumable';
  $('#minDurLabel').textContent = isConsumable ? t('ui.minDurC') : t('ui.minDur');
  $('#minDur').placeholder = isConsumable ? t('ui.minDurPhC') : t('ui.minDurPh');
  document.querySelectorAll('.only-consumable').forEach((n) => {
    n.style.display = isConsumable ? '' : 'none';
  });
  const names = ty.professions.map((p) => loc(state.meta.professions[p] || { zh: p, en: p })).join(' / ');
  $('#typeHint').textContent = t('ui.professions', { list: names });
}

// ---------------------------------------------------------------- 目标词条
function buildIdList(filter) {
  const box = $('#idList');
  box.innerHTML = '';
  const q = (filter || '').trim().toLowerCase();
  state.meta.ids.forEach((i) => {
    const label = `${i.label} ${i.key}`.toLowerCase();
    if (q && label.indexOf(q) < 0) return;
    const row = el('label', 'idrow' + (state.selected.includes(i.key) ? ' on' : ''));
    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.checked = state.selected.includes(i.key);
    cb.addEventListener('change', () => toggleTarget(i.key));
    row.appendChild(cb);
    row.appendChild(el('span', 'idlabel', esc(i.label)));
    row.appendChild(el('span', 'idkey', esc(i.key)));
    row.appendChild(el('span', 'idcount', String(i.count)));
    box.appendChild(row);
  });
  if (!box.children.length) box.appendChild(el('div', 'empty-small', t('ui.noMatch')));
}

function toggleTarget(key) {
  const idx = state.selected.indexOf(key);
  if (idx >= 0) {
    state.selected.splice(idx, 1);
  } else {
    state.selected.push(key);
    if (state.weights[key] === undefined) state.weights[key] = 1;
    if (state.mins[key] === undefined) state.mins[key] = '';
    if (state.maxs[key] === undefined) state.maxs[key] = '';
  }
  buildIdList($('#idFilter').value);
  renderSelected();
}

function renderSelected() {
  const box = $('#selected');
  box.innerHTML = '';
  if (!state.selected.length) {
    box.appendChild(el('div', 'empty-small', t('ui.noTarget')));
    updateWeightHint();
    return;
  }
  state.selected.forEach((key) => {
    const row = el('div', 'selrow');
    row.appendChild(el('span', 'selname', esc(state.labels[key] || key)));

    const w = document.createElement('input');
    w.type = 'number';
    w.step = 'any';
    w.title = t('ui.weight');
    w.value = weightOf(key);
    w.addEventListener('input', () => {
      state.weights[key] = parseWeight(w.value, 1);
      updateWeightHint();
    });
    row.appendChild(w);

    const m = document.createElement('input');
    m.type = 'number';
    m.placeholder = t('ui.min');
    m.title = t('ui.min');
    m.value = state.mins[key];
    m.addEventListener('input', () => { state.mins[key] = m.value; });
    row.appendChild(m);

    const mx = document.createElement('input');
    mx.type = 'number';
    mx.placeholder = t('ui.max');
    mx.title = t('ui.maxHint');
    mx.value = state.maxs[key];
    mx.addEventListener('input', () => { state.maxs[key] = mx.value; });
    row.appendChild(mx);

    const x = el('button', 'mini', '×');
    x.type = 'button';
    x.title = t('ui.remove');
    x.addEventListener('click', () => toggleTarget(key));
    row.appendChild(x);

    box.appendChild(row);
  });
  updateWeightHint();
}

function updateWeightHint() {
  const box = $('#weightHint');
  if (!box) return;
  const allZero = state.selected.length > 0 && state.selected.every((k) => weightOf(k) === 0);
  box.textContent = allZero ? t('ui.weightHintZero') : t('ui.weightHint');
  box.classList.toggle('warn', allZero);
}

// ---------------------------------------------------------------- 禁用素材
function buildBanList(filter) {
  const box = $('#banList');
  box.innerHTML = '';
  if (!state.meta) return;
  const q = (filter || '').trim().toLowerCase();
  const list = state.meta.ingredients
    .filter((i) => !q || i.name.toLowerCase().indexOf(q) >= 0)
    .sort((a, b) => a.name.localeCompare(b.name));
  list.slice(0, 120).forEach((i) => {
    const row = el('label', 'idrow' + (state.disabled.includes(i.id) ? ' on' : ''));
    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.checked = state.disabled.includes(i.id);
    cb.addEventListener('change', () => toggleBan(i.id));
    row.appendChild(cb);
    row.appendChild(el('span', 'idlabel', esc(i.name)));
    row.appendChild(el('span', 'idkey', esc((i.professions || []).map((p) => {
      const pr = state.meta.professions[p];
      return pr ? loc(pr) : p;
    }).join('/'))));
    row.appendChild(el('span', 'idcount', i.durability > 0 ? '+' + i.durability : String(i.durability)));
    box.appendChild(row);
  });
  if (!list.length) box.appendChild(el('div', 'empty-small', t('ui.noMatch')));
  if (list.length > 120) box.appendChild(el('div', 'empty-small', t('ui.more', { n: list.length - 120 })));
}

function toggleBan(id) {
  const i = state.disabled.indexOf(id);
  if (i >= 0) state.disabled.splice(i, 1);
  else state.disabled.push(id);
  buildBanList($('#banFilter').value);
  renderBanChips();
}

function renderBanChips() {
  const box = $('#banChips');
  box.innerHTML = '';
  $('#banCount').textContent = String(state.disabled.length);
  state.disabled.forEach((id) => {
    const chip = el('span', 'chip on', esc(id) + ' <b>×</b>');
    chip.style.cursor = 'pointer';
    chip.title = t('ui.restore');
    chip.addEventListener('click', () => toggleBan(id));
    box.appendChild(chip);
  });
  if (!state.disabled.length) box.appendChild(el('span', 'empty-small', t('ui.noBan')));
}

// ---------------------------------------------------------------- 预设配置
function collectPreset() {
  const ty = currentType();
  const meta = state.meta;
  const uniform = meta.types.every((x) => sameArr(state.baseTable[x.id], state.baseTable[ty.id]));
  let bd;
  if (uniform) {
    bd = state.baseTable[ty.id].map(Number);
  } else {
    bd = {};
    meta.types.forEach((x) => {
      if (!sameArr(state.baseTable[x.id], meta.defaultBaseTable)) bd[x.id] = state.baseTable[x.id].map(Number);
    });
  }
  const pl = {};
  document.querySelectorAll('#skillLimits input').forEach((inp) => {
    const v = inp.value.trim();
    if (v !== '') pl[inp.dataset.skill] = Number(v);
  });
  return {
    v: 1,
    t: ty.id,
    bt: state.baseTier[ty.id],
    bd,
    md: numOrNull($('#minDur').value),
    pl,
    tg: state.selected.map((k) => [k, weightOf(k),
      state.mins[k] === '' || state.mins[k] === undefined ? null : Number(state.mins[k]),
      state.maxs[k] === '' || state.maxs[k] === undefined ? null : Number(state.maxs[k])]),
    cmp: $('#compare').value,
    n: Number($('#topN').value) || 12,
    e: Number($('#effort').value) || 1200,
    dup: $('#allowDupes').checked ? 1 : 0,
    cb: ty.kind === 'consumable' ? { [ty.id]: Number($('#baseDur').value) || 0 } : undefined,
    ch: ty.kind === 'consumable' ? { [ty.id]: Number($('#baseCharges').value) || 0 } : undefined,
    mc: ty.kind === 'consumable' ? numOrNull($('#minCharges').value) : null,
    dis: state.disabled.slice(),
    lg: state.lang,
  };
}

function toB64Url(bytes) {
  let s = '';
  for (let i = 0; i < bytes.length; i++) s += String.fromCharCode(bytes[i]);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function fromB64Url(str) {
  const s = str.replace(/-/g, '+').replace(/_/g, '/');
  const pad = (4 - (s.length % 4)) % 4;
  const bin = atob(s + '='.repeat(pad));
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

async function packPreset(obj) {
  const bytes = new TextEncoder().encode(JSON.stringify(obj));
  if (typeof CompressionStream === 'function') {
    try {
      const cs = new CompressionStream('deflate-raw');
      const stream = new Blob([bytes]).stream().pipeThrough(cs);
      const buf = new Uint8Array(await new Response(stream).arrayBuffer());
      return 'WBCz' + toB64Url(buf);
    } catch (e) { /* 退回未压缩 */ }
  }
  return 'WBC' + toB64Url(bytes);
}

async function unpackPreset(raw) {
  const s = String(raw || '').replace(/\s+/g, '');
  if (!s) return null;
  if (s.indexOf('WBCz') === 0) {
    if (typeof DecompressionStream !== 'function') throw new Error('decompression unsupported');
    const bytes = fromB64Url(s.slice(4));
    const ds = new DecompressionStream('deflate-raw');
    const stream = new Blob([bytes]).stream().pipeThrough(ds);
    return JSON.parse(await new Response(stream).text());
  }
  if (s.indexOf('WBC') === 0) {
    return JSON.parse(new TextDecoder().decode(fromB64Url(s.slice(3))));
  }
  return null;
}

function applyPreset(p) {
  if (!p || typeof p !== 'object') return false;
  const meta = state.meta;
  const types = meta.types;

  types.forEach((x) => {
    state.baseTable[x.id] = meta.defaultBaseTable.slice();
    state.baseTier[x.id] = 1;
  });
  if (Array.isArray(p.bd)) {
    types.forEach((x) => { state.baseTable[x.id] = p.bd.slice(); });
  } else if (p.bd && typeof p.bd === 'object') {
    Object.keys(p.bd).forEach((k) => {
      if (state.baseTable[k] && Array.isArray(p.bd[k])) state.baseTable[k] = p.bd[k].slice();
    });
  }
  if (p.t && types.some((x) => x.id === p.t)) $('#type').value = p.t;
  const typeId = $('#type').value;
  if (p.bt) state.baseTier[typeId] = Math.min(Math.max(Number(p.bt) || 1, 1), meta.baseTiers);

  $('#minDur').value = p.md === null || p.md === undefined ? '' : p.md;
  $('#minCharges').value = p.mc === null || p.mc === undefined ? '' : p.mc;
  document.querySelectorAll('#skillLimits input').forEach((inp) => {
    const v = (p.pl || {})[inp.dataset.skill];
    inp.value = v === null || v === undefined ? '' : v;
  });

  state.selected = [];
  state.weights = {};
  state.mins = {};
  state.maxs = {};
  (p.tg || []).forEach((row) => {
    if (!row || !row[0] || !state.labels[row[0]]) return;
    state.selected.push(row[0]);
    state.weights[row[0]] = row[1] === undefined || row[1] === null ? 1 : Number(row[1]);
    state.mins[row[0]] = row[2] === undefined || row[2] === null ? '' : row[2];
    state.maxs[row[0]] = row[3] === undefined || row[3] === null ? '' : row[3];
  });

  $('#compare').value = p.cmp === 'min' ? 'min' : 'max';
  $('#topN').value = p.n || 12;
  const eff = Number(p.e) || 1200;
  $('#effort').value = String(eff <= 600 ? 400 : eff <= 2000 ? 1200 : 3000);
  $('#allowDupes').checked = p.dup !== 0;
  $('#baseDur').value = (p.cb && p.cb[typeId]) || 0;
  $('#baseCharges').value = p.ch && p.ch[typeId] !== undefined ? p.ch[typeId] : 3;
  state.disabled = Array.isArray(p.dis) ? p.dis.slice() : [];

  renderStars();
  updateTypeUi();
  buildIdList($('#idFilter').value);
  renderSelected();
  buildBanList($('#banFilter').value);
  renderBanChips();
  if (p.lg === 'zh' || p.lg === 'en') applyLang(p.lg);
  return true;
}

function loadPresets() {
  try { return JSON.parse(localStorage.getItem(PRESET_KEY)) || []; } catch (e) { return []; }
}

function savePresets(list) {
  try { localStorage.setItem(PRESET_KEY, JSON.stringify(list)); } catch (e) { /* 忽略 */ }
}

function renderPresetList() {
  const box = $('#presetList');
  if (!box) return;
  box.innerHTML = '';
  const list = loadPresets();
  if (!list.length) {
    box.appendChild(el('div', 'empty-small', t('ui.noPreset')));
    return;
  }
  list.forEach((p, idx) => {
    const row = el('div', 'preset-row');
    row.appendChild(el('span', 'preset-name', esc(p.name || `#${idx + 1}`)));
    const load = el('button', 'mini', t('ui.load'));
    load.type = 'button';
    load.addEventListener('click', () => {
      $('#presetCode').value = p.code;
      tryImportCode(p.code);
    });
    row.appendChild(load);
    const del = el('button', 'mini', t('ui.del'));
    del.type = 'button';
    del.addEventListener('click', () => {
      const cur = loadPresets();
      cur.splice(idx, 1);
      savePresets(cur);
      renderPresetList();
    });
    row.appendChild(del);
    box.appendChild(row);
  });
}

async function onPresetExport() {
  const name = ($('#presetName').value || '').trim() || `#${loadPresets().length + 1}`;
  const code = await packPreset(collectPreset());
  $('#presetCode').value = code;
  const list = loadPresets().filter((p) => p.name !== name);
  list.unshift({ name, code, ts: Date.now() });
  savePresets(list.slice(0, 30));
  renderPresetList();
  $('#presetStatus').textContent = t('msg.saved', { name, n: code.length });
}

async function onPresetCopy() {
  const code = $('#presetCode').value.trim();
  if (!code) return;
  try {
    await navigator.clipboard.writeText(code);
    $('#presetStatus').textContent = t('msg.copied');
  } catch (e) {
    $('#presetCode').select();
    $('#presetStatus').textContent = t('msg.selectCopy');
  }
}

function tryImportCode(code) {
  unpackPreset(code).then((p) => {
    if (!p) {
      $('#presetStatus').textContent = t('msg.badCode');
      return;
    }
    if (applyPreset(p)) {
      const n = (p.tg || []).length;
      const ban = state.disabled.length ? t('msg.importedBan', { m: state.disabled.length }) : '';
      $('#presetStatus').textContent = t('msg.imported', { n, ban });
    }
  }).catch((e) => {
    $('#presetStatus').textContent = t('msg.importFail', { e: e.message });
  });
}

function tryImport() {
  const code = $('#presetImport').value.trim();
  if (code.length < 8) return;
  tryImportCode(code);
}

// ---------------------------------------------------------------- 搜索
function pointsLimits() {
  const out = {};
  document.querySelectorAll('#skillLimits input').forEach((inp) => {
    const v = inp.value.trim();
    out[inp.dataset.skill] = v === '' ? null : Number(v);
  });
  return out;
}

async function onSubmit(ev) {
  ev.preventDefault();
  if (state.busy) return;
  if (!state.selected.length) {
    $('#status').textContent = t('ui.pickTarget');
    return;
  }
  const ty = currentType();
  const payload = {
    type: ty.id,
    baseDurability: state.baseTable,
    baseTier: state.baseTier,
    consumableBase: ty.kind === 'consumable' ? { [ty.id]: Number($('#baseDur').value) || 0 } : {},
    chargesBase: ty.kind === 'consumable' ? { [ty.id]: Number($('#baseCharges').value) || 0 } : {},
    minDurability: numOrNull($('#minDur').value),
    minCharges: ty.kind === 'consumable' ? numOrNull($('#minCharges').value) : null,
    pointsLimit: pointsLimits(),
    targets: state.selected.map((k) => ({
      key: k,
      weight: weightOf(k),
      min: state.mins[k] === '' || state.mins[k] === undefined ? null : Number(state.mins[k]),
      max: state.maxs[k] === '' || state.maxs[k] === undefined ? null : Number(state.maxs[k]),
    })),
    compare: $('#compare').value,
    topN: Number($('#topN').value) || 12,
    beam: Number($('#effort').value) || 1200,
    allowDuplicates: $('#allowDupes').checked,
    disabled: state.disabled,
  };

  state.busy = true;
  $('#go').disabled = true;
  $('#status').textContent = t('ui.searching');
  const t0 = performance.now();
  try {
    const res = await fetch('/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    renderResults(data, payload, Math.round(performance.now() - t0));
  } catch (err) {
    $('#status').textContent = t('msg.reqFail', { e: err.message });
  } finally {
    state.busy = false;
    $('#go').disabled = false;
  }
}

function numOrNull(v) {
  if (v === '' || v === null || v === undefined) return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

// ---------------------------------------------------------------- 渲染
function renderResults(data, payload, ms) {
  state.last = { data, payload, ms };
  const list = $('#list');
  list.innerHTML = '';
  const results = data.results || [];
  const ty = currentType();
  const isConsumable = ty.kind === 'consumable';

  if (!results.length) {
    $('#summary').textContent = `${ms} ms`;
    $('#status').textContent = '';
    const msg = data.code ? t('err.' + data.code) : (data.message || t('res.noResults'));
    list.appendChild(el('div', 'empty', esc(msg)));
    return;
  }

  $('#summary').textContent = t('res.summary', {
    n: results.length, c: data.candidates == null ? '-' : data.candidates,
    s: data.scanned == null ? '-' : data.scanned, ms,
  });
  $('#status').textContent = '';

  results.forEach((r, idx) => {
    const card = el('article', 'card');
    const head = el('div', 'card-head');
    head.appendChild(el('span', 'rank', `#${idx + 1}`));

    if (isConsumable) {
      head.appendChild(el('span', 'badge dur', t('res.time', { v: r.duration })));
      head.appendChild(el('span', 'badge', t('res.charges', { v: r.charges })));
    } else {
      const b = el('span', 'badge dur' + (r.durability < 0 ? ' neg' : ''),
        t('res.durability', { v: r.durability }));
      b.title = `${r.baseDurability} (T${r.baseTier}) + ${r.durabilityModifier}`;
      head.appendChild(b);
    }

    const skillsOn = state.meta.skills.filter((s) => r.skills[s.key] > 0);
    if (skillsOn.length) {
      head.appendChild(el('span', 'badge',
        t('res.skills', { list: skillsOn.map((s) => `${state.lang === 'zh' ? s.cn : s.en} ${r.skills[s.key]}`).join(' · ') })));
    }

    r.targets.forEach((tg) => {
      head.appendChild(el('span', 'badge target',
        `${esc(state.labels[tg.key] || tg.key)} ${fmt(tg.value)}`));
    });
    card.appendChild(head);

    // 3x2 网格
    const grid = el('div', 'grid');
    r.cells.forEach((c) => {
      const cell = el('div', 'cell');
      cell.style.setProperty('--tier', tierColor(c.tier));
      cell.appendChild(el('div', 'cname', esc(c.name)));
      const row = el('div', 'crow');
      const b = el('span', 'cbonus', (c.bonus > 0 ? '+' : '') + c.bonus + '%');
      b.classList.add(c.bonus > 0 ? 'pos' : c.bonus < 0 ? 'neg' : 'zero');
      row.appendChild(b);
      const own = c.ids[r.targets[0].key];
      if (own) row.appendChild(el('span', 'cid', fmt(own.max)));
      if (c.durability > 0) {
        const d = el('span', 'cdur', `+${c.durability}`);
        d.title = '+durability';
        row.appendChild(d);
      }
      cell.appendChild(row);
      grid.appendChild(cell);
    });
    card.appendChild(grid);

    // 词条明细
    const detail = el('div', 'detail');
    const tkeys = r.targets.map((x) => x.key);
    Object.entries(r.ids)
      .filter(([, v]) => v.max !== 0 || v.min !== 0)
      .sort((a, b) => Math.abs(b[1].max) - Math.abs(a[1].max))
      .forEach(([k, v]) => {
        const chip = el('span', 'chip' + (tkeys.includes(k) ? ' on' : ''),
          `${esc(state.labels[k] || k)} <b>${v.min === v.max ? fmt(v.max) : `${fmt(v.min)}~${fmt(v.max)}`}</b>`);
        detail.appendChild(chip);
      });
    if (!detail.children.length) detail.appendChild(el('span', 'chip', t('res.noIds')));
    card.appendChild(detail);

    // 点数与耐久明细
    const lines = [];
    const sk = state.meta.skills
      .map((s) => [state.lang === 'zh' ? s.cn : s.en, r.skills[s.key]])
      .filter(([, v]) => v !== 0)
      .map(([cn, v]) => `${cn} ${v}`)
      .join('　');
    if (sk) lines.push(sk);
    if (!isConsumable) {
      const mod = r.durabilityModifier;
      lines.push(mod <= 0
        ? t('res.durMinus', { b: r.baseDurability, t: r.baseTier, m: Math.abs(mod), d: r.durability })
        : t('res.durPlus', { b: r.baseDurability, t: r.baseTier, m: mod, d: r.durability }));
    } else {
      lines.push(t('res.durationLine', { b: r.baseDuration, m: r.duration - r.baseDuration, d: r.duration }));
      const cm = r.charges - (r.baseCharges === undefined ? 3 : r.baseCharges);
      lines.push(t('res.chargesLine', { b: r.baseCharges === undefined ? 3 : r.baseCharges, m: cm, d: r.charges }));
    }
    card.appendChild(el('div', 'skills', esc(lines.join('　|　'))));

    list.appendChild(card);
  });
}

boot().catch((e) => {
  $('#status').textContent = t('msg.initFail', { e: e.message });
});
