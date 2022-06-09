""" Swedish g2p rules."""

import pynini
from pynini.lib import rewrite
from pynini.lib import pynutil

# Graphemes are based on:
# https://en.wikipedia.org/wiki/Swedish_alphabet#Sound%E2%80%93spelling_correspondences

# Phonemes are based on:
# https://oxford.universitypressscholarship.com/view/10.1093/acprof:oso/9780199543571.001.0001/acprof-9780199543571-chapter-2
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
    "i",
    "o",
    "u",
    "y",
    "å",
    "ä",
    "ö",
    # Vowel phonemes that aren't also graphemes
    "iː",
    "ɪ",
    "eː",
    "e",
    "ɛː",
    "ɛ",
    # # Reduction of <e> before a retroflex
    # "æː",  # ära /ˈɛ̂ːra/ → [ˈæ̂ːra] ('honor')
    # "æ",  # ärt /ˈɛrt/ → [ˈæʈː] ('pea')
    "ɑː",
    "a",
    "oː",
    "ɔ",
    "uː",
    "ʊ",
    "ʉː",
    "ɵ",
    "yː",
    "ʏ",
    "øː",
    "ø",
    # # Reduction of <ö> before a retroflex
    # "œ:",  # øː --> œ: / _r
    # "œ",  # # ø --> œ / _r
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
    "ʝ",
    "jː",
    "bː",
    "dː",
    "fː",
    "gː",
    "lː",
    "mː",
    "nː",
    "pː",
    "rː",
    "sː",
    "tː",
    "kː",
)

SIGMA_STAR = pynini.union(v, c).closure().optimize()

# Front vowels
fv = pynini.union(
    "e", "i", "ä", "y", "ö", "ɪ", "ʏ", "ɛ", "ø", "iː", "eː", "ɛː", "yː", "øː"
)

G2P = (
    # Rule #1 – short vowels (assuming stress)
    pynini.cdrewrite(
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
    # Rule #2 – long vowels (assuming stress)
    @ pynini.cdrewrite(
        pynini.string_map(
            [
                ("i", "iː"),
                ("y", "yː"),
                ("e", "eː"),
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
    # "rl", "rn", "rd", "ln" simplified the long vowel rule
    # Consonants
    # Rule #3 – <c> as /s/
    @ pynini.cdrewrite(pynini.cross("c", "s"), "", fv, SIGMA_STAR)
    # Rule #4 – <ck> as /k/
    @ pynini.cdrewrite(pynini.cross("ck", "kː"), "", "", SIGMA_STAR)
    # Rule #5 – <ch> as /ɧ/
    @ pynini.cdrewrite(pynini.cross("ch", "ɧ"), "", "", SIGMA_STAR)
    # Rule #6 – <c> as /k/
    @ pynini.cdrewrite(pynini.cross("c", "k"), "", "", SIGMA_STAR)
    # Rule #7 – /d/-deletion
    @ pynini.cdrewrite(
        pynutil.delete("d"),
        "n",
        pynini.union("p", "b", "k", "g", "f", "v", "s"),
        SIGMA_STAR,
    )
    # Rule #8 – <gn> as /gn/
    @ pynini.cdrewrite(pynini.cross("gn", "gn"), "[BOS]", v, SIGMA_STAR)
    # Rule #9 – <gn> as /ŋ/
    @ pynini.cdrewrite(
        pynini.cross("gn", "ŋ"), "", pynini.union("t", "s"), SIGMA_STAR
    )
    # Rule #10 – <gn> as /ŋn/
    @ pynini.cdrewrite(pynini.cross("gn", "ŋn"), v, "", SIGMA_STAR)
    # Rule #11 – retroflexes
    @ pynini.cdrewrite(
        pynini.string_map(
            [("rt", "ʈ"), ("rd", "ɖ"), ("rn", "ɳ"), ("rs", "ʂ"), ("rl", "ɭ")]
        ),
        "",
        "",
        SIGMA_STAR,
    )
    # Rule #12 – lenition of dorsals before front vowels (palatalization)
    @ pynini.cdrewrite(pynini.cross("g", "j"), "", fv, SIGMA_STAR)
    # Rule #13 – /g/-palatalization after /r, l/
    @ pynini.cdrewrite(
        pynini.cross("g", "j"), pynini.union("r", "l"), "", SIGMA_STAR,
    )
    # Rule #14 - <gj> as /ʝ/
    @ pynini.cdrewrites(pynini.cross("gj", "ʝ"), "[BOS]", "")
    # Rule #15 – /l/-palatalization
    @ pynini.cdrewrite(pynini.cross("lj", "ʝ"), "[BOS]", "", SIGMA_STAR)
    # Rule #16 – <ng>
    @ pynini.cdrewrite(pynini.cross("ng", "ŋ"), "", "", SIGMA_STAR)
    # Rule #17 – <sj>-sound before vowels
    @ pynini.cdrewrite(
        pynini.cross(pynini.union("sj", "skj", "stj"), "ɧ"), "", v, SIGMA_STAR,
    )
    # Rule #18 – <tj>/<kj>-sound
    @ pynini.cdrewrite(
        pynini.cross(pynini.union("tj", "kj"), "ɕ"), "", "", SIGMA_STAR
    )
    # Rule #19 – <sk> as /ɧ/ before front vowels
    @ pynini.cdrewrite(pynini.cross("sk", "ɧ"), "", fv, SIGMA_STAR)
    # Rule #20
    @ pynini.cdrewrite(
        pynini.string_map([("gj", "ʝ"), ("w", "v"), ("x", "ks"), ("z", "s")]),
        "",
        "",
        SIGMA_STAR,
    )
    # Rule #21 – long consonants
    @ pynini.cdrewrite(
        pynini.string_map(
            [
                ("bb", "bː"),
                ("dd", "dː"),
                ("ff", "fː"),
                ("gg", "gː"),
                ("ll", "lː"),
                ("mm", "mː"),
                ("nn", "nː"),
                ("pp", "pː"),
                ("rr", "rː"),
                ("ss", "sː"),
                ("tt", "tː"),
            ]
        ),
        v,
        v,
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
    @ pynini.cdrewrite(pynini.cross("k", "ɕ"), "", fv, SIGMA_STAR)
    # Rule #24 – j is always long
    @ pynini.cdrewrite(pynini.cross("j", "jː"), v, "", SIGMA_STAR)
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
