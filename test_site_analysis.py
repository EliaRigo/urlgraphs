import unittest

class TestMyModule(unittest.TestCase):

   def test_Parser(self):
       from site_analysis import Parser
       import re

       parser = Parser()
       self.assertFalse(parser.match('www.google.it'))

       parser.regex = re.compile('www.google.it')
       self.assertTrue(parser.match('www.google.it'))


   def test_clear_site(self):
        from site_analysis import clear_site

        self.assertEqual(clear_site('http://www.miosito.com:80/pagina.html'),'http://www.miosito.com/pagina.html')
        self.assertEqual(clear_site('http://www.viagginrete-it.it/vacanze/vacanze per famiglie/'),
            'http://www.viagginrete-it.it/vacanze/vacanze%20per%20famiglie/')
        self.assertEqual(clear_site('http://www.miosito.com:80/pagina.html?params=params'),
            'http://www.miosito.com/pagina.html?params=params')
        self.assertEqual(clear_site('http://www.miosito.com/pagina.html/print'), 'http://www.miosito.com/pagina.html/')
        self.assertEqual(clear_site('http://www.miosito.com/pagina.html/print/'), 'http://www.miosito.com/pagina.html/')


   def  test_Generic_link(self):
       from site_analysis import GenericLink
       gl = GenericLink()
       l = []
       for found_url in gl.run('http://www.diffbot.com/'):
           l.append(found_url)
       self.assertListEqual(l,['http://www.diffbot.com:80/our-apis'])


   def test_gen_hash(self):
       from site_analysis import gen_hash
       #self.assertEqual(gen_hash('http://www.diffbot.com/',dict(p1='p1', p2='p2')),'1905959970210950507')
       # insetrt new hash
       self.assertEqual(gen_hash('http://www.diffbot.com/',dict(p1='p1', p2='p2')),
                        gen_hash('http://www.diffbot.com/',dict(p1='p1', p2='p2')))

   def test_is_valid(self):
       from site_analysis import is_valid
       self.assertTrue(is_valid('http://it.wikipedia.org/wiki/Python/'))
       self.assertFalse(is_valid('javascript://'))
       self.assertFalse(is_valid('http://showthread.php/?s=8714a40618cf41351b24bd0cbd6729d7&p=884417#post884417'))
       self.assertFalse(is_valid('mailto:mail_user@webhost.com'))
       self.assertFalse(is_valid('http://turistipercaso.it/forum/p/abuse/775751/'))
       self.assertFalse(is_valid('http://turistipercaso.it/u/u/login/?popup'))
       self.assertFalse(is_valid('http://www.ilturista.info/ugc/foto_viaggi_vacanze/'
                                 '455-Le_cascate_piu_belle_grandi_o_spettacolari_del_mondo/?idfoto=8704'))
       self.assertFalse(is_valid('http://www.ilturista.info/ugc/immagini/giordania/asia/1822/'))
       self.assertFalse(is_valid('http://www.ilturista.info/photogallery/'))
       self.assertFalse(is_valid('http://fakeurl.it/'))

   def test_VBulletin_Topic(self):
       from site_analysis import VBulletin_Topic
       from bs4 import BeautifulSoup
       import requests
       vbt = VBulletin_Topic()
       self.assertTrue(vbt.match('http://www.ilgiramondo.net/forum/trentino-alto-adige/15753-trentino-alto-adige.html'))
       self.assertFalse(vbt.match('http://www.google.it'))
       text_soup = BeautifulSoup(requests.get('http://www.ilgiramondo.net/forum/trentino-alto-adige/15753-trentino-alto-adige.html').text, "lxml")
       self.assertEqual(len(list(vbt.found_pages(text_soup))),9)
       self.assertEqual(len(list(vbt.messages_url(text_soup))),9)
       self.assertEqual(len(list(vbt.run('http://www.ilgiramondo.net/forum/trentino-alto-adige/15753-trentino-alto-adige.html'))),18)

   def test_VBUlletin_Section(self):
       from site_analysis import VBulletin_Section
       vbt = VBulletin_Section()
       self.assertTrue(vbt.match('http://www.ilgiramondo.net/forum/trentino-alto-adige/'))
       self.assertFalse(vbt.match('http://www.google.it'))
       self.assertEqual(len(list(vbt.run('http://www.ilgiramondo.net/forum/trentino-alto-adige/'))),131)

   def test_Turisti_Per_Caso(self):
       from site_analysis import TuristiPerCaso
       from bs4 import BeautifulSoup
       import requests
       vbt = TuristiPerCaso()
       self.assertTrue(vbt.match('http://turistipercaso.it/forum/t/71583/isole-della-grecia.html'))
       self.assertTrue(vbt.match('https://turistipercaso.it/forum/t/71583/isole-della-grecia.html'))
       self.assertTrue(vbt.match('http://www.turistipercaso.it/forum/t/71583/isole-della-grecia.html'))
       self.assertTrue(vbt.match('https://www.turistipercaso.it/forum/t/71583/isole-della-grecia.html'))
       grecia_soup = BeautifulSoup(requests.get('http://turistipercaso.it/forum/t/71583/isole-della-grecia.html').text, "lxml")
       self.assertEqual(len(list(vbt.found_paginator(grecia_soup))),6)
       messico_soup = BeautifulSoup(requests.get('http://turistipercaso.it/forum/t/194776/holbox-messico.html').text, "lxml")
       self.assertEqual(len(list(vbt.found_paginator(messico_soup))),0)
       self.assertEqual(len(list(vbt.run('http://turistipercaso.it/forum/t/71583/isole-della-grecia.html'))),len(list(vbt.run('http://turistipercaso.it/forum/t/71583/isole-della-grecia.html'))))

if __name__ == "__main__":
    unittest.main()
