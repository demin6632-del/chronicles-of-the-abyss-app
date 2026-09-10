from pathlib import Path

p = Path('game.html')
text = p.read_text(encoding='utf-8')
marker = '</script></body></html>'
if "const DLC_ID='abyss-awakening';" in text:
    print('DLC already present')
    raise SystemExit(0)
if not text.endswith(marker):
    raise SystemExit('Unexpected game.html ending')
dlc = """\n/* ============================================================
   ПЛАТНОЕ DLC v1 — ПРОБУЖДЕНИЕ БЕЗДНЫ
   Доступ открывается только после серверной проверки покупки.
   ============================================================ */
const DLC_ID='abyss-awakening';
const DLC_PRICE_RUB=300;
const DLC_API='https://chronicles-of-the-abyss-dlc-api.vercel.app';

function dlcUnlocked(){
  ensureMeta();
  return !!(META.dlc&&META.dlc[DLC_ID]&&META.dlc[DLC_ID].unlocked);
}
function setDlcUnlocked(code){
  ensureMeta();
  META.dlc=META.dlc||{};
  META.dlc[DLC_ID]={unlocked:true,activatedAt:Date.now(),code:String(code||'')};
  metaSave(META);
}
function openDlcActivation(){
  openModal(`<h2>🌑 Пробуждение Бездны</h2>
  <p class="muted">Платное DLC за ${DLC_PRICE_RUB} ₽. После покупки на сайте ты получаешь код активации.</p>
  <input id="dlcCode" autocomplete="off" placeholder="ABYSS-...">
  <button class="btn primary" onclick="activateDlc(document.getElementById('dlcCode').value)">🔓 Активировать DLC</button>
  <button class="btn" onclick="window.open('https://demin6632-del.github.io/chronicles-of-the-abyss-site/dlc.html','_blank')">🛒 Купить DLC — ${DLC_PRICE_RUB} ₽</button>
  <div class="small muted">Код проверяется сервером. После успешной активации DLC сохраняется на этом устройстве.</div>
  <button class="btn" onclick="closeModal()">Закрыть</button>`);
}
async function activateDlc(code){
  code=String(code||'').trim();
  if(!code){toast('Введи код активации.');return}
  const b=document.querySelector('#modalBack .primary');
  if(b){b.disabled=true;b.textContent='⏳ Проверка...'}
  try{
    const r=await fetch(DLC_API+'/api/activate',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({code})
    });
    const d=await r.json().catch(()=>({}));
    if(r.ok&&d.valid&&d.dlc_id===DLC_ID){
      setDlcUnlocked(code);
      awardAchievement('dlcAwakened');
      closeModal();
      toast('🌑 DLC «Пробуждение Бездны» активировано!');
      render();
    }else{
      toast(d.error||'Код недействителен или покупка не подтверждена.');
      if(b){b.disabled=false;b.textContent='🔓 Активировать DLC'}
    }
  }catch(e){
    toast('Не удалось связаться с сервером активации. Проверь интернет и попробуй снова.');
    if(b){b.disabled=false;b.textContent='🔓 Активировать DLC'}
  }
}

Object.assign(CLASSES,{awakened:{name:'Пробуждённый',icon:'🌑',hp:96,mp:64,atk:13,def:5,tags:['magic','risk','combo'],desc:'Герой, коснувшийся ядра Бездны. Использует разломы, эхо и силу за счёт собственного здоровья.',skills:['rift','voidpulse','echo','devour','collapse'],dlc:DLC_ID}});
Object.defineProperty(CLASSES,'awakened',{value:CLASSES.awakened,enumerable:false,writable:true,configurable:true});
Object.assign(SKILLS,{
  rift:{name:'Разлом',cost:12,tag:'magic',tags:['magic','risk'],desc:'1.7× магический урон + замедление на 2 хода.',base:1.7,dlc:DLC_ID},
  voidpulse:{name:'Импульс Бездны',cost:10,tag:'magic',tags:['magic','burn','poison'],desc:'1.45× магический урон + случайный негативный эффект.',base:1.45,dlc:DLC_ID},
  echo:{name:'Эхо Бездны',cost:9,tag:'combo',tags:['combo','magic'],desc:'2 удара по 0.75×; +2 комбо и +2 MP.',base:.75,dlc:DLC_ID},
  devour:{name:'Поглощение',cost:14,tag:'risk',tags:['risk','heal'],desc:'1.5× урон; лечит на 15% нанесённого урона.',base:1.5,dlc:DLC_ID},
  collapse:{name:'Схлопывание',cost:18,tag:'risk',tags:['risk','magic','combo'],desc:'2.5× магический урон; теряешь 6% max HP. Сильнее по врагу со статусом.',base:2.5,dlc:DLC_ID}
});
Object.assign(SUBCLASSES,{awakened:{
  voidwalker:{name:'Ходок Бездны',icon:'🕳️',desc:'Сила растёт вместе с риском.',tags:['risk','magic'],bonus:{magic:5,hp:-4},dlc:DLC_ID},
  echoLord:{name:'Повелитель Эха',icon:'🌌',desc:'Комбо превращается в магическую силу.',tags:['combo','magic'],bonus:{mp:12,crit:.03},dlc:DLC_ID}
}});

const DLC_ITEMS=[
  {id:'riftblade',name:'Клинок Разлома',slot:'weapon',rarity:'epic',tags:['magic','risk'],atk:6,magic:3,desc:'+6 ATK, +3 MAGIC; урон навыков +5%.',dlc:DLC_ID,skillMul:.05},
  {id:'voidstaff',name:'Посох Пустого Света',slot:'weapon',rarity:'epic',tags:['magic','burn'],magic:9,desc:'+9 MAGIC; горение от навыков +1.',dlc:DLC_ID,skillBurn:1},
  {id:'echoDagger',name:'Эхо-кинжал',slot:'weapon',rarity:'rare',tags:['combo','crit'],atk:4,crit:.06,desc:'+4 ATK, +6% CRIT; при комбо 5+ ещё +10% урона.',dlc:DLC_ID,comboMul:.10},
  {id:'abyssArmor',name:'Панцирь Пробуждения',slot:'armor',rarity:'epic',tags:['defense','risk'],def:6,desc:'+6 DEF; при HP ниже 40% получаемый урон -10%.',dlc:DLC_ID,lowHpDef:.10},
  {id:'fractureMail',name:'Кольчуга Трещин',slot:'armor',rarity:'rare',tags:['bleed','magic'],def:4,magic:3,desc:'+4 DEF, +3 MAGIC; кровоточащие враги получают +10% урона.',dlc:DLC_ID,bleedMul:.10},
  {id:'voidMantle',name:'Мантия Пустоты',slot:'armor',rarity:'legendary',def:3,magic:10,desc:'+10 MAGIC, +3 DEF; каждый третий ход +3 MP.',dlc:DLC_ID,turnMana:3},
  {id:'awakeningAmulet',name:'Амулет Пробуждения',slot:'accessory',rarity:'epic',tags:['heal','risk'],hp:10,desc:'+10 max HP; лечение навыками +20%.',dlc:DLC_ID,healMul:.20},
  {id:'echoRing',name:'Кольцо Эха',slot:'accessory',rarity:'rare',tags:['combo','magic'],magic:4,desc:'+4 MAGIC; каждый навык с 2+ комбо возвращает 1 MP.',dlc:DLC_ID,echoMp:1},
  {id:'riftBoots',name:'Сапоги Разлома',slot:'accessory',rarity:'rare',tags:['risk','combo'],crit:.05,desc:'+5% CRIT; первый навык в бою наносит +20% урона.',dlc:DLC_ID,firstSkill:.20},
  {id:'abyssCore',name:'Ядро Пробуждения',slot:'accessory',rarity:'legendary',tags:['magic','risk','summon'],magic:7,atk:3,desc:'+3 ATK, +7 MAGIC; при победе над элитой +5% max HP до конца забега.',dlc:DLC_ID,eliteHp:.05}
];
ITEMS.push(...DLC_ITEMS);
const DLC_RELICS=[
  {id:'riftHeart',name:'Сердце Разлома',rarity:'epic',tags:['magic','risk'],desc:'Навыки наносят +12% урона, но их стоимость MP +1.',dlc:DLC_ID},
  {id:'echoCrown',name:'Корона Эха',rarity:'legendary',tags:['combo','magic'],desc:'При комбо 5+ каждый навык получает +25% урона.',dlc:DLC_ID},
  {id:'voidEye',name:'Око Пробуждения',rarity:'legendary',tags:['risk','heal'],desc:'Один раз за бой при HP ≤25% полностью снимает один негативный статус и лечит 18% max HP.',dlc:DLC_ID},
  {id:'fractureShard',name:'Осколок Трещины',rarity:'rare',tags:['bleed','risk'],desc:'Криты по кровоточащим целям добавляют 1 кровотечение.',dlc:DLC_ID},
  {id:'abyssLantern',name:'Фонарь Бездны',rarity:'rare',tags:['magic','burn','poison'],desc:'Каждый первый негативный эффект на враге в бою получает +1 ход.',dlc:DLC_ID},
  {id:'echoStone',name:'Камень Эха',rarity:'epic',tags:['combo','heal'],desc:'При комбо 4+ каждый третий навык лечит 4% max HP.',dlc:DLC_ID},
  {id:'voidAnchor',name:'Якорь Пустоты',rarity:'epic',tags:['defense','risk'],desc:'Когда блок поглощает удар полностью, получаешь +2 MP.',dlc:DLC_ID},
  {id:'awakeningSeal',name:'Печать Пробуждения',rarity:'legendary',tags:['magic','combo','risk'],desc:'За каждый активный статус на враге +6% урона навыков, максимум +30%.',dlc:DLC_ID}
];
RELICS.push(...DLC_RELICS);
const DLC_ENEMIES=[
  {id:'riftStalker',name:'Сталкер Разлома',hp:82,atk:17,def:4,gold:48,pattern:['attack','slow','crit'],dlc:DLC_ID},
  {id:'voidSeer',name:'Провидец Пустоты',hp:76,atk:15,def:5,gold:52,pattern:['burn','poison','heal'],dlc:DLC_ID},
  {id:'echoDevourer',name:'Пожиратель Эха',hp:105,atk:18,def:6,gold:65,pattern:['block','stun','attack'],dlc:DLC_ID}
];
ENEMIES.push(...DLC_ENEMIES);
const DLC_BOSS={id:'awakeningAvatar',name:'Аватар Пробуждения',hp:330,atk:27,def:9,gold:240,phases:3,skills:['special','burn','crit','heal'],dlc:DLC_ID};
BOSSES.push(DLC_BOSS);
const DLC_EVENTS=[
  {name:'Сломанный портал',desc:'Разлом предлагает короткий путь за часть жизненной силы.',actions:[['🕳️ -15 HP → +100 золота',()=>{S.p.hp=Math.max(1,S.p.hp-15);S.gold+=100;addLog('🕳️ Портал отдал тебе золото.','good')}],['🌌 -10 max HP → редкая реликвия',()=>{S.p.max=Math.max(1,S.p.max-10);S.p.hp=Math.min(S.p.hp,S.p.max);giveRelic('rare')}],['🚪 Уйти',()=>{}]],dlc:DLC_ID},
  {name:'Хор Эха',desc:'Голоса обещают силу, если ты выдержишь их ритм.',actions:[['⚡ +3 комбо → -8 HP',()=>{S.p.combo=Math.min(9,S.p.combo+3);S.p.hp=Math.max(1,S.p.hp-8)}],['💧 +12 MP → получить проклятие',()=>{S.p.mp=Math.min(S.p.maxmp,S.p.mp+12);addCurse()}],['🚪 Уйти',()=>{}]],dlc:DLC_ID},
  {name:'Око Пустоты',desc:'Оно показывает один возможный исход твоего похода.',actions:[['👁️ Увидеть силу → +15% ATK на текущий бой',()=>{S.p.tempDlcAtk=.15;addLog('👁️ Око усилило следующий бой.','good')}],['💎 Заплатить 30 золота → легендарная реликвия',()=>{if(S.gold>=30){S.gold-=30;giveRelic('legendary')}else toast('Не хватает золота.')}],['🚪 Уйти',()=>{}]],dlc:DLC_ID},
  {name:'Кузница Трещин',desc:'Металл здесь помнит удары тех, кто прошёл Бездну.',actions:[['🔨 Улучшить случайный предмет',()=>{const i=R.int(S.inventory.length);if(S.inventory.length)forgeItem(i);else toast('Нет предметов.')}],['🔥 Обменять 15 HP на 40 золота',()=>{S.p.hp=Math.max(1,S.p.hp-15);S.gold+=40}],['🚪 Уйти',()=>{}]],dlc:DLC_ID},
  {name:'Последнее пробуждение',desc:'Бездны становится больше, но и ты меняешься вместе с ней.',actions:[['🌑 +20 max HP → +1 проклятие',()=>{S.p.max+=20;S.p.hp=Math.min(S.p.max,S.p.hp+20);addCurse()}],['⚔️ +2 ATK → -20 max HP',()=>{S.p.atk+=2;S.p.max=Math.max(1,S.p.max-20);S.p.hp=Math.min(S.p.hp,S.p.max)}],['🚪 Уйти',()=>{}]],dlc:DLC_ID}
];
EVENTS.push(...DLC_EVENTS);
Object.assign(ACHIEVEMENTS,{dlcAwakened:{name:'Пробуждение',desc:'Активировать DLC «Пробуждение Бездны».',pts:20,dlc:DLC_ID},dlcClass:{name:'Новая грань',desc:'Завершить забег Пробуждённым.',pts:35,dlc:DLC_ID},dlcBoss:{name:'Лик Пробуждения',desc:'Победить Аватара Пробуждения.',pts:45,dlc:DLC_ID},dlcBuild:{name:'Эхо и разлом',desc:'Завершить забег с активной синергией DLC.',pts:30,dlc:DLC_ID},dlcCollector:{name:'Архив пробуждения',desc:'Собрать 5 разных предметов или реликвий DLC.',pts:40,dlc:DLC_ID}});
CODEX_ENEMIES.push(...DLC_ENEMIES,DLC_BOSS);

const BASE_DLC_GIVE_RELIC=giveRelic;
giveRelic=function(rarity){if(dlcUnlocked())return BASE_DLC_GIVE_RELIC(rarity);const original=RELICS.slice();for(let i=RELICS.length-1;i>=0;i--)if(RELICS[i].dlc===DLC_ID)RELICS.splice(i,1);try{return BASE_DLC_GIVE_RELIC(rarity)}finally{RELICS.splice(0,RELICS.length,...original)}};
const BASE_DLC_START_COMBAT=startCombat;
startCombat=function(elite=false){const original=ENEMIES.slice();if(!dlcUnlocked())for(let i=ENEMIES.length-1;i>=0;i--)if(ENEMIES[i].dlc===DLC_ID)ENEMIES.splice(i,1);try{return BASE_DLC_START_COMBAT(elite)}finally{ENEMIES.splice(0,ENEMIES.length,...original)}};
const BASE_DLC_START_BOSS=startBoss;
startBoss=function(){const original=BOSSES.slice();if(!dlcUnlocked())for(let i=BOSSES.length-1;i>=0;i--)if(BOSSES[i].dlc===DLC_ID)BOSSES.splice(i,1);try{return BASE_DLC_START_BOSS()}finally{BOSSES.splice(0,BOSSES.length,...original)}};
const BASE_DLC_MAKE_REWARDS=makeRewards;
makeRewards=function(count){const oi=ITEMS.slice(),or=RELICS.slice();if(!dlcUnlocked()){for(let i=ITEMS.length-1;i>=0;i--)if(ITEMS[i].dlc===DLC_ID)ITEMS.splice(i,1);for(let i=RELICS.length-1;i>=0;i--)if(RELICS[i].dlc===DLC_ID)RELICS.splice(i,1)}try{return BASE_DLC_MAKE_REWARDS(count)}finally{ITEMS.splice(0,ITEMS.length,...oi);RELICS.splice(0,RELICS.length,...or)}};
const BASE_DLC_ENTER_NODE=enterNode;
enterNode=function(n){const oe=EVENTS.slice();if(!dlcUnlocked())for(let i=EVENTS.length-1;i>=0;i--)if(EVENTS[i].dlc===DLC_ID)EVENTS.splice(i,1);try{return BASE_DLC_ENTER_NODE(n)}finally{EVENTS.splice(0,EVENTS.length,...oe)}};

const BASE_DLC_START_RUN=startRun;
startRun=function(cls,asc,seed,subclass='auto',loadout='none',modifier='normal'){if(CLASSES[cls]?.dlc===DLC_ID&&!dlcUnlocked()){openDlcActivation();return}BASE_DLC_START_RUN(cls,asc,seed,subclass,loadout,modifier);const sub=SUBCLASSES[cls]?.[S.profile?.subclass];if(sub?.bonus?.crit&&S.p)S.p.crit+=sub.bonus.crit;if(S.p)S.p.dlcFirstSkillUsed=false;recomputeBuild();save();render()};

const BASE_DLC_APPLY_ITEM=applyItem;
applyItem=function(it){BASE_DLC_APPLY_ITEM(it);if(it?.dlc===DLC_ID&&it.hp&&S.p){const m=RARITY[it.rarity]?.mul||1,hp=Math.round(it.hp*m);S.p.max+=hp;S.p.hp+=hp;it.__bonus=it.__bonus||{};it.__bonus.hp=hp}};
const BASE_DLC_SCRAP_ITEM=scrapItem;
scrapItem=function(i){const it=S.inventory[i];if(!it)return;const hp=it.__bonus?.hp||0;BASE_DLC_SCRAP_ITEM(i);if(hp&&S.p){S.p.max=Math.max(1,S.p.max-hp);S.p.hp=Math.min(S.p.hp,S.p.max)}save()};

const BASE_DLC_USE_SKILL=useSkill;
useSkill=function(id){const sk=SKILLS[id];if(!sk||sk.dlc!==DLC_ID)return BASE_DLC_USE_SKILL(id);if(!dlcUnlocked()){toast('Этот контент доступен после активации DLC.');return}if(!canAct())return;const p=S.p,e=enemy(),effectiveCost=sk.cost+(hasRelic('riftHeart')?1:0);if(p.mp<effectiveCost){toast('Недостаточно MP');return}p.mp-=effectiveCost;let d=0,skillBonus=1;if(id==='rift'){d=dmgCalc(p,e,sk.base,true)*skillBonus;dealPlayerDamage(Math.floor(d),'Разлом');addStatus(e,'slow',2)}else if(id==='voidpulse'){d=dmgCalc(p,e,sk.base,true)*skillBonus;dealPlayerDamage(Math.floor(d),'Импульс Бездны');const st=R.pick(['burn','poison','bleed']);addStatus(e,st,3+(st==='burn'&&hasItem('voidstaff')?1:0));if(hasRelic('abyssLantern'))addStatus(e,st,4)}else if(id==='echo'){for(let i=0;i<2;i++){d=dmgCalc(p,e,sk.base,true)*skillBonus;if(p.combo>=5&&hasRelic('echoCrown'))d*=1.25;dealPlayerDamage(Math.floor(d),'Эхо Бездны');if(e.hp<=0)break}p.combo=Math.min(9,p.combo+2);p.mp=Math.min(p.maxmp,p.mp+2+(hasItem('echoRing')?1:0))}else if(id==='devour'){d=dmgCalc(p,e,sk.base)*skillBonus;dealPlayerDamage(Math.floor(d),'Поглощение');const healed=Math.floor(Math.max(0,d)*.15*(1+(hasItem('awakeningAmulet')?.20:0)));if(healed>0)heal(healed)}else if(id==='collapse'){d=dmgCalc(p,e,sk.base,true)*skillBonus;if((e.statuses||[]).length)d*=1.30;if(hasRelic('awakeningSeal'))d*=1+Math.min(.30,(e.statuses||[]).length*.06);if(p.combo>=5&&hasRelic('echoCrown'))d*=1.25;dealPlayerDamage(Math.floor(d),'Схлопывание');p.hp=Math.max(1,p.hp-Math.ceil(p.max*.06))}if(hasItem('riftBoots'))p.dlcFirstSkillUsed=true;if(e.hp>0)endPlayerTurn();else winCombat()};

const BASE_DLC_DMG_CALC=dmgCalc;
dmgCalc=function(att,def,mult=1,magic=false){let d=BASE_DLC_DMG_CALC(att,def,mult,magic);if(att===S.p&&dlcUnlocked()){if(magic){if(hasItem('riftblade'))d*=1.05;if(hasRelic('riftHeart'))d*=1.12;if(hasRelic('echoCrown')&&S.p.combo>=5)d*=1.25;if(hasRelic('awakeningSeal'))d*=1+Math.min(.30,(def.statuses||[]).length*.06)}if(S.p.tempDlcAtk){d*=1+S.p.tempDlcAtk;S.p.tempDlcAtk=0}if(hasItem('echoDagger')&&S.p.combo>=5)d*=1.10;if(hasItem('riftBoots')&&!S.p.dlcFirstSkillUsed)d*=1.20}return Math.max(1,Math.floor(d))};
const BASE_DLC_END_TURN=endPlayerTurn;
endPlayerTurn=function(){BASE_DLC_END_TURN();if(dlcUnlocked()&&S.screen==='combat'&&S.p){if(hasItem('voidMantle')&&S.combat.turn%3===0)S.p.mp=Math.min(S.p.maxmp,S.p.mp+3);if(hasItem('echoRing')&&S.p.combo>=2)S.p.mp=Math.min(S.p.maxmp,S.p.mp+1);if(hasRelic('echoStone')&&S.p.combo>=4&&S.combat.turn%3===0)heal(Math.floor(S.p.max*.04))}};
const BASE_DLC_WIN_COMBAT=winCombat;
winCombat=function(){const wasDlcEnemy=!!enemy()?.dlc;const beforeInventory=(S.inventory||[]).filter(x=>x.dlc===DLC_ID).length;BASE_DLC_WIN_COMBAT();if(dlcUnlocked()&&wasDlcEnemy){addLog('🌑 Победа над врагом DLC.','good');if(hasItem('abyssCore')&&enemy()?.elite){S.p.max=Math.floor(S.p.max*1.05);S.p.hp=Math.min(S.p.max,S.p.hp+5)}}if(dlcUnlocked()&&beforeInventory>=5)awardAchievement('dlcCollector')};
const BASE_DLC_SET_INTENT=setIntent;
setIntent=function(){const e=enemy();if(e?.id==='awakeningAvatar'&&dlcUnlocked()){const pool=e.phase===1?['attack','special','burn']:e.phase===2?['crit','special','heal']:['special','crit','burn','attack'];e.intent=R.pick(pool);return}BASE_DLC_SET_INTENT()};

const BASE_DLC_EXPANDED_CITY=expandedCityScreen;
expandedCityScreen=function(){const h=BASE_DLC_EXPANDED_CITY();const box=dlcUnlocked()?`<div class="card"><h2>🌑 Пробуждение Бездны</h2><div class="cityStatus good">✓ DLC активно</div><button class="btn" onclick="setScreen('start');render()">🌑 Начать забег Пробуждённым</button></div>`:`<div class="card"><h2>🌑 Пробуждение Бездны</h2><div class="cityStatus">Платное DLC • ${DLC_PRICE_RUB} ₽</div><button class="btn primary" onclick="openDlcActivation()">🔓 Купить / активировать DLC</button><div class="small muted">Новый класс, подклассы, навыки, предметы, реликвии, враги, босс, события, достижения и записи кодекса.</div></div>`;return h+box};
const BASE_DLC_START_SCREEN=startScreen;
startScreen=function(){const h=BASE_DLC_START_SCREEN();const extra=dlcUnlocked()?`<div class="card"><h2>🌑 DLC: Пробуждение Бездны</h2><div class="cityStatus good">✓ Активировано</div><button class="btn primary" onclick="openStart('awakened')">🌑 Выбрать Пробуждённого</button></div>`:`<div class="card"><h2>🌑 DLC: Пробуждение Бездны</h2><div class="cityStatus">🔒 Заблокировано • ${DLC_PRICE_RUB} ₽</div><button class="btn" onclick="openDlcActivation()">🔓 Купить / активировать</button></div>`;return h+extra};
const BASE_DLC_OPEN_START=openStart;
openStart=function(cls){if(CLASSES[cls]?.dlc===DLC_ID&&!dlcUnlocked()){openDlcActivation();return}return BASE_DLC_OPEN_START(cls)};
const BASE_DLC_END_SCREEN=endScreen;
endScreen=function(win){const h=BASE_DLC_END_SCREEN(win);if(dlcUnlocked()&&win&&S.cls==='awakened'){if((SYNERGIES||[]).some(x=>tagCount(x.tag)>=x.need&&['magic','combo','risk'].includes(x.tag)))awardAchievement('dlcBuild');if(S.inventory.filter(x=>x.dlc===DLC_ID).length+S.relics.filter(x=>x.dlc===DLC_ID).length>=5)awardAchievement('dlcCollector');awardAchievement('dlcClass')}return h};
const BASE_DLC_CODEX=codexScreen;
codexScreen=function(){if(dlcUnlocked())return BASE_DLC_CODEX();const original=CODEX_ENEMIES.slice();for(let i=CODEX_ENEMIES.length-1;i>=0;i--)if(CODEX_ENEMIES[i].dlc===DLC_ID)CODEX_ENEMIES.splice(i,1);let h;try{h=BASE_DLC_CODEX()}finally{CODEX_ENEMIES.splice(0,CODEX_ENEMIES.length,...original)}return h+`<div class="card"><h2>🌑 Пробуждение Бездны</h2><div class="cityStatus">🔒 Записи DLC скрыты до активации.</div><button class="btn" onclick="openDlcActivation()">🔓 Активировать DLC</button></div>`};
"""
text = text[:-len(marker)] + dlc + '\n' + marker
p.write_text(text, encoding='utf-8')
print('Paid DLC v1 applied')
