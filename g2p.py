""" Swedish g2p rules."""

import pynini
from pynini.lib import rewrite
from pynini.lib import pynutil

# Graphemes are based on:
# https://en.wikipedia.org/wiki/Swedish_alphabet

# Phonemes are based on:
# https://oxford.universitypressscholarship.com/view/10.1093/acprof:oso/9780199543571.001.0001/acprof-9780199543571
# https://en.wikipedia.org/wiki/Swedish_phonology
# https://en.wikipedia.org/wiki/Help:IPA/Swedish

# Rules are based on:
# https://en.wikipedia.org/wiki/Swedish_alphabet
# https://en.wikipedia.org/wiki/Swedish_phonology
# The Phonology of Swedish by Tomas Riad (2014)
# http://www.glottopedia.org/index.php/Swedish_Phonology#:~:text=Swedish%20makes%20use%20of%20nine%20short%20vowels.&text=In%20many%20cases%20and,%5B%C9%9B%5D%20are%20only%20allophones.
# https://www.languagetrainers.ca/blog/swedish-accent-pronunciation/#:~:text=In%20Swedish%2C%20speakers%20use%20single,to%20distinguish%20between%20two%20words.&text=Double%20consonants%20also%20affect%20pronunciation,(v%C3%A4gen%2C%20the%20road).

# Defining the relevant inventories
v = pynini.union(
    # 9 vowels as graphemes
    "a",
    "e",
    "é",
    "i",
    "o",
    "u",
    "y",
    "å",
    "ä",
    "ö",
    # Vowel phonemes that aren't also graphemes
    "ɪ",
    "e",
    "ɛ",
    "æ",
    "ɑ",
    "a",
    "ɔ",
    "ʊ",
    "ʉ",
    "ɵ",
    "ʏ",
    "ø",
    "œ",
    # length marker
    "ː"
)
c = pynini.union(
    # 20 consonants
    "b",
    "c",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "q",
    "r",
    "s",
    "t",
    "v",
    "w",
    "x",
    "z",
    # Consonantal phonemes that aren't also graphemes
    "ɕ",
    "ɧ",
    "s̪",
    "ŋ",
    "ɖ",
    "ɭ",
    "ɳ",
    "ʂ",
    "ʈ",
    "ʝ"
)

SIGMA_STAR = pynini.union(v, c).closure().optimize()

# Front vowels
fv = pynini.union(
    "e", "i", "ä", "y", "ö", "ɪ", "ʏ", "ɛ", "ø", "iː", "eː", "ɛː", "yː", "øː"
)

G2P = (
    # Rule #1 – vowel lowering (short)
    pynini.cdrewrite(
        pynini.string_map([("ä", "æ"), ("ö", "œ")]),
        "",
        pynini.union("rl", "rt", "rd", "rs", "rn"),
        SIGMA_STAR,
    )
    # Rule #2 – vowel lowering (long)
    @ pynini.cdrewrite(
        pynini.string_map([("ä", "æː"), ("ö", "œː")]),
        "",
        pynini.accep("r") + "[EOS]",
        SIGMA_STAR,
    )
    # Rule #3 – short vowels (assuming stress)
    @ pynini.cdrewrite(
        pynini.string_map(
            [
                ("i", "ɪ"),
                ("y", "ʏ"),
                ("e", "e"),
                ("ä", "ɛ"),
                ("ö", "ø"),
                ("u", "ɵ"),
                ("o", "ʊ"),
                ("å", "ɔ"),
                ("a", "a"),
            ]
        ),
        "",
        pynini.union(c + c.plus, "j", "m"),
        SIGMA_STAR,
    )
    # Rule #4 – long vowels (assuming stress)
    @ pynini.cdrewrite(
        pynini.string_map(
            [
                ("i", "iː"),
                ("y", "yː"),
                ("e", "eː"),
                ("é", "eː"),
                ("ä", "ɛː"),
                ("ö", "øː"),
                ("u", "ʉː"),
                ("o", "uː"),
                ("å", "oː"),
                ("a", "ɑː"),
            ]
        ),
        "",
        c.ques + "[EOS]",
        SIGMA_STAR,
    )
    # Consonants
    # Rule #5 – <c> as /s/
    @ pynini.cdrewrite(pynini.cross("c", "s"), "", fv, SIGMA_STAR)
    # Rule #6 – <ck> as /k/
    @ pynini.cdrewrite(pynini.cross("ck", "kk"), "", "", SIGMA_STAR)
    # Rule #7 – <ch> as /ɧ/
    @ pynini.cdrewrite(pynini.cross("ch", "ɧ"), "", "", SIGMA_STAR)
    # Rule #8 – <c> as /k/
    @ pynini.cdrewrite(pynini.cross("c", "k"), "", "", SIGMA_STAR)
    # Rule #9 – /d/-deletion
    @ pynini.cdrewrite(
        pynutil.delete("d"),
        "n",
        pynini.union("p", "b", "k", "g", "f", "v", "s"),
        SIGMA_STAR,
    )
    # Rule #10 – <gn> as /ŋ/
    @ pynini.cdrewrite(
        pynini.cross("gn", "ŋ"), "", pynini.union("t", "s"), SIGMA_STAR
    )
    # Rule #11 – <gn> as /ŋn/
    @ pynini.cdrewrite(pynini.cross("gn", "ŋn"), v, "", SIGMA_STAR)
    # Rule #12 – retroflexes
    @ pynini.cdrewrite(
        pynini.string_map(
            [("rt", "ʈ"), ("rd", "ɖ"), ("rn", "ɳ"), ("rs", "ʂ"), ("rl", "ɭ")]
        ),
        "",
        "",
        SIGMA_STAR,
    )
    # Rule #13 – lenition of dorsals before front vowels (palatalization)
    @ pynini.cdrewrite(pynini.cross("g", "j"), "", fv, SIGMA_STAR)
    # Rule #14 – /g/-palatalization after /r, l/
    @ pynini.cdrewrite(
        pynini.cross("g", "j"), pynini.union("r", "l"), "", SIGMA_STAR,
    )
    # Rule #15 - <gj> as /ʝ/
    @ pynini.cdrewrite(pynini.cross("gj", "ʝ"), "[BOS]", "", SIGMA_STAR)
    # Rule #16 – /l/-palatalization
    @ pynini.cdrewrite(pynini.cross("lj", "ʝ"), "[BOS]", "", SIGMA_STAR)
    # Rule #17 – <ng>
    @ pynini.cdrewrite(pynini.cross("ng", "ŋ"), "", "", SIGMA_STAR)
    # Rule #18 – <sj>-sound before vowels
    @ pynini.cdrewrite(
        pynini.cross(pynini.union("sj", "skj", "stj"), "ɧ"), "", v, SIGMA_STAR,
    )
    # Rule #19 – <tj>/<kj>-sound
    @ pynini.cdrewrite(
        pynini.cross(pynini.union("tj", "kj"), "ɕ"), "", "", SIGMA_STAR
    )
    # Rule #20 – <sk> as /ɧ/ before front vowels
    @ pynini.cdrewrite(pynini.cross("sk", "ɧ"), "", fv, SIGMA_STAR)
    # Rule #21
    @ pynini.cdrewrite(
        pynini.string_map([("gj", "ʝ"), ("w", "v"), ("x", "ks"), ("z", "s")]),
        "",
        "",
        SIGMA_STAR,
    )
    # Rule #22 – short double consonants
    @ pynini.cdrewrite(
        pynini.string_map(
            [
                ("bb", "b"),
                ("dd", "d"),
                ("ff", "f"),
                ("gg", "g"),
                ("ll", "l"),
                ("mm", "m"),
                ("nn", "n"),
                ("pp", "p"),
                ("rr", "r"),
                ("ss", "s"),
                ("tt", "t"),
            ]
        ),
        v,
        "[EOS]",
        SIGMA_STAR,
    )
    # Rule #23 – /k/-palatalization
    @ pynini.cdrewrite(pynini.cross("k", "ɕ"), "[BOS]", fv, SIGMA_STAR)
    # Rule #24 – j is always long
    @ pynini.cdrewrite(pynini.cross("j", "jj"), v, "", SIGMA_STAR)
)


def g2p(istring: str) -> str:
    """Applies the G2P rule.

    Args:
      istring: the graphemic input string.

    Returns:
      The phonemic output string.

    Raises.
      rewrite.Error: composition failure.
    """
    return rewrite.one_top_rewrite(istring, G2P)
