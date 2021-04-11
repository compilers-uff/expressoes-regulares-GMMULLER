from funcoes_conversao import *

class TestER:

    def test_match_1(self):

        assert match('a', 'a')

    def test_match_2(self):

        assert match('+(a,b)', 'a')
    
    def test_match_3(self):

        assert match('.(a,b)', 'ab')

    def test_match_4(self):

        assert match('*(+(a,b))', 'a')

    def test_match_5(self):

        assert match('*(+(a,b))', 'aaa')

    def test_match_6(self):

        assert match('*(+(a,b))', 'ab')
    
    def test_match_7(self):

        assert match('*(+(a,b))', 'aba')

    def test_match_8(self):

        assert match('*(+(a,b))', 'abababa')

    def test_match_9(self):

        assert match('+(a,b))', 'a')

    def test_match_10(self):

        assert not match('.(a,b)', 'a')

    def test_match_11(self):

        assert match('*(+(a,b))', 'a')
    
    def test_match_12(self):

        assert match('*(a)', '')

    def test_match_13(self):

        assert match('*(a)', 'aaaaaaa')

    def test_match_14(self):

        assert match('.(*(+(a,b)), *(+(+(a,b),c)))', 'ababababbabacababacbacb')

    def test_match_15(self):

        assert not match('.(.(a,b),c)', 'abcc')
    
    def test_match_16(self):

        assert match('.(+(a,b),+(c,d))', 'ac')

    def test_match_17(self):

        assert not match('a', '')

    def test_match_18(self):

        assert match('.(.(+(a,b),+(c,d)), .(+(a,b),+(c,d)))', 'acbd')

    def test_match_19(self):

        assert not match('.(.(+(a,b),+(c,d)), .(+(a,b),+(c,d)))', 'abcbd')

    def test_match_20(self):

        assert match('*(.(.(a,b),c))', 'abc')

    def test_match_21(self):

        assert not match('*(.(.(a,b),c))', 'abca')

    def test_match_22(self):

        assert match('*(.(.(a,b),c))', 'abcabc')

    def test_match_23(self):

        assert match('+(+(+(+(a,b),c),d),e)', 'e')

    def test_match_24(self):

        assert not match('+(+(+(+(a,b),c),d),e)', '')

    def test_match_25(self):

        assert match('.(+(+(+(+(a,b),c),d),e), +(+(+(+(a,b),c),d),e))', 'ae')