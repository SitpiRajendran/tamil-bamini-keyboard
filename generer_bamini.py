# -*- coding: utf-8 -*-
"""
Génère un clavier Tamil Unicode, disposition Bamini adaptée à un clavier AZERTY :
  - Tamil-Bamini-AZERTY.klc -> Microsoft Keyboard Layout Creator (MSKLC)
  - tamil_bamini_azerty.kmn -> Keyman Developer (remet ெ ே ை dans le bon ordre)

Les lettres suivent l'étiquette AZERTY (touche M -> அ, A -> ய, Q -> ங...).
Référence : convertisseur Bamini de Suratha (https://www.suratha.com/JS/bamini.js).
Pour corriger une touche : modifiez la table KEYS puis relancez :
    python generer_bamini.py
None = la touche ne produit rien dans cet état.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "keyman", "source")

# Rangée des chiffres : comme en AZERTY, Maj + touche = chiffre.
# (scancode, VK Windows AZERTY, étiquette AZERTY, sortie normale, sortie Maj)
KEYS = [
    ("29", "OEM_7",      "²", "ஹ",  "க்ஷ"),
    ("02", "1", "&", "!", "1"),
    ("03", "2", "é", "@", "2"),
    ("04", "3", '"', "சூ", "3"),
    ("05", "4", "'", "கூ", "4"),
    ("06", "5", "(", "மூ", "5"),
    ("07", "6", "-", "டூ", "6"),
    ("08", "7", "è", "ரூ", "7"),
    ("09", "8", "_", "ழூ", "8"),
    ("0a", "9", "ç", "(", "9"),
    ("0b", "0", "à", ")", "0"),
    ("0c", "OEM_4",      ")", "-",  "ூ"),    # Suratha : [_ = ஜூ
    ("0d", "OEM_PLUS",   "=", "ஸ்ரீ", "+"),
    ("10", "A",          "A", "ய",  "யு"),
    ("11", "Z",          "Z", "ண",  "ணு"),
    ("12", "E",          "E", "ந",  "நு"),
    ("13", "R",          "R", "ச",  "சு"),
    ("14", "T",          "T", "வ",  "வு"),
    ("15", "Y",          "Y", "ல",  "லு"),
    ("16", "U",          "U", "ர",  "ரு"),
    ("17", "I",          "I", "ை",  "ஐ"),
    ("18", "O",          "O", "ழ",  "ழு"),
    ("19", "P",          "P", "ி",  "ீ"),
    ("1a", "OEM_6",      "^", "ஜ",  "ு"),    # Suratha : [{ = ஜு
    ("1b", "OEM_1",      "$", "ஸ",  "ூ"),    # Suratha : Z} = ணூ
    ("2b", "OEM_5",      "*", "ஷ",  ";"),
    ("1e", "Q",          "Q", "ங",  "ஞ"),
    ("1f", "S",          "S", "ள",  "ளு"),
    ("20", "D",          "D", "ன",  "னு"),
    ("21", "F",          "F", "க",  "கு"),
    ("22", "G",          "G", "ப",  "பு"),
    ("23", "H",          "H", "ா",  "ர்"),   # Suratha : H = ர்
    ("24", "J",          "J", "த",  "து"),
    ("25", "K",          "K", "ம",  "மு"),
    ("26", "L",          "L", "ட",  "டு"),
    ("27", "M",          "M", "அ",  "ஆ"),
    ("28", "OEM_3",      "ù", "'",  '"'),
    ("2c", "W",          "W", "ற",  "று"),
    ("2d", "X",          "X", "ஒ",  "ஓ"),
    ("2e", "C",          "C", "உ",  "ஊ"),
    ("2f", "V",          "V", "எ",  "ஏ"),
    ("30", "B",          "B", "டி", "டீ"),
    ("31", "N",          "N", "ெ",  "ே"),
    ("32", "OEM_COMMA",  ",", "இ",  "?"),
    ("33", "OEM_PERIOD", ";", "்",  "."),
    ("34", "OEM_2",      ":", ":",  "ஃ"),
    ("35", "OEM_8",      "!", "!",  "§"),
    ("56", "OEM_102",    "<", "ஈ",  ","),
]

# Nom Keyman (positionnel, référence US) de chaque scancode
SC_TO_KEYMAN = {
    "29": "K_BKQUOTE", "02": "K_1", "03": "K_2", "04": "K_3", "05": "K_4",
    "06": "K_5", "07": "K_6", "08": "K_7", "09": "K_8", "0a": "K_9", "0b": "K_0",
    "0c": "K_HYPHEN", "0d": "K_EQUAL",
    "10": "K_Q", "11": "K_W", "12": "K_E", "13": "K_R", "14": "K_T", "15": "K_Y",
    "16": "K_U", "17": "K_I", "18": "K_O", "19": "K_P", "1a": "K_LBRKT",
    "1b": "K_RBRKT", "2b": "K_BKSLASH",
    "1e": "K_A", "1f": "K_S", "20": "K_D", "21": "K_F", "22": "K_G", "23": "K_H",
    "24": "K_J", "25": "K_K", "26": "K_L", "27": "K_COLON", "28": "K_QUOTE",
    "2c": "K_Z", "2d": "K_X", "2e": "K_C", "2f": "K_V", "30": "K_B", "31": "K_N",
    "32": "K_M", "33": "K_COMMA", "34": "K_PERIOD", "35": "K_SLASH", "56": "K_oE2",
}

PREFIX_VOWELS = ["ெ", "ே", "ை"]   # signes tapés AVANT la consonne en Bamini

# AltGr comme sur l'AZERTY français
ALTGR = {"03": "~", "04": "#", "05": "{", "06": "[", "07": "|", "08": "`",
         "09": "\\", "0a": "^", "0b": "@", "0c": "]", "0d": "}", "12": "€"}

# Touches où Verr. Maj agit comme Maj (rangée des chiffres, comme en AZERTY)
CAPS_SC = {"02", "03", "04", "05", "06", "07", "08", "09", "0a", "0b", "0c", "0d"}


def hx(c):
    return "%04x" % ord(c)


# ---------------------------------------------------------------- MSKLC (.klc)
KEYNAME = """KEYNAME

01\tEsc
0e\tBackspace
0f\tTab
1c\tEnter
1d\tCtrl
2a\tShift
36\t"Right Shift"
37\t"Num *"
38\tAlt
39\tSpace
3a\t"Caps Lock"
3b\tF1
3c\tF2
3d\tF3
3e\tF4
3f\tF5
40\tF6
41\tF7
42\tF8
43\tF9
44\tF10
45\tPause
46\t"Scroll Lock"
47\t"Num 7"
48\t"Num 8"
49\t"Num 9"
4a\t"Num -"
4b\t"Num 4"
4c\t"Num 5"
4d\t"Num 6"
4e\t"Num +"
4f\t"Num 1"
50\t"Num 2"
51\t"Num 3"
52\t"Num 0"
53\t"Num Del"
54\t"Sys Req"
57\tF11
58\tF12

KEYNAME_EXT

1c\t"Num Enter"
1d\t"Right Ctrl"
35\t"Num /"
37\t"Prnt Scrn"
38\t"Right Alt"
45\t"Num Lock"
46\tBreak
47\tHome
48\tUp
49\t"Page Up"
4b\tLeft
4d\tRight
4f\tEnd
50\tDown
51\t"Page Down"
52\tInsert
53\tDelete
5b\t"Left Windows"
5c\t"Right Windows"
5d\tApplication
"""


def build_klc():
    rows, ligs = [], []
    for sc, vk, _lbl, out0, out1 in KEYS:
        cols = []
        for mod, out in ((0, out0), (1, out1), (6, ALTGR.get(sc))):
            if out is None:
                cols.append("-1")
            elif len(out) == 1:
                cols.append(hx(out))
            else:
                cols.append("%%")
                ligs.append("%s\t\t%d\t%s" % (vk.ljust(10), mod, "\t".join(hx(c) for c in out)))
        cap = "1" if sc in CAPS_SC else "0"
        rows.append("%s\t%s\t%s\t%s\t%s\t%s" % (sc, vk.ljust(10), cap, cols[0], cols[1], cols[2]))
    rows.append("39\t%s\t0\t0020\t0020\t-1" % "SPACE".ljust(10))
    rows.append("53\t%s\t0\t002e\t002e\t-1" % "DECIMAL".ljust(10))

    klc = (
        'KBD\ttambamaz\t"Tamil - Bamini AZERTY (Unicode)"\n\n'
        'COPYRIGHT\t"(c) 2026 Sitpi Rajendran"\n\n'
        'COMPANY\t"Sitpi Rajendran"\n\n'
        'LOCALENAME\t"ta-LK"\n\n'
        'LOCALEID\t"00000849"\n\n'
        'VERSION\t1.0\n\n'
        'SHIFTSTATE\n\n'
        '0\t//Column 4\n'
        '1\t//Column 5 : Shft\n'
        '6\t//Column 6 : Ctrl Alt (AltGr)\n\n'
        "LAYOUT\t\t;an extra '@' at the end is a dead key\n\n"
        '//SC\tVK_\t\tCap\t0\t1\t6\n'
        '//--\t----\t\t----\t----\t----\t----\n\n'
        + "\n".join(rows) + "\n\n"
        'LIGATURE\n\n'
        '//VK_\t\tMod#\tChar0\tChar1\tChar2\tChar3\n'
        '//----\t\t----\t----\t----\t----\t----\n\n'
        + "\n".join(ligs) + "\n\n"
        + KEYNAME + "\n"
        'DESCRIPTIONS\n\n'
        '0409\tTamil - Bamini AZERTY (Unicode)\n\n'
        'LANGUAGENAMES\n\n'
        '0409\tTamil (Sri Lanka)\n\n'
        'ENDKBD\n'
    )
    # MSKLC exige UTF-16 LE avec BOM et fins de ligne CRLF
    with open(os.path.join(HERE, "Tamil-Bamini-AZERTY.klc"), "w", encoding="utf-16", newline="\r\n") as f:
        f.write(klc)


# ------------------------------------------------------------- Keyman (.kmn)
def uplus(s):
    return " ".join("U+%04X" % ord(c) for c in s)


def vkey(sc, shift):
    return "[%s%s]" % ("SHIFT " if shift else "", SC_TO_KEYMAN[sc])


def build_kmn():
    cons_keys, cons_out, other = [], [], []
    ksha_key = None
    for sc, _vk, _lbl, out0, out1 in KEYS:
        for shift, out in ((False, out0), (True, out1)):
            if out is None:
                continue
            k = vkey(sc, shift)
            if out == "க்ஷ":
                ksha_key = k
            if len(out) == 1 and 0x0B95 <= ord(out) <= 0x0BB9:
                cons_keys.append(k)
                cons_out.append(out)
            else:
                other.append((k, out))

    L = []
    L.append("c Clavier Tamil Unicode - disposition Bamini pour AZERTY (généré par generer_bamini.py)")
    L.append("store(&VERSION) '10.0'")
    L.append("store(&NAME) 'Tamil Bamini AZERTY (Unicode)'")
    L.append("store(&TARGETS) 'windows macosx'")
    L.append("store(&KEYBOARDVERSION) '1.2'")
    L.append("store(&COPYRIGHT) '(c) 2026 Sitpi Rajendran'")
    L.append("")
    L.append("begin Unicode > use(main)")
    L.append("")
    L.append("store(ckeys) " + " ".join(cons_keys))
    L.append("store(cons)  " + " ".join(uplus(c) for c in cons_out))
    L.append("")
    L.append("group(main) using keys")
    L.append("")
    L.append("c --- Bamini : le signe voyelle préfixe est tapé AVANT la consonne ;")
    L.append("c --- on le replace après la consonne (ordre Unicode correct).")
    for v in PREFIX_VOWELS:
        L.append("dk(pv) %s + any(ckeys) > index(cons, 3) %s" % (uplus(v), uplus(v)))
        L.append("dk(pv) %s + %s > U+0B95 U+0BCD U+0BB7 %s" % (uplus(v), ksha_key, uplus(v)))
    L.append("")
    L.append("c --- ெ/ே puis ா -> ொ/ோ ;  ெ puis ள -> ௌ ;  ஒ puis ள -> ஔ")
    L.append("any(cons) U+0BC6 + [K_H] > index(cons, 1) U+0BCA")
    L.append("any(cons) U+0BC7 + [K_H] > index(cons, 1) U+0BCB")
    L.append("any(cons) U+0BC6 + [K_S] > index(cons, 1) U+0BCC")
    L.append("U+0B92 + [K_S] > U+0B94")
    L.append("")
    L.append("c --- Suratha : ு puis ா / } / + -> ூ  (Sh = ளூ, Z} = ணூ, A+ = யூ)")
    L.append("U+0BC1 + [K_H] > U+0BC2")
    L.append("U+0BC1 + [SHIFT K_RBRKT] > U+0BC2")
    for plus in ("[SHIFT NCAPS K_EQUAL]", "[CAPS K_EQUAL]"):
        L.append("U+0BC1 + %s > U+0BC2" % plus)
        L.append("any(cons) + %s > index(cons, 1) U+0BC2" % plus)
    L.append("c --- Suratha : ா a la forme de ர  ->  hp = ரி, hP = ரீ, h; = ர்")
    L.append("U+0BBE + [K_P] > U+0BB0 U+0BBF")
    L.append("U+0BBE + [SHIFT K_P] > U+0BB0 U+0BC0")
    L.append("U+0BBE + [K_COMMA] > U+0BB0 U+0BCD")
    L.append("")
    L.append("c --- Consonnes")
    L.append("+ any(ckeys) > index(cons, 1)")
    L.append("")
    L.append("c --- Autres touches (dk(pv) = marqueur invisible : signe préfixe pas encore placé)")
    caps_names = {SC_TO_KEYMAN[sc] for sc in CAPS_SC}
    for k, out in other:
        mark = "dk(pv) " if out in PREFIX_VOWELS else ""
        name = k.strip("[]").split()[-1]
        if name in caps_names:   # Verr. Maj inverse Maj, comme en AZERTY
            sh = k.startswith("[SHIFT")
            L.append("+ [%sNCAPS %s] > %s%s" % ("SHIFT " if sh else "", name, mark, uplus(out)))
            L.append("+ [%sCAPS %s] > %s%s" % ("" if sh else "SHIFT ", name, mark, uplus(out)))
        else:
            L.append("+ %s > %s%s" % (k, mark, uplus(out)))
    L.append("")
    L.append("c --- AltGr comme sur l'AZERTY français")
    for sc, ch in ALTGR.items():
        for caps in (("NCAPS ", "CAPS ") if sc in CAPS_SC else ("",)):
            L.append("+ [RALT %s%s] > %s" % (caps, SC_TO_KEYMAN[sc], uplus(ch)))
    L.append("")
    with open(os.path.join(SRC, "tamil_bamini_azerty.kmn"), "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write("\n".join(L))


KPS = """<?xml version="1.0" encoding="utf-8"?>
<Package>
  <System>
    <KeymanDeveloperVersion>17.0.0.0</KeymanDeveloperVersion>
    <FileVersion>7.0</FileVersion>
  </System>
  <Options/>
  <Info>
    <Name URL="">Tamil Bamini AZERTY (Unicode)</Name>
    <Copyright URL="">(c) 2026 Sitpi Rajendran</Copyright>
    <Version URL="">1.2</Version>
  </Info>
  <Files>
    <File>
      <Name>../build/tamil_bamini_azerty.kmx</Name>
      <Description>Clavier Tamil Bamini AZERTY</Description>
      <CopyLocation>0</CopyLocation>
      <FileType>.kmx</FileType>
    </File>
  </Files>
  <Keyboards>
    <Keyboard>
      <Name>Tamil Bamini AZERTY (Unicode)</Name>
      <ID>tamil_bamini_azerty</ID>
      <Version>1.2</Version>
      <Languages>
        <Language ID="ta-LK">Tamil (Sri Lanka)</Language>
      </Languages>
    </Keyboard>
  </Keyboards>
</Package>
"""


def build_kps():
    with open(os.path.join(SRC, "tamil_bamini_azerty.kps"), "w", encoding="utf-8") as f:
        f.write(KPS)


if __name__ == "__main__":
    os.makedirs(SRC, exist_ok=True)
    build_klc()
    build_kmn()
    build_kps()
    print("OK : Tamil-Bamini-AZERTY.klc et keyman/source/ générés.")
