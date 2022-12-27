def compare(input, k):
    num_matches = 0
    iter = 0
    while k < len(input) and iter < len(input):
        if input[iter] == input[k]:
            num_matches += 1
        else:
            break
        k += 1
        iter += 1
    return num_matches


def naive_z_algo(input):
    n = len(input)
    zValues = [0 for i in range(n)]
    zValues[0] = n

    for i in range(1, n):
        num_matches = compare(input, i)
        zValues[i] = num_matches
    return zValues


def z_algo(input):
    n = len(input)
    zValues = [0 for i in range(n)]
    zValues[0] = n

    prefix_index = 0
    z_index = 1
    z_score_current = 0
    while z_index < n and input[prefix_index] == input[z_index]:
        z_score_current += 1
        z_index += 1
        prefix_index += 1
    zValues[1] = z_score_current
    if z_score_current > 0:
        r = z_score_current
        l = 1
    else:
        r = 0
        l = 0

    m = 2
    if z_score_current > 0:
        while m < len(input) and z_score_current > 0:
            zValues[m] = z_score_current - 1
            z_score_current -= 1
            m += 1

    for k in range(m, n):
        if k > r:
            prefix_index = 0
            z_index = k
            z_score_current = 0
            while z_index < n and input[prefix_index] == input[z_index]:
                z_score_current += 1
                z_index += 1
                prefix_index += 1
            if z_score_current > 0:
                r = z_index - 1
                l = k
            zValues[k] = z_score_current
        else:
            # If the z value of the similar box less
            # than the length....
            if zValues[k - l] < r - k + 1:
                zValues[k] = zValues[k - l]
            else:
                if zValues[k - l] > r - k + 1:
                    zValues[k] = r - k + 1
                else:
                    z_index = r + 1
                    prefix_index = r - k + 1
                    while z_index < n and input[prefix_index] == input[z_index]:
                        z_score_current += 1
                        z_index += 1
                        prefix_index += 1
                    zValues[k] = z_index - k
                    r = z_index - 1
                    l = k
    return zValues


def find_pattern(input_str: str, pat: str):
    combined = pat + "$" + input_str
    z_score = z_algo(combined)
    output = []
    for i in range(len(pat) + 1, len(z_score)):
        if z_score[i] == len(pat):
            output.append(i - len(pat) - 1)
    return output

