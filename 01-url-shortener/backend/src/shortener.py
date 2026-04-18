"""Base62 encoding and short code generation logic"""


class Base62Encoder:
    """Encodes/decodes numbers to/from Base62 strings"""
    
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    @staticmethod
    def encode(num: int) -> str:
        """
        Encode a decimal number to Base62 string.
        
        Args:
            num: Non-negative integer to encode
            
        Returns:
            str: Base62 encoded string
            
        Examples:
            encode(0) -> "0"
            encode(1) -> "1"
            encode(9) -> "9"
            encode(10) -> "a"
            encode(61) -> "Z"
            encode(62) -> "10"
            encode(100) -> "1w"
            encode(1000) -> "g8"
        """
        BASE = 62
        result = ''
        while num > 0:
            num, remainder = divmod(num, 62)
            result += Base62Encoder.ALPHABET[remainder]
        return result[::-1] if result else '0'


    
    @staticmethod
    def decode(code: str) -> int:
        """
        Decode a Base62 string back to decimal number.
        
        Args:
            code: Base62 encoded string
            
        Returns:
            int: Decoded decimal number
            
        Examples:
            decode("0") -> 0
            decode("a") -> 10
            decode("Z") -> 61
            decode("10") -> 62
            decode("1w") -> 100
            decode("g8") -> 1000
        """
        BASE = 62
        position_multiplier = 1               
        num = 0
        for char in reversed(code):
            num += position_multiplier * Base62Encoder.ALPHABET.index(char)
            position_multiplier *= 62
        return num


class URLShortener:
    """Handles URL shortening logic"""
    
    def __init__(self, base_url: str):
        """
        Initialize URL shortener.
        
        Args:
            base_url: Base URL for short links (e.g., 'http://short.ly')
        """
        self._base_url = base_url
    
    def generate_short_url(self, short_code: str) -> str:
        """
        Generate full short URL from short code.
        
        Args:
            short_code: Short code (e.g., 'abc123')
            
        Returns:
            str: Full short URL (e.g., 'http://short.ly/abc123')
        """
        return self._base_url + '/' + short_code
    
    def validate_long_url(self, url: str) -> bool:
        """
        Validate that URL is a valid HTTP/HTTPS URL.
        
        Args:
            url: URL to validate
            
        Returns:
            bool: True if URL is valid
        """
        REASONABLE_LENGTH = 2048
        if not isinstance(url, str):
            return False
        url = url.strip()
        if not url or len(url) >= REASONABLE_LENGTH or (not url.startswith('http://') and not url.startswith('https://')): 
            return False
        return True
