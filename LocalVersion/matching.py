degenerate_sequence = 'AA[CGT]G[AG]T[AT]CG[AG]TATC[ACGT]C[GT]G'
pattern = 'ACGGTA'
sequence = 'ATCGTAGGCAG'
degenerate_pattern = '[ACG]G'

print('Please enter text: ', end='')
s = input()
print('Please enter pattern: ', end='')
p = input()

# sequence and pattern are both degenerate string
if ((s.find('[') != -1) or (s.find('N') != -1)) and ((p.find('[') != -1) or (p.find('N') != -1)):
    print('Text and pattern can not both be degenerate string.')

# sequence and pattern are not both DNA or not both RNA
if ((s.find('T') != -1) and (p.find('U') != -1)) or ((s.find('U') != -1) and (p.find('T') != -1)):
    print('Text and pattern are not both DNA or not both RNA.')

# Determine characters Σ contains
sigma = []
if (s.find('A') != -1) or (p.find('A') != -1):
    sigma.append('A')
if (s.find('C') != -1) or (p.find('C') != -1):
    sigma.append('C')
if (s.find('G') != -1) or (p.find('G') != -1):
    sigma.append('G')
if (s.find('T') != -1) or (p.find('T') != -1):
    sigma.append('T')
elif (s.find('U') != -1) or (p.find('U') != -1):
    sigma.append('U')
# print('Σ: ' + str(sigma))

# process degenerate string
process_s = []
process_p = []
s_actual_index = []

i = 0
while i < len(s):
    temp_subset = []
    s_actual_index.append(i)
    if s[i] != '[':
        temp_subset.append(s[i])
        i += 1
    else:
        for k in range(i + 1, len(s)):
            if s[k] != ']':
                temp_subset.append(s[k])
            else:
                i = k + 1
                break
    process_s.append(temp_subset)
# print(process_s)
# print(s_actual_index)
i = 0
while i < len(p):
    temp_subset = []
    if p[i] != '[':
        temp_subset.append(p[i])
        i += 1
    else:
        for k in range(i + 1, len(p)):
            if p[k] != ']':
                temp_subset.append(p[k])
            else:
                i = k + 1
                break
    process_p.append(temp_subset)
# print(process_p)

M_list = []
for a in sigma:
    s_prime = []
    p_prime = []
    # Construct S‘
    for item in process_s:
        if a in item:
            s_prime.append(1)
        else:
            s_prime.append(0)
    # Construct P'
    for item in process_p:
        if a in item:
            p_prime.append(1)
        else:
            p_prime.append(0)
    # print(a, end=': s:')
    # print(s_prime, end=', p:')
    # print(p_prime)
    # Construct Ma
    Ma = []
    for i in range(0, len(s_prime) - len(p_prime) + 1):
        bitwise_and = []
        sub_s_prime = []
        for k in range(0, len(p_prime)):
            bitwise_and.append(p_prime[k] & s_prime[i + k])
            sub_s_prime.append(s_prime[i + k])
        # print(sub_s_prime)
        # problem 1: degenerate text T and a pattern P.
        if s.find('[') != -1 or (s.find('[') == -1 and p.find('[') == -1):
            if bitwise_and == p_prime:
                Ma.append(1)
            else:
                Ma.append(0)
        # problem 2: text T and a degenerate pattern P.
        elif p.find('[') != -1:
            # print('sub_s:', end='')
            # print(s_prime[i:i + len(p_prime):])
            if bitwise_and == sub_s_prime:
                Ma.append(1)
            else:
                Ma.append(0)
    # print(Ma)
    M_list.append(Ma)
M = []
for i in range(0, len(M_list[0])):
    temp_bit = 1
    for k in range(0, len(sigma)):
        temp_bit = temp_bit & M_list[k][i]
    M.append(temp_bit)
# print(M)
result = []
for i in range(0, len(M)):
    if M[i] == 1:
        result.append(i + 1)
# show the matching pattern in sequence
result_in_s = s
insert_symbol = ['$', '|', '%', '*', '#', '@', '^']
symbol_count = 0
temp_result = [x - 1 for x in result]
# print(temp_result)
for item in temp_result:
    result_in_s = result_in_s[:s_actual_index[item]] + insert_symbol[symbol_count % 6] + result_in_s[s_actual_index[item]:]
    # print(result_in_s)
    for k in range(item, len(s_actual_index)):
        s_actual_index[k] = s_actual_index[k] + 1
    # print(s_actual_index)
    if item + len(process_p) >= len(s_actual_index):
        result_in_s = result_in_s + insert_symbol[symbol_count % 6]
    else:
        result_in_s = result_in_s[:s_actual_index[item + len(process_p)]] + insert_symbol[symbol_count % 6] + result_in_s[s_actual_index[item + len(process_p)]:]
    # print(result_in_s)
    for k in range(item + len(process_p), len(s_actual_index)):
        s_actual_index[k] = s_actual_index[k] + 1
    # print(s_actual_index)
    symbol_count += 1
if len(result) == 0:
    result.append(-1)
print('The starting positions: ', end='')
print(result)
print('The result displayed in original text: ', end='')
print(result_in_s)
