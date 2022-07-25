from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app, supports_credentials=True)


# Determine what characters Σ contains
def get_sigma(s, p):
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
    return sigma


# Process degenerate string, each bit is represented by a list
def process_string(string):
    actual_index = []
    process_str = []
    i = 0
    while i < len(string):
        temp_subset = []
        actual_index.append(i)
        if string[i] != '[':
            temp_subset.append(string[i])
            i += 1
        else:
            for k in range(i + 1, len(string)):
                if string[k] != ']':
                    temp_subset.append(string[k])
                else:
                    i = k + 1
                    break
        process_str.append(temp_subset)
    return process_str, actual_index


"""
Determine the type of problem
return code: 1 represents a normal text T and a normal pattern P or problem 1: a degenerate text T and a normal pattern P.
             2 represents problem 2: a normal text T and a degenerate pattern P.
"""
def get_type(s, p):
    if s.find('[') != -1 or (s.find('[') == -1 and p.find('[') == -1):
        return 1
    elif p.find('[') != -1:
        return 2


# Calculate Ma
def calculate_ma(a, process_s, process_p, problem_type):
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
        # Construct Ma
        Ma = []
        for i in range(0, len(s_prime) - len(p_prime) + 1):
            bitwise_and = []
            sub_s_prime = []
            for k in range(0, len(p_prime)):
                bitwise_and.append(p_prime[k] & s_prime[i + k])
                sub_s_prime.append(s_prime[i + k])
            # problem 1: degenerate text T and a pattern P.
            if problem_type == 1:
                if bitwise_and == p_prime:
                    Ma.append(1)
                else:
                    Ma.append(0)
            # problem 2: text T and a degenerate pattern P.
            elif problem_type == 2:
                if bitwise_and == sub_s_prime:
                    Ma.append(1)
                else:
                    Ma.append(0)
    return Ma


# Calculate M
def calculate_m(m_list, sigma_length):
    m = []
    for i in range(0, len(m_list[0])):
        temp_bit = 1
        for k in range(0, sigma_length):
            temp_bit = temp_bit & m_list[k][i]
        m.append(temp_bit)
    return m


# The pattern of a match marked in a sequence with a special symbol
def show_in_sequence(s, temp_result, s_actual_index, p_length):
    result_in_s = s
    insert_symbol = ['$', '|', '%', '*', '#', '@', '^']
    symbol_count = 0
    for item in temp_result:
        result_in_s = result_in_s[:s_actual_index[item]] + insert_symbol[symbol_count % 6] + result_in_s[
                                                                                             s_actual_index[item]:]
        for k in range(item, len(s_actual_index)):
            s_actual_index[k] = s_actual_index[k] + 1
        if item + p_length >= len(s_actual_index):
            result_in_s = result_in_s + insert_symbol[symbol_count % 6]
        else:
            result_in_s = result_in_s[:s_actual_index[item + p_length]] + insert_symbol[
                symbol_count % 6] + result_in_s[s_actual_index[item + p_length]:]
        for k in range(item + p_length, len(s_actual_index)):
            s_actual_index[k] = s_actual_index[k] + 1
        symbol_count += 1
    return result_in_s


def get_result(s, p):
    # sequence and pattern are both degenerate string
    if (s.find('[') != -1) and (p.find('[') != -1):
        print('s and p can not both be degenerate string')
        return [], [-2]

    # sequence and pattern are not both DNA or not both RNA
    if ((s.find('T') != -1) and (p.find('U') != -1)) or ((s.find('U') != -1) and (p.find('T') != -1)):
        print('Must not match')
        return [], [-1]

    # get Σ
    sigma = get_sigma(s, p)

    process_s, s_actual_index = process_string(s)
    process_p, p_actual_index = process_string(p)

    # get problem type
    problem_type = get_type(s, p)

    # calculate Ma
    m_list = []
    for a in sigma:
        m_list.append(calculate_ma(a, process_s, process_p, problem_type))

    # calculate M
    m = calculate_m(m_list, len(sigma))

    # find occurrences' starting index
    result_index = []
    for i in range(0, len(m)):
        if m[i] == 1:
            result_index.append(i + 1)

    # show the matching result in original sequence
    result_in_sequence = show_in_sequence(s, [x - 1 for x in result_index], s_actual_index, len(process_p))

    # No matching
    if len(result_index) == 0:
        result_index.append(-1)
    return result_in_sequence, result_index


@app.route('/matching', methods=['POST'])
def match():
    sequence_list = request.form.getlist('sequences')
    pattern_list = request.form.getlist('patterns')
    result_list_in_sequence = []
    result_index_list = []
    for sequence in sequence_list:
        for pattern in pattern_list:
            result_in_sequence, result_index = get_result(sequence, pattern)
            result_list_in_sequence.append(result_in_sequence)
            result_index_list.append(result_index)
    return {'result_index': result_index_list, 'result_sequence': result_list_in_sequence}


if __name__ == '__main__':
    # The front end and back end are on the LAN
    app.run(host='0.0.0.0', threaded=True, debug=True)
    # The front end and back end are in the same machine
    # app.run(threaded=True, debug=True)
