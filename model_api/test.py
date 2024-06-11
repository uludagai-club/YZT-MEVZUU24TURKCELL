import unittest
from main import process_text, TextInput

class TestNerSentiment(unittest.TestCase):
    
    def test_process_text(self):
        input_text = TextInput(text="Fiber 100mb SuperOnline kullanıcısıyım yaklaşık 2 haftadır @Twitch @Kick_Turkey gibi canlı yayın platformlarında 360p yayın izlerken donmalar yaşıyoruz.")
        result = process_text(input_text)
        self.assertTrue("entity_list" in result)
        self.assertTrue("results" in result)
        
if __name__ == '__main__':
    unittest.main()
