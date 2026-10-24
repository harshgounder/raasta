# HINDI-CHECK: every Hindi line, so a native speaker can verify in two minutes

hermes, 2026-10-24 23:45 IST, research and copy only. Scope: `story/STORY-v2.md` and
`research/hermes/sc02/WHATIF-WALL.md`.

Two honest notes before the table.
- `STORY-v2.md` contains Hindi only in romanised form, no Devanagari at all (checked with a proper Unicode
  range search, zero lines). The Devanagari column below is my rendering of those romanised lines.
- `WHATIF-WALL.md` contains no Hindi yet, also zero Devanagari lines. Its 15 entries are questions, so I have
  drafted the Hindi for them here rather than pretending they already exist. All of it needs a native read,
  and I would rather say that than let the team assume my Hindi is checked.

Column meanings: **romanised** is what is on disk or what I would put on disk, **Devanagari** is for the
site, **plain English** is what a judge should understand from the line.

## Part 1, story lines (from `STORY-v2.md`, beats 1 to 8)

| # | where | romanised (as on disk) | Devanagari | plain English | note |
|---|---|---|---|---|---|
| S1 | line 1, title and tagline | Isse kuch nahi hoga | इससे कुछ नहीं होगा | This won't do anything | the double meaning is the whole story: before the route it means "useless", after it means "nothing bad will happen" |
| S2 | line 9, old man's reply | Haan, sahi kaha | हाँ, सही कहा | Yes, you are right | deadpan agreement, not sarcasm |
| S3 | line 9, after each hurdle | Isse humein kuch nahi hoga | इससे हमें कुछ नहीं होगा | With this, nothing will happen to us | the payoff line, must land identically to S1 |
| S4 | beat 1, caption | Map pe sab saaf dikhta hai | मैप पे सब साफ़ दिखता है | On the map, everything looks clear | "map" stays English in Hindi speech, that is how people say it |
| S5 | beat 2, bird lift 1 | Upar se dekho. Ye raasta nahi, ek bhool-bhulaiya hai | ऊपर से देखो। ये रास्ता नहीं, एक भूल-भुलैया है | Look from above. This is not a path, it is a maze | "bhool-bhulaiya" is the word a grandparent would use, keep it |
| S6 | beat 4, old woman | Wahi map. Wahi raasta | वही मैप। वही रास्ता | Same map. Same route | four words, two beats, do not expand |
| S7 | beat 5, kid's question | Dadu, sab log normal map use karte hain. Ye kyun? Isse kuch nahi hoga | दादू, सब लोग नॉर्मल मैप इस्तेमाल करते हैं। ये क्यों? इससे कुछ नहीं होगा | Dadu, everyone uses the normal map. Why this? This won't do anything | "normal map" stays English, it is the generic-map label |
| S8 | beat 6, bird lift 2 | Har jaal ka raasta | हर जाल का रास्ता | A way around every trap | ties to the dungeon-map visual |
| S9 | beat 8, kid at arrival | Kuch nahi hua | कुछ नहीं हुआ | Nothing happened | the mirror of S1, must be delivered flat |
| S10 | beat 8, old man | Isiliye toh. Isse humein kuch nahi hoga | इसीलिए तो। इससे हमें कुछ नहीं होगा | That is exactly why. With this, nothing will happen to us | two sentences, pause between them |
| S11 | beat 8, tagline on screen | RAASTA. Isse kuch nahi hoga | रास्ता। इससे कुछ नहीं होगा | RAASTA. Use it and nothing goes wrong | brand word stays Latin on screen, Devanagari only if the lockup is bilingual |

Translation cautions a checker should confirm.
1. **S1 against S3 and S10.** The joke only works if the Hindi is identical in all three. If a translator
   "improves" one of them, the story collapses.
2. **Dadu versus Dadaji.** The file uses both. Pick one and use it in the subtitle and the voice line.
3. **"kuch nahi hoga" versus "kuch nahi hua".** Present tense warning versus past tense result. Do not
   normalise them into the same phrase, the contrast is the point.
4. **RAASTA spelled in Devanagari** would be रास्ता, which simply means "path" and loses the brand. Keep the
   wordmark Latin, and if a Devanagari tagline is needed, put the brand in Latin and the sentence in Devanagari.

## Part 2, the 15 what-if questions (drafted by me, none on disk yet)

| # | romanised | Devanagari | plain English |
|---|---|---|---|
| W1 | Barish ho rahi ho to kya | बारिश हो रही हो तो क्या | What if it is raining |
| W2 | Photo raat mein li gayi ho to kya | फ़ोटो रात में ली गई हो तो क्या | What if the photo was taken at night |
| W3 | Gaay footpath par baith jaye to kya | गाय फुटपाथ पर बैठ जाए तो क्या | What if a cow sits on the footpath |
| W4 | Dukaan wala shaam paanch baje stall laga de to kya | दुकान वाला शाम पाँच बजे स्टॉल लगा दे तो क्या | What if a shop puts its stall out at five |
| W5 | Footpath hi na ho to kya | फुटपाथ ही न हो तो क्या | What if there is no footpath at all |
| W6 | Footpath toota ho aur koi theek na kare to kya | फुटपाथ टूटा हो और कोई ठीक न करे तो क्या | What if the footpath is broken and nobody fixes it |
| W7 | Log footpath par gaadi khadi kar dein to kya | लोग फुटपाथ पर गाड़ी खड़ी कर दें तो क्या | What if people park on the footpath |
| W8 | Poori gali mein paani bhar jaye to kya | पूरी गली में पानी भर जाए तो क्या | What if the whole street floods |
| W9 | Raasta chadhai wala ho ya seedhiyan hon to kya | रास्ता चढ़ाई वाला हो या सीढ़ियाँ हों तो क्या | What if the road is steep or has steps |
| W10 | Malba pada ho to kya | मलबा पड़ा हो तो क्या | What if there is rubble lying there |
| W11 | Thela aada khada ho to kya | ठेला आड़ा खड़ा हो तो क्या | What if a cart is parked across the path |
| W12 | Raasta itna patla ho ki guzar na paun to kya | रास्ता इतना पतला हो कि गुज़र न पाऊँ तो क्या | What if the path is too narrow to pass |
| W13 | Photo saalon purani ho to kya | फ़ोटो सालों पुरानी हो तो क्या | What if the photo is years old |
| W14 | Raat mein poora bazaar sadak par aa jaye to kya | रात में पूरा बाज़ार सड़क पर आ जाए तो क्या | What if the whole market spills onto the road at night |
| W15 | Kinara ooncha ho aur ramp photo se bahar ho to kya | किनारा ऊँचा हो और रैंप फ़ोटो से बाहर हो तो क्या | What if the kerb is high and the ramp is outside the photo |

## Part 3, the terminology decisions someone must make once

| English | choices in play | my recommendation | why |
|---|---|---|---|
| footpath | फुटपाथ, पैदल रास्ता, फुटपाथ (दिल्ली) | फुटपाथ | it is what people say, and it matches the English word the site already uses |
| kerb | किनारा, कर्ब, साइड | किनारा on the page, कर्ब in a technical line | "किनारा" reads naturally in a warning; "कर्ब" is precise in a measurement |
| ramp | रैंप, ढलान | रैंप | ढलान means any slope, and the point is the built ramp |
| route | रास्ता, मार्ग | रास्ता | मार्ग sounds official, and the product talks to a family, not a clerk |
| barrier | बाधा, रुकावट | रुकावट | बाधा is abstract, रुकावट is the thing that stops you today |
| confidence | भरोसा, विश्वास | भरोसा | it is evidence confidence, not faith, and भरोसा fits "how much we trust the photo" |

## Checker's two-minute routine

1. Read S1, S3 and S10 in Devanagari out loud. If they do not sound like the same sentence said twice, the
   story joke is broken, flag it.
2. Read S7 and confirm a child would say it, not a newsreader.
3. Read W1 to W15 and mark any line you would not say to your own grandmother.
4. Confirm the terminology table, then the copy lane can apply it everywhere in one pass.

Nothing here is code, and nothing here is a translation I would ship without the native read this file exists
to request.
