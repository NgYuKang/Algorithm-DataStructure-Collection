from z_algo_code import z_algo


def pretty_print_maxtrix(matrix):
    for each in matrix:
        print(each)


def z_algo_suffix(input):
    n = len(input)
    zValues = [0 for i in range(n)]
    zValues[n - 1] = n

    prefix_index = n - 1
    z_index = n - 2
    z_score_current = 0
    while z_index >= 0 and input[prefix_index] == input[z_index]:
        z_score_current += 1
        z_index -= 1
        prefix_index -= 1
    zValues[n - 2] = z_score_current
    if z_score_current > 0:
        r = n - 2 - (z_score_current - 1)
        l = n - 2
    else:
        r = n - 1
        l = n - 1

    for k in range(n - 3, -1, -1):
        if k < r:
            prefix_index = n - 1
            z_index = k
            z_score_current = 0
            while z_index >= 0 and input[prefix_index] == input[z_index]:
                z_score_current += 1
                z_index -= 1
                prefix_index -= 1
            if z_score_current > 0:
                r = k - (z_score_current - 1)
                l = k
            zValues[k] = z_score_current
        else:
            # If the z value of the similar box less
            # than the length....
            if zValues[n - 1 - (l - k)] < k - r + 1:
                zValues[k] = zValues[n - 1 - (l - k)]
            else:
                if zValues[n - 1 - (l - k)] > k - r + 1:
                    zValues[k] = k - r + 1
                else:
                    z_index = r - 1
                    prefix_index = n - 1 - (k - r + 1)
                    while z_index >= 0 and input[prefix_index] == input[z_index]:
                        z_score_current += 1
                        z_index -= 1
                        prefix_index -= 1
                    zValues[k] = k - z_index
                    r = z_index + 1
                    l = k
    return zValues


def calc_extended_bad_char(pat):
    # if consider lower case only....
    num_char = 26
    start_num = 97
    # init memo
    extended_bad_char = [[-1 for i in range(num_char)] for i in range(len(pat))]
    # Iterate over len of pat (row)
    for i in range(1, len(pat)):
        # Iterate over number of char (the weight in knapsack we are allowed to carry)
        for char_code in range(0, num_char):
            exclude = extended_bad_char[i - 1][char_code]
            include = -1
            if i - 1 >= 0 and ord(pat[i - 1]) - start_num == char_code:
                include = i - 1
            extended_bad_char[i][char_code] = max(exclude, include)
    return extended_bad_char


def matched_prefix(pat):
    z_score = z_algo(pat)
    matched = [0 for i in range(len(pat) + 1)]
    for i in range(len(pat) - 1, -1, -1):
        z_score_current = z_score[i]
        prev = matched[i + 1]
        if i + z_score_current >= len(pat):
            matched[i] = max(prev, z_score_current)
        else:
            matched[i] = prev
    return matched


def boyer_moore(input, pat):
    start_num = 97

    bad_char = calc_extended_bad_char(pat)
    temp_list = []
    for i in range(len(pat) - 1, -1, -1):
        temp_list.append(pat[i])
    reversed_pat = ''.join(temp_list)
    temp_list = z_algo(reversed_pat)
    z_suffix = []
    for i in range(len(temp_list) - 1, -1, -1):
        z_suffix.append(temp_list[i])

    # Good suffix
    good_suffix = [0 for i in range(len(pat) + 1)]
    for i in range(1, len(pat)):
        j = len(pat) - z_suffix[i - 1] + 1
        good_suffix[j - 1] = i
    matched_prefix_pat = matched_prefix(pat)

    input_iter = 0
    pat_iter = len(pat) - 1
    index_match = []
    start, stop = -1, -1

    while input_iter + len(pat) - 1 < len(input):  # Loop through the text
        # Loop through the pattern
        # compare text and pat from right to left
        while pat_iter > stop and input[input_iter + pat_iter] == pat[pat_iter]:
            pat_iter -= 1
        # Skip over places that we know already matches galil optimization
        if start >= 0 and stop >= 0 and pat_iter == stop:
            pat_iter = start - 1
        while pat_iter >= 0 and input[input_iter + pat_iter] == pat[pat_iter]:
            pat_iter -= 1

        shift_bad_char_cur = pat_iter - bad_char[pat_iter][ord(input[input_iter + pat_iter]) - start_num] \
            if bad_char[pat_iter][ord(input[input_iter + pat_iter]) - start_num] < pat_iter else 1
        shift_good_suffix_cur = 1
        if pat_iter < 0:
            shift_good_suffix_cur = len(pat) - matched_prefix_pat[1]
            index_match.append(input_iter)
            start = 0
            stop = matched_prefix_pat[1] - 1
        elif good_suffix[pat_iter + 1] > 0:
            shift_good_suffix_cur = len(pat) - good_suffix[pat_iter + 1]
            start = good_suffix[pat_iter + 1] - len(pat) + pat_iter
            stop = good_suffix[pat_iter + 1] - 1
        elif good_suffix[pat_iter + 1] == 0:
            shift_good_suffix_cur = len(pat) - matched_prefix_pat[pat_iter + 1]
            start = 0
            stop = matched_prefix_pat[pat_iter + 1] - 1
        input_iter += max(shift_bad_char_cur, shift_good_suffix_cur)
        pat_iter = len(pat) - 1

    return index_match


def kmp(input, pat):
    z_score_pat = z_algo(pat)
    sp_val = [0 for i in range(len(pat))]

    # Init sp_val
    for j in range(len(pat) - 1, 0, -1):
        i = j + z_score_pat[j] - 1
        sp_val[i] = z_score_pat[j]
    pat_iter = 0
    str_iter = 0

    index_found = []
    while str_iter + len(pat) - 1 < len(input):
        while pat_iter < len(pat) and input[str_iter + pat_iter] == pat[pat_iter]:
            pat_iter += 1
        # If found pattern
        if pat_iter == len(pat):
            index_found.append(str_iter)
            str_iter += (len(pat) - sp_val[len(pat) - 1])
        # Mismatch at pat_iter (i+1)
        else:
            # Go back to the index before mismatch
            # if mismatch on first index, make it 0
            pat_iter = max(0, pat_iter - 1)
            sp_val_i = sp_val[pat_iter]
            # Max function makes sure at least shift by 1
            str_iter += max((pat_iter - sp_val_i), 1)
        pat_iter = 0
    return index_found


def hammingdist_one(text, pat):
    z_pre = z_algo("".join([pat, "$", text]))
    z_suf = z_algo("".join([text, "$", pat])[::-1])[::-1]

    ret = []
    for i in range(len(pat) + 1, len(z_pre)):
        z_pre_val = z_pre[i]
        z_suf_val = z_suf[i - 2]
        final_val = min(z_pre_val + z_suf_val, max(z_pre_val, z_suf_val))
        if len(pat) - final_val == 0 or len(pat) - final_val == 1:
            ret.append(i - len(pat) - 1)
    return ret


if __name__ == '__main__':
    print(boyer_moore("bbbbabbbbbbabb", "bbbb"))
    print(kmp("bbbbabbbbbbabb", "bbbb"))