"""Unit tests for Swedish G2P."""

import unittest

import g2p


class G2PTest(unittest.TestCase):
    def rewrites(self, istring: str, expected_ostring: str) -> None:
        """Asserts that the g2p rule produces the correct output.

        Args:
            istring: the input string
            expected_ostring: the expected output string.
        """
        ostring = g2p.g2p(istring)
        self.assertEqual(ostring, expected_ostring)

    # short vowel tests
    # the following two also tests for short double consonants
    def test_sill(self):
        self.rewrites("sill", "sɪl")

    def test_syll(self):
        self.rewrites("syll", "sʏl")

    # the following also tests for long /j/
    def test_grej(self):
        self.rewrites("grej", "greːjj")

    def test_hämnd(self):
        self.rewrites("hämnd", "hɛmnd")

    def test_nöts(self):
        self.rewrites("nöts", "nøts")

    def test_tum(self):
        self.rewrites("tum", "tɵm")

    def test_bord(self):
        self.rewrites("bord", "bʊɖ")

    def test_åtta(self):
        self.rewrites("åtta", "ɔttɑː")

    def test_namn(self):
        self.rewrites("namn", "namn")

    # long vowel tests
    def test_sil(self):
        self.rewrites("sil", "siːl")

    def test_syl(self):
        self.rewrites("syl", "syːl")

    def test_hel(self):
        self.rewrites("hel", "heːl")

    def test_fä(self):
        self.rewrites("fä", "fɛː")

    def test_nöt(self):
        self.rewrites("nöt", "nøːt")

    def test_du(self):
        self.rewrites("du", "dʉː")

    def test_dok(self):
        self.rewrites("dok", "duːk")

    def test_på(self):
        self.rewrites("på", "poː")

    # vowel lowering (short)
    def test_närt(self):
        self.rewrites("närt", "næʈ")

    def test_hörs(self):
        self.rewrites("hörs", "hœʂ")

    # # vowel lowering (long)
    def test_här(self):
        self.rewrites("här", "hæːr")

    def test_hör(self):
        self.rewrites("hör", "hœːr")

    # <c> as /s/ before fv
    def test_cent(self):
        self.rewrites("cent", "sent")

    # <ck> as /kː/
    def test_bock(self):
        self.rewrites("bock", "bʊkk")

    # <c> as /k/
    def test_cab(self):
        self.rewrites("cab", "kɑːb")

    # <ch> as /ɧ/
    def test_chans(self):
        self.rewrites("chans", "ɧans")

    def test_chips(self):
        self.rewrites("chips", "ɧɪps")

    # /d/-deletion
    def test_landsväg(self):
        self.rewrites("landsväg", "lansvɛːg")

    # <gn> as /gn/
    def test_gnist(self):
        self.rewrites("gnist", "gnɪst")

    # <gn> as /ŋ/
    def test_lugnt(self):
        self.rewrites("lugnt", "lɵŋt")

    # <gn> as /ŋn/
    def test_dygn(self):
        self.rewrites("dygn", "dʏŋn")

    # retroflexes
    def test_fort(self):
        self.rewrites("fort", "fʊʈ")

    def test_gård(self):
        self.rewrites("gård", "gɔɖ")

    def test_forn(self):
        self.rewrites("forn", "fʊɳ")

    def test_ers(self):
        self.rewrites("ers", "eʂ")

    def test_curl(self):
        self.rewrites("curl", "kɵɭ")

    # lenition of /g/ before front vowels (palatalization)
    def test_gift(self):
        self.rewrites("gift", "jɪft")

    # /g/-palatalization after /r, l/
    def test_arg(self):
        self.rewrites("arg", "arj")

    def test_alg(self):
        self.rewrites("alg", "alj")

    # /k/-palatalization
    def test_kök(self):
        self.rewrites("kök", "ɕøːk")

    # tj/kj-sound
    def test_tjej(self):
        self.rewrites("tjej", "ɕeːjj")

    def test_kjol(self):
        self.rewrites("kjol", "ɕuːl")

    # /l/-palatalization
    def test_ljud(self):
        self.rewrites("ljud", "ʝʉːd")

    # <ng> as /ŋ/
    def test_gång(self):
        self.rewrites("gång", "gɔŋ")

    # sj-sound before vowels
    def test_sjö(self):
        self.rewrites("sjö", "ɧøː")

    def test_sjuk(self):
        self.rewrites("sjuk", "ɧʉːk")

    def test_skjut(self):
        self.rewrites("skjut", "ɧʉːt")

    def test_stjäl(self):
        self.rewrites("stjäl", "ɧɛːl")

    # <sk> as /ɧ/ before front vowels
    def test_skön(self):
        self.rewrites("skön", "ɧøːn")

    # <gj> as /ʝ/
    def test_gjort(self):
        self.rewrites("gjort", "ʝʊʈ")

    # <k> as /ɕ/ before front vowels
    def test_kiwi(self):
        self.rewrites("kiwi", "ɕiviː")

    # <x> as /ks/
    def test_fixt(self):
        self.rewrites("fixt", "fɪkst")

    # <z> as /s/
    def test_zen(self):
        self.rewrites("zen", "seːn")


if __name__ == "__main__":
    unittest.main()
