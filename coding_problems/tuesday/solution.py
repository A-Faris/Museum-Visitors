def longest_palindrome(s):
    long_length = 0
    for num in range(len(s)):
        for length in range(len(s[num:])):
            check = s[num:length+num+1]
            if check == check[::-1]:
                long_length = max(long_length, len(check))
    return long_length
