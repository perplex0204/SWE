#
# @lc app=leetcode id=10 lang=python3
#
# [10] Regular Expression Matching
#

# Solution 1: Import re
import re


class Solution1:
    def isMatch(self, s: str, p: str) -> bool:
        print(re.match(f"^{p}$", s))
        if (re.match(f"^{p}$", s)) == None:
            return False
        else:
            return True


# Solution 2: Backtracking
class Solution2:
    def isMatch(self, string: str, pattern: str) -> bool:
        i, j = len(string) - 1, len(pattern) - 1
        ans = self.backtrack({}, string, pattern, i, j)
        return ans

    def backtrack(self, cache, string, pattern, i, j):
        key = (i, j)
        if key in cache:
            return cache[key]

        # 傳入pattern跟string的長度為-1，表示已經比對完了
        if i == -1 and j == -1:
            cache[key] = True
            return True

        # 傳入pattern的長度為-1，表示已經比對完了，但string還有剩，代表不匹配
        # i!= -1 代表string還有剩
        if i != -1 and j == -1:
            cache[key] = False
            return cache[key]

        # 傳入的string長度為-1，pattern還有剩，代表pattern還有可能是匹配的
        if i == -1 and pattern[j] == '*':
            k = j
            while k != -1 and pattern[k] == '*':
                k -= 2

            if k == -1:
                cache[key] = True
                return cache[key]

            cache[key] = False
            return cache[key]

        if i == -1 and pattern[j] != '*':
            cache[key] = False
            return cache[key]

        if pattern[j] == '*':
            if self.backtrack(cache, string, pattern, i, j - 2):
                cache[key] = True
                return cache[key]

            if pattern[j - 1] == string[i] or pattern[j - 1] == '.':
                if self.backtrack(cache, string, pattern, i - 1, j):
                    cache[key] = True
                    return cache[key]

        if pattern[j] == '.' or string[i] == pattern[j]:
            if self.backtrack(cache, string, pattern, i - 1, j - 1):
                cache[key] = True
                return cache[key]

        cache[key] = False
        return cache[key]


# Solution 3 : DP
class Solution3:
    def isMatch(self, s: str, p: str) -> bool:
        # 在主函數 isMatch 中，它首先初始化一個名為 memo 的字典，
        # 用於儲存已經計算過的子問題結果，這是動態規劃中的 "Memoization" 技術。
        memo = {}

        # 定義一個內部輔助函數 dp(i: int, j: int) -> bool，傳入i、j兩個int，且返回一個bool值。
        # 它被用來計算 s[i:] 和 p[j:] 是否匹配。
        # 如果已經計算過這個問題，就直接從 memo 中返回結果。
        def dp(i: int, j: int) -> bool:
            # 如果已經計算過這個問題，就直接從 memo 中返回結果。
            if (i, j) in memo:
                return memo[(i, j)]

            # 如果j已經到達p的尾部，代表p已經匹配完了
            # 如果i也到達s的尾部，代表s也匹配完了，返回True，否則返回False
            # ，也就是說，如果p匹配完了，但是s還沒有匹配完的話，那代表不匹配。
            if j == len(p):
                return i == len(s)

            # 第一次match，有兩個判斷條件：
            # 1. i < len(s) 代表s還沒有匹配完
            # 2. p[j] == s[i] or p[j] == '.' 代表p[j]跟s[i]匹配
            # 若兩者皆符合，代表第一次match成功，first_match = True
            first_match = i < len(s) and (p[j] == s[i] or p[j] == '.')

            # 接下來需判斷兩個條件以確定後面有沒有'*'：
            # 1. j + 1 < len(p)，代表p還沒有匹配完
            # 2. p[j+1] == '*'，代表p[j+1]是'*'，像是a*或是.*這樣的pattern
            # ans = dp(i, j+2) or (first_match and dp(i+1, j))
            # 若其中之一不符合，代表接下來沒有'*'，則ans = first_match and dp(i+1, j+1)
            if j + 1 < len(p) and p[j+1] == '*':
                # 這裡的兩種情況代表了'*'的兩種作用：
                # 1. '*'代表0個前面的字元，所以直接跳過'*'跟'*'前面的字元，繼續比對
                # 2. '*'代表1個或多個前面的字元，所以'*'前面的字元跟s[i]匹配，然後繼續比對
                ans = dp(i, j+2) or (first_match and dp(i+1, j))
            else:
                ans = first_match and dp(i+1, j+1)

            memo[(i, j)] = ans
            print(memo)
            return ans

        return dp(0, 0)


print(Solution1().isMatch("abc", "a*bccccc"))

# @lc code=end
