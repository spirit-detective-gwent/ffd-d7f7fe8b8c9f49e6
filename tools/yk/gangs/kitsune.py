from sheets import *
E='ext/'
KP=[('#9e1b2f','Kitsune crimson (gang colour)'),('#1b1920','Club black'),('#e2b33a','Fox gold (crest, pins, buttons)'),('#c0242f','Kumadori red (fox mask markings)')]
sheet('mb2_game','ksJin','"High-Score" Jin  (mb2_game)','Club Kitsune / Syndicate boss  -  Game Center',
  [('#efece6','White satin bomber'),('#9e1b2f','Crimson trim, crest ring, headphone cups'),('#1b1920','Black tee and slacks'),('#e2b33a','Gold chain + coin, gold fox crest'),('#b51f30','Crimson streaks in a black pompadour')],
  ['The boss of the Game Center, so he is the only Kitsune man in white: a white satin bomber with the gang crimson on the collar band and ribbed hem, and a big gold fox mask in a crimson ring across the back.',
   'Arcade king details from his card text: headphones (worn round the neck, DJ style, crimson cups with gold rings) and two-tone hair (a black pompadour with crimson streaks combed through the quiff). Gold chain with a coin on a black tee.',
   'Built a little heavier than a Suit (bulk 0.18), black slacks, white sneakers. His current in-game art is a blue pinstripe suit, while his card says neon-green bomber; this look keeps the bomber/headphones/two-tone idea in Kitsune colours. If wired, CXD.mb2_game.a should be updated to match.'],
  E+'old_mb2_game_fig.webp',E+'old_mb2_game_walk.webp')
sheet('bouncer','ksBouncer','Black-Suit Bouncer  (bouncer)','Club Kitsune lieutenant  -  the club door',
  [('#25232b','Black double-breasted suit'),('#9e1b2f','Crimson shirt'),('#6e0f1e','Dark crimson tie'),('#36333d','Lapel facing'),('#e2b33a','Gold buttons + gold fox lapel pin')],
  ['Kitsune lieutenant and a Heavy-Guard Bruiser, so he is built as a wall: bulk 0.75 (just above Flip, below Goda), shaved head with a shine, black shades.',
   'Keeps his name: a black double-breasted suit, now with the gang crimson shirt and a dark crimson tie, gold buttons and a small gold fox pin on the lapel. Same suit cut as the Suits so he reads as their senior, but black instead of crimson.',
   'His current art is a unique slim painted figure (tall 245x760 fig); this redraws him in the same cel pass as the rest of Ch2.'],
  E+'old_bouncer_fig.webp',E+'old_bouncer_walk.webp')
sheet('c2_suit_a','ksSuit','Kitsune uniform A: "Suit"  (c2_suit)','Club Kitsune rank and file  -  floor enforcers',
  KP+[('#7a1323','Lapel facing')],
  ['Uniform A, the enforcers on the club floor and at the pass: a crimson double-breasted suit (gold buttons), black shirt, gold tie, gold fox lapel pin, black slacks and shoes, a black punch perm (the classic yakuza cut), tinted shades.',
   'Matches the card text (double-breasted, tinted shades) and the Heavy-Guard Bruiser role. Every Suit wears the same uniform; only Jin and the Bouncer are unique.'],
  E+'old_c2_suit_fig.webp',E+'old_c2_suit_walk.webp')
sheet('c2_suit_b','ksRun','Kitsune uniform B: "Runner"  (second Kitsune sub-group)','Club Kitsune rank and file  -  game-floor runners',
  KP,
  ['Uniform B, the younger runners who work the Game Center floor and the back alley: crimson satin bomber with a black collar band and ribbed hem, the gold Kitsune fox mask across the back, a black tee, black slacks, white sneakers, slicked-back wine-black hair.',
   'Same three colours as the Suits (crimson, black, gold), and both uniforms are crimson from the waist up, so the gang reads as one colour from across the street; the Bouncer (black) and Jin (white) stand out as the two unique ranks. If you only want one uniform, this one can be dropped and every c2_suit uses uniform A.'],
  None)
sheet('n13sb','sabu','Sabu  (n13sb)','Nails\' Punk crew  -  the youngest, the one Nails knocks down',
  [('#6a35a0','Punk purple sukajan (crew colour)'),('#f0c040','Gold sukajan embroidery (kept from the old jacket)'),('#f1ece0','White tee'),('#3e2a5c','Dark purple bontan'),('#3a2a20','Dark brown pompadour'),('#e08a32','Orange bleached streaks'),('#c9b48a','Tan setta / sneakers')],
  ['Still in the Punks\' purple so he is clearly Nails\' crew, but the junior: a short purple sukajan (the gold embroidery of the old Sukajan Punk jacket kept on purpose) instead of a long tokkofuku coat, a plain white tee, dark purple bontan, tan shoes, no shades.',
   'A smaller pompadour with orange bleached streaks (a kid copying Punk C\'s bleach job), a plaster across his nose, slightly slimmer frame than the other Punks (bulk -0.08).',
   'His lie/KO sheets would come from the same spec, so the knock-down beat keeps the look.'],
  E+'n13sb_fig.webp',E+'n13sb_walk.webp')
