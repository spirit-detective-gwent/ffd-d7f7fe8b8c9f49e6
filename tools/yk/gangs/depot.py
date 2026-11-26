from sheets import *
E='ext/'
DP=[('#e8661c','Hi-vis orange (gang colour)'),('#2c2e33','Depot charcoal'),('#d9dfe2','Reflective tape'),('#ff7a1e','Orange embroidery (YORU-HASHIRU "night run")')]
sheet('mb2_depot','dpMasa','Foreman Masa  (mb2_depot)','Depot boss  -  runs the night freight under the canal',
  DP+[('#f0c419','Yellow hard hat (orange stripe)'),('#1a1a1e','Black jika-tabi')],
  ['Keeps what his card says (orange coverall, reflective bands, yellow hard hat) and adds the gang\'s bosozoku side so he reads as their boss: an open charcoal tokkofuku thrown over the coverall, orange lining, and the gang motto YORU-HASHIRU ("night run", the kanji on the coat) embroidered in orange on the back and the coat fronts.',
   'Built heavy (bulk 0.95, between Flip and Goda), baggy nikka work trousers, reflective tape across the chest and shins, hard hat with an orange band. He is the only Depot man who wears both halves of the gang (the riders\' coat and the dock crew\'s coverall).'],
  E+'old_mb2_depot_fig.webp',E+'old_mb2_depot_walk.webp')
sheet('c2_boso_a','dpRider','Depot uniform A: "Rider"  (c2_boso)','The Depot\'s bosozoku  -  the night-run bikers',
  [DP[0],DP[1],DP[3],('#f3f1ec','White surgical mask'),('#f1ece0','Sarashi')],
  ['Uniform A, the bikers: a long charcoal tokkofuku with orange lining and YORU-HASHIRU ("night run", the kanji on the coat) stitched in orange down the back and on both front panels, sarashi wrap, charcoal bontan, a black pompadour under an orange hachimaki, and the bosozoku white mask.',
   'Replaces the old purple coats, which clashed with Nails\' Punks. Orange + charcoal is nowhere else in Ch2 (Punks purple, bath-house indigo/brown, Kitsune crimson).'],
  E+'old_c2_boso_fig.webp',E+'old_c2_boso_walk.webp')
sheet('c2_boso_b','dpDock','Depot uniform B: "Dock hand"  (second Depot sub-group)','The Depot\'s freight crew  -  the men on Masa\'s dock',
  [DP[0],DP[1],DP[2],('#1a1a1e','Black jika-tabi')],
  ['Uniform B, the freight crew: a hi-vis orange coverall (tsunagi) open on a charcoal tee, reflective tape across the chest and shins, baggy nikka trousers like Japanese site workers wear, black jika-tabi, slicked hair under a charcoal tenugui headband.',
   'Same orange + charcoal + reflective tape as the Riders and Masa. If you only want one uniform, this one can be dropped and every c2_boso uses uniform A.'],
  None)
