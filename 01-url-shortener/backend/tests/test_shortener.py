"""Unit tests for Base62 encoding and URL validation"""

import pytest
from src.shortener import Base62Encoder, URLShortener


class TestBase62Encoder:
    """Test Base62 encoding and decoding"""
    
    def test_encode_zero(self):
        """Test encoding 0 returns "0" """
        assert Base62Encoder.encode(0) == "0"
    
    def test_encode_single_digit(self):
        """Test encoding single digit 9 returns "9" """
        assert Base62Encoder.encode(9) == "9"
    
    def test_encode_alphabet_start(self):
        """Test encoding 10 returns "a" (start of alphabet) """
        assert Base62Encoder.encode(10) == "a"
    
    def test_encode_alphabet_end(self):
        """Test encoding 61 returns "Z" (end of alphabet) """
        assert Base62Encoder.encode(61) == "Z"
    
    def test_encode_overflow(self):
        """Test encoding 62 returns "10" (overflow to 2 digits) """
        assert Base62Encoder.encode(62) == "10"
    
    def test_encode_large_number(self):
        """Test encoding 1000 returns "g8" """
        assert Base62Encoder.encode(1000) == "g8"
    
    def test_decode_zero(self):
        """Test decoding "0" returns 0"""
        assert Base62Encoder.decode("0") == 0
    
    def test_decode_alphabet(self):
        """Test decoding "a" returns 10"""
        assert Base62Encoder.decode("a") == 10
    
    def test_decode_uppercase(self):
        """Test decoding "Z" returns 61"""
        assert Base62Encoder.decode("Z") == 61
    
    def test_encode_decode_roundtrip(self):
        """Test that encode/decode are inverse operations for 0-10000"""
        for n in range(10000):
            assert Base62Encoder.decode(Base62Encoder.encode(n)) == n
    
    def test_encode_decode_large_roundtrip(self):
        """Test roundtrip with very large number"""
        assert Base62Encoder.decode(Base62Encoder.encode(1000000)) == 1000000


class TestURLShortener:
    """Test URL validation and short URL generation"""
    
    @pytest.fixture
    def shortener(self):
        """Fixture to create URLShortener instance"""
        return URLShortener("http://short.ly")
    
    def test_validate_valid_https_url(self, shortener):
        """Test that valid HTTPS URL passes validation"""
        assert shortener.validate_long_url("https://example.com") == True
    
    def test_validate_valid_http_url(self, shortener):
        """Test that valid HTTP URL passes validation"""
        assert shortener.validate_long_url("http://example.com") == True
    
    def test_validate_long_url_with_path(self, shortener):
        """Test that URL with path passes validation"""
        assert shortener.validate_long_url("https://example.com/path/to/page") == True
    
    def test_validate_long_url_with_query(self, shortener):
        """Test that URL with query parameters passes validation"""
        assert shortener.validate_long_url("https://example.com?param=value") == True
    
    def test_reject_invalid_protocol(self, shortener):
        """Test that FTP protocol is rejected"""
        assert shortener.validate_long_url("ftp://example.com") == False
    
    def test_reject_no_protocol(self, shortener):
        """Test that URL without protocol is rejected"""
        assert shortener.validate_long_url("example.com") == False
    
    def test_reject_empty_string(self, shortener):
        """Test that empty string is rejected"""
        assert shortener.validate_long_url("") == False
    
    def test_generate_short_url(self, shortener):
        """Test that short URL is generated correctly"""
        assert shortener.generate_short_url("abc123") == "http://short.ly/abc123"
    
    def test_generate_short_url_different_base(self):
        """Test short URL generation with different base URL"""
        shortener = URLShortener("https://example.com")
        assert shortener.generate_short_url("xyz") == "https://example.com/xyz"
