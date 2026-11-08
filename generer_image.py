# -*- coding: utf-8 -*-
"""
Dessine le clavier AZERTY avec les caractères français et tamouls (Bamini).
Produit docs/clavier-azerty.html puis docs/clavier-azerty.png (via Chrome headless).

    python generer_image.py
"""
import html
import os
import subprocess

from generer_bamini import KEYS, ALTGR

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, "docs")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Étiquettes AZERTY françaises : scancode -> (normal, Maj)
FR = {
    "29": ("²", ""), "02": ("&", "1"), "03": ("é", "2"), "04": ('"', "3"), "05": ("'", "4"),
    "06": ("(", "5"), "07": ("-", "6"), "08": ("è", "7"), "09": ("_", "8"), "0a": ("ç", "9"),
    "0b": ("à", "0"), "0c": (")", "°"), "0d": ("=", "+"),
    "1a": ("^", "¨"), "1b": ("$", "£"), "28": ("ù", "%"), "2b": ("*", "µ"), "56": ("<", ">"),
    "32": (",", "?"), "33": (";", "."), "34": (":", "/"), "35": ("!", "§"),
}
for sc, _vk, lbl, _o0, _o1 in KEYS:
    if lbl.isalpha() and lbl.isascii():
        FR[sc] = (lbl, "")          # lettre : une seule étiquette, comme sur le clavier

TAMIL = {sc: (o0 or "", o1 or "") for sc, _vk, _l, o0, o1 in KEYS}

# Rangées ISO : (scancode ou nom de touche spéciale, largeur en unités)
ROWS = [
    [("29", 1)] + [("%02x" % i, 1) for i in range(2, 14)] + [("Retour ⌫", 2)],
    [("Tab ↹", 1.5)] + [("%02x" % i, 1) for i in range(0x10, 0x1c)] + [("ENTER", 1.5)],
    [("Verr. Maj", 1.75)] + [("%02x" % i, 1) for i in range(0x1e, 0x29)] + [("2b", 1), ("", 1.25)],
    [("Maj ⇧", 1.25), ("56", 1)] + [("%02x" % i, 1) for i in range(0x2c, 0x36)] + [("Maj ⇧", 2.75)],
    [("Ctrl", 1.25), ("Win", 1.25), ("Alt", 1.25), ("Espace", 6.25), ("AltGr", 1.25),
     ("Win", 1.25), ("Menu", 1.25), ("Ctrl", 1.25)],
]

U = 74          # taille d'une unité en px
GAP = 6
PAD = 24
MARKS = set("ாிீுூெேைொோௌ்")   # signes : affichés sur un cercle pointillé


def show(t):
    if t and t[0] in MARKS:
        t = "◌" + t
    return html.escape(t)


def key_html(name, x, y, w):
    W = w * U - GAP
    style = "left:%dpx;top:%dpx;width:%dpx;height:%dpx" % (x, y, W, U - GAP)
    if name in TAMIL or name in FR:
        fr0, fr1 = FR.get(name, ("", ""))
        ta0, ta1 = TAMIL.get(name, ("", ""))
        ag = ALTGR.get(name, "")
        if ta0 == fr0:
            ta0 = ""
        if ta1 in (fr1, fr0) and ta1 and not ta1.isalpha():
            ta1 = "" if ta1 == fr1 else ta1
        return (
            '<div class="k" style="%s">'
            '<span class="fr s">%s</span><span class="fr n">%s</span>'
            '<span class="ta s">%s</span><span class="ta n">%s</span>'
            '<span class="ag">%s</span></div>'
            % (style, html.escape(fr1), html.escape(fr0), show(ta1), show(ta0), html.escape(ag))
        )
    if name == "":
        return ""
    return '<div class="k sp" style="%s"><span>%s</span></div>' % (style, html.escape(name))


def build():
    parts, y = [], PAD + 70
    for r, row in enumerate(ROWS):
        x = PAD
        for name, w in row:
            if name == "ENTER":   # Entrée ISO sur deux rangées
                W = w * U - GAP
                parts.append(
                    '<div class="k sp enter" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
                    % (x, y, W, U))
                parts.append(
                    '<div class="k sp enterlow" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
                    '<span>Entrée ↵</span></div>'
                    % (x + int(0.25 * U), y + U - GAP - 4, W - int(0.25 * U), U + 4))
            else:
                parts.append(key_html(name, x, y, w))
            x += w * U
        y += U
    width = int(15 * U + 2 * PAD - GAP)
    height = y + 64
    page = """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<title>Clavier Tamil Bamini AZERTY</title>
<style>
  :root {
    --bg: #f4f1ea; --key: #ffffff; --edge: #d8d2c4; --sp: #e9e4d8;
    --fr: #3b3b3b; --ta: #b3261e; --ag: #1f5fa8; --muted: #6b665c;
  }
  html, body { margin: 0; background: var(--bg); }
  body { width: %(W)dpx; height: %(H)dpx; position: relative;
         font-family: "Helvetica Neue", Arial, sans-serif; }
  h1 { position: absolute; left: %(P)dpx; top: 18px; margin: 0; font-size: 26px; color: #222; }
  h1 small { font-weight: 400; font-size: 16px; color: var(--muted); margin-left: 10px; }
  .k { position: absolute; box-sizing: border-box; background: var(--key);
       border: 1px solid var(--edge); border-bottom-width: 3px; border-radius: 8px; }
  .k span { position: absolute; line-height: 1; }
  .fr { left: 8px; color: var(--fr); font-size: 17px; }
  .fr.s { top: 7px; } .fr.n { bottom: 8px; }
  .ta { right: 7px; color: var(--ta); font-family: "Tamil Sangam MN", "Tamil MN", sans-serif; }
  .ta.s { top: 6px; font-size: 18px; } .ta.n { bottom: 7px; font-size: 22px; font-weight: 600; }
  .ag { left: 50%%; transform: translateX(-50%%); bottom: 7px; color: var(--ag); font-size: 13px; }
  .sp { background: var(--sp); }
  .sp span { left: 10px; bottom: 9px; font-size: 14px; color: var(--muted); }
  .enter { border-bottom: none; border-bottom-left-radius: 0; z-index: 1; }
  .enterlow { border-top: none; border-top-left-radius: 0; border-top-right-radius: 0; z-index: 2; }
  .legend { position: absolute; left: %(P)dpx; bottom: 18px; font-size: 14px; color: var(--muted); }
  .legend b { font-weight: 600; margin-right: 18px; }
  .legend .fr, .legend .ta, .legend .ag { position: static; font-size: inherit; }
</style></head><body>
<h1>Clavier Tamil Bamini — AZERTY<small>Unicode · Tamoul (Sri Lanka) · référence Suratha</small></h1>
%(KEYS)s
<div class="legend">
  <b class="fr">Noir : AZERTY français</b>
  <b class="ta">Rouge : tamoul (bas = sans Maj, haut = Maj)</b>
  <b class="ag">Bleu : AltGr</b>
  ◌ = signe voyelle à combiner · ெ ே ை se tapent avant la consonne
</div>
</body></html>
""" % {"W": width, "H": height, "P": PAD, "KEYS": "\n".join(parts)}
    os.makedirs(DOCS, exist_ok=True)
    out_html = os.path.join(DOCS, "clavier-azerty.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(page)
    return out_html, width, height


if __name__ == "__main__":
    path, w, h = build()
    png = os.path.join(DOCS, "clavier-azerty.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=%d,%d" % (w, h),
                    "--screenshot=" + png, "file://" + path],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("OK :", png)
