class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Find the length of the longest substring without duplicate characters.
        
        Time Complexity: O(n) where n is the length of the string
        Space Complexity: O(min(m, n)) where m is the charset size
        """
        char_index = {}  # Store the most recent index of each character
        max_length = 0
        left = 0  # Left pointer of the sliding window
        
        for right in range(len(s)):
            char = s[right]
            
            # If character is already in our current window, move left pointer
            if char in char_index and char_index[char] >= left:
                left = char_index[char] + 1
            
            # Update the character's most recent index
            char_index[char] = right
            
            # Update max length
            max_length = max(max_length, right - left + 1)
        
        return max_length


# Test cases
def test_solution():
    sol = Solution()
    
    # Example 1
    assert sol.lengthOfLongestSubstring("abcabcbb") == 3
    print("Test 1 passed: 'abcabcbb' -> 3")
    
    # Example 2
    assert sol.lengthOfLongestSubstring("bbbbb") == 1
    print("Test 2 passed: 'bbbbb' -> 1")
    
    # Example 3
    assert sol.lengthOfLongestSubstring("pwwkew") == 3
    print("Test 3 passed: 'pwwkew' -> 3")
    
    # Edge cases
    assert sol.lengthOfLongestSubstring("") == 0
    print("Test 4 passed: '' -> 0")
    
    assert sol.lengthOfLongestSubstring("a") == 1
    print("Test 5 passed: 'a' -> 1")
    
    assert sol.lengthOfLongestSubstring("abcdef") == 6
    print("Test 6 passed: 'abcdef' -> 6")
    
    assert sol.lengthOfLongestSubstring("aab") == 2
    print("Test 7 passed: 'aab' -> 2")
    
    print("\nAll tests passed!")

# Run tests
test_solution()
