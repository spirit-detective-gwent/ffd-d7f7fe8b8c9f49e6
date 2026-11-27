# v6564-angry — angry portrait variants (GGD angry)
Branch v6564-angry off main e1ba0d4, worktree /workspace/angry/wt. Never push/publish.
Scratch: /workspace/angry (ref/ = neutral PNGs, raw/ = generated 864x1152, out/ = 360x480 webp, tools/).

## Existing mechanism (main)
- PT_PAINT maps speaker id -> paint id; PT_HAS lists files portraits/<id>_<mood>.webp.
- ptMoodOf(who,opt,txt): opt.mood > kneel=beaten > {shout}/opt.shout=angry (rage if hype) > calm if <id>_calm exists > neutral.
- ptPaintUrl(who,mood): fallback chain, angry -> calm -> neutral. So adding <id>_angry + PT_HAS turns on every
  existing {mood:'angry'} / {shout} NPC line for free.
- dlgFaceStyle(key) (versus/choice boxes) zooms IMG[*_fig]; never painted. Fixed here (and on v6564-sukajan).
- Bosses already had angry/calm/beaten: bando goda gouki jin kagero kaneda kurata mai masa mizuno nails saeki shigure (+kaji, sada).

## Plan
1. Code: ptMoodOf scene rules (PT_ANGRY_SC by scene id, PT_ANGRY_LN text snippets per speaker), versus box -> angry,
   actSay text-aware, lazy per-scene preload of angry files.
2. Paint <id>_angry for every neutral-only NPC except the sukajan set.
3. Sukajan set pending until its neutrals land: c2punk(+Y2/Y3) c2hustler c2boso goda(angry redo) sabu nao nurse sota haru, nami, tatsumi.

## Log

### Slam gate (v6.5.64)
`scene()` still paints the angry bust whenever `ptMoodOf` returns angry/rage (tagged line, table hit, or scene rule). `ptSlam` now fires only when the line itself is explicitly angry or shouted: `ln[2].mood === 'angry'`, `ln[2].shout`, `{shout}` in the raw text, or mood is `rage`. Table-only angry lines (including an explicit `{mood:'neutral'|'calm'}` that the table overrules) swap the face with no slam.

Verified 10/10 in /workspace/angry/tools/slam_check.py (hook on ptSlam, one evaluate per line):
- no slam: chinpira table toll, nurse "Try losing less.", Genji scold with `{mood:'neutral'}` overruled by the table, c2_boso opener, Genji "Sit tight." stays neutral, Gōda `{mood:'calm'}`.
- slam: explicit `{mood:'angry'}`, `{shout}` in text, `{shout:1}`, explicit `{mood:'rage'}` (kind rage).
- All expected faces and moods matched; no page errors.


## Angry lines (v6564-angry)

Mechanism: `ptMoodOf(who, opt, txt, sceneId)` -> angry when the line is tagged {mood:'angry'} / {shout} (as before), OR its text matches `PT_ANGRY_LN[paintId]` (substring), OR `PT_ANGRY_SC[sceneId]` lists the speaker (empty for now; hook for per-scene rules). An explicit {mood:'neutral'|'calm'} is overruled only by the table; sad/happy/beaten/rage tags win. Ryo/Aoi never. Versus boxes (dialog opt.versus) default to the angry bust unless the ally is in `PT_VS_CALM` (Genji, Nurse, Tsukikage). Missing file -> calm -> neutral fallback (ptPaintUrl).
Lazy load: `ptPreloadScene(id, L)` at scene start warms only that scene's angry busts (one Image per URL, cached in PT_PRE); versus faces call ptPreload on open. No loops/timers.
Already angry before this branch (tagged lines): chinpira x4, bouncer, drum, student x2, masa x2, bando, gouki/jin/masa/bando/student/drum {shout} lines; boss splash/vs cards use <boss>_angry.

Classified from 901 NPC lines (tools/lines.py -> lines.json; picks.txt = line indices). 188 lines marked angry:
- **chinpira** (7): You think I feel like talking? Jin owns the club. That is all you get. | Watched you on six screens, kid.{p} {slow}You fight like you owe somebody.{/slow} | You think this is my club? Jin owns it. He'll hear about this. | My Thursday crates never showed.{p} {slow}Somebody talked.{/slow} | I’m the guy in the middle. Middle pays best. | Oi, schoolboy. This street charges a toll. | Make me. …Yeah. Thought so.
- **c2suit** (13): Door's shut. Walk. | Neither is the door. | Door’s shut. Jin’s orders. | Come back when the floor forgets your face. | Children. In our lights. | The club doesn't take kids. | Someone lose their students? | Run along. Grown-ups are talking. | A boy and a girl playing city. | You're in over your heads. | We'll see. | You can try to keep it. | You're a long way from the arcade.
- **ckdealer** (1): Count's not finished.
- **bouncer** (4): Office is past me. | Members only tonight. Walk on. | Club’s closed to schoolkids. Walk on. | Leave him. Boss is waiting.
- **c2hustler** (20): Hey. Gym kids. You lost? | Go back to Genji. This street isn't for you. | A boy and a girl. Cute. | Run home before someone taxes you. | Kurogane's sending children now? | You two wouldn't last a round down here. | You're on the wrong street. | Plaza's ours tonight. | Hey. You two lost? | This street isn't for you. | A boy and a girl on our wall. | You two wouldn't last a round down here. | Heard Nails sent kids. | Nails sends schoolkids now? | Cute. | Hah… you think the wall matters? | The bathhouse. By the station. Ask for Kaneda. He’ll ask for your teeth. | Staff only, kids. The old lady stays in the kitchen. | Boss says she stays out of the cold. We say she stays out of the way. | Steam’s private now. Pay or shiver.
- **c2punk** (9): School's that way, kids. | Or did the uniforms scare you off? | Look. Freshmen. | Walk on, little foxes. This wall's taken. | You two playing gang tonight? | Cute. Go finish your homework. | We live here. Push up. | Keep your bikes off this walk. | And you're a long way from the club.
- **c2boso** (13): Kids on our street. Cute. | You can't even reach a peg. | You hear a bike and flinch, schoolboy. | Take her home before the freight rolls. | Freight's no place for children. | Keep moving, both of you. | Then move. | Suits don't belong down here. | Punks on Masa’s row? | Punks on the bridge? This freight is Masa’s. | Second bike. You already hit the first? | Last bag of the night. You want it, you take it off me. | Schedule’s sacred. You’re late for a bruise.
- **gekko** (3): Not now. | You again. Still slow. | This shop’s under Gōda now. I don’t owe Nails a thing.
- **graycoat** (1): {quiet}Keep walking.{/quiet}
- **bully2** (2): Class is over. Everything’s over. Gouki says so. | {quiet}Shhh.{/quiet} Library rules. {slow}Say it with us: I will be quiet.{/slow}
- **bully4** (3): Look who walked in. The delinquent and a new girl. | Again. Five hundred times. “I will be quiet.” | Then you’ll be quiet sooner.
- **student** (1): Wrong office, Kazan.
- **bully3** (1): Wrong answer.
- **gouki** (11): Come earn it inside. I’m not your errand. | {slow}Still standing. Still mine.{/slow} | Solo strikes never outlast this. | {slow}Still standing. Still mine.{/slow} | Solo strikes never outlast this. | {slow}Still standing. Still mine.{/slow} | Solo strikes never outlast this. | {slow}How many times can you bleed?{/slow} | {slow}How many times can you bleed?{/slow} | {slow}How many times can you bleed?{/slow} | You walked my halls. Good.{p} {slow}Now earn the rest.{/slow}
- **shigure** (10): Turn around. This alley’s paid for. | Back again. You learn anything? | Third time. I respect that. Doesn’t change the ending. | {slow}Name’s Ban.{/slow}{p=600} Remember who put you down. | You telegraph that punch. I saw it from Lucky 7. | Two of you, and you still swing alone. | Kazan.{p=500} {slow}You fight like I used to.{/slow}{p} Not a compliment. | You eat every hit whole. A fight isn’t one punch. | The coat pays me to keep this door. | {slow}Show me.{/slow}
- **nails** (11): Students. Toll’s a hundred yen a step. | {slow}Wouldn’t you like to know.{/slow} Everyone pays me now. | {slow}Then I decide what you are.{/slow} | Gekko’s street. Weeks of nothing. And you said ‘slow.’ | Tell the street what skimming costs. | Students. Toll’s a hundred yen a step. You owe me thirty steps. | Bold. I like bold. It bruises nicely. | Sneaking in my arcade? That’s extra. | Loud kid. Let’s make you quiet. | Students. Toll’s a hundred yen a step. | {slow}A gray coat who understands hunger.{/slow} Everyone pays me now.
- **goda** (13): {slow}Forty years I heated that water. Now it’s mine.{/slow} | Then you read my mail. Kids today. | Then you read my mail. Kids today. | Then you read my mail. Kids today. | …{p=500}{slow}The seal keeps the fire lit, boy.{/slow}{p=600} Break it and this alley has  | An ōzeki doesn’t step out of the ring.{p} {slow}Come.{/slow} | Bath’s closed. Forty years I heated that water. Now it’s his. | Towel off and leave, children. | Kicking a sentō door. Your grandfather would weep. | I can smell you in the steam, child. | Polite. Fine. Polite gets a fair fight. | {slow}Forty years I heated that water. Now it’s mine.{/slow} | He gave me a seal. I gave him quiet. Towel off.
- **kagero** (6): Two children.{p} {slow}Four of my seals in your pockets.{/slow} | Four locks broken by two children. The Wardens are slipping. | Kagerō. I only gave this city what it wanted. A lock on every door. | Two children.{p} {slow}Four of my seals broken.{/slow} | {slow}Did you think I worked alone?{/slow} | There are more of us.{p} Come prove you can climb.
- **kaneda** (9): Members, family, and people Gōda owes money.{p} You’re none of those. | Then you’re the reason I’m working tonight. | {slow}Observant.{/slow} Doesn’t open the door. | You again. Upstairs is the boss’s house. | …Then you know he’s not going to let you through. Neither am I. | Make me. | {slow}You counted.{/slow} Good. Count your teeth after. | Plenty of kids tried that. | The door is me.
- **masa** (10): You used a late load to walk my yard. | The shutter is mine. You want it, you come get it. | You read a board. You have not read the yard. | Honest freight still goes through me. The shutter stays shut. | End of the line. The lift does not move without my seal. | You do not use my paperwork against me. | I said no. The schedule never stops. | Night freight. Gray crates, no questions. You’re a question. | Rats in the crates again. | You’re a question. Off my dock.
- **mizuno** (1): {quiet}You came through my library. You unplugged my readers.{/quiet}{p} That was very lou
- **mai** (1): You broke my section.{p} {slow}Three players, gone off tempo.{/slow}
- **kurata** (1): You threw out my bread.{p} {slow}Three whole crates.{/slow}
- **bando** (1): {slow}Who put a third hurdle on my track?{/slow}
- **jin** (6): New challengers. I’ve got the top score on every cabinet here. | He lost. Losers pay. House rules. | Rude. You don’t touch another player’s session. | Reading me? Two can play. | New challenger? Cute. Insert coin. | He lost. Losers pay. House rules — and I don’t lose.
- **genji** (15): Hands off my gear until we’ve talked, kid. | Hands off my gear until we’ve talked, kid. | You’re not bleeding. Save my tape for when you are. | Either way: it took two of you for Gouki. Don’t get cute. | Sit.{p} Then get up. | Sit.{p} Then get up. | Sit.{p} Then get up. | Sit.{p} Then get up. | Sit.{p} Then get up. | Sit.{p} Then get up. | Sync Break. Your partner is not furniture. | Sync Break. Your partner is not furniture. | Losing three times isn’t the problem. Not knowing WHY is. Get up. | I’m not fighting your fights for you. I show you once. You two work it out on each other. | “Two of you, still swinging alone.” Ban’s words. Fix that.
- **nurse** (4): Not yet. Sit. Let me see that hand. | Your pride is your own problem. | Back with us? You look terrible. Hold still. | Try losing less.
- **tsukikage** (8): Your color’s fine. Off you go. Don’t come back bleeding. | Good. Now stop collecting bruises. | Because you keep earning it. | I know. Your kind always is. | Spirit burns love cold bodies. Move. | Come back a quarter dead. | You are on your feet. I do not pour a full cup for a faint. | You are on your feet. I do not pour a full cup for a faint.
- **oda** (3): You’ll pay twice, then. Machi next door has the bay open again too. | It’s noodles, boy. Machi next door has the bay open again too. | It’s noodles. Don’t push it. Machi next door has the bay open again too.

Calm lines kept neutral: Genji lessons/briefings, Nurse directions, Tsukikage herb/shop talk, quest-givers (Mina, Attendant, Courier, Tetsuo, Kenta, Aya, Riku, Yuto), beaten/defeated lines, boss backstory/calm lines.

### Tests (after slam commit 957ba4b)
Reran /workspace/angry/run_tests.sh from the worktree; verify_wired from /workspace/v6560-review/portraits. All green:
- verify_wired: PASS (every checked Ch2 speaker has a painted portrait)
- ngp: 104/104
- s2: 167/167
- bond: 109/109
- yk no_old_art: PASS
- yk ch_smoke: PASS
Did not add tools/ngp/shots/.

