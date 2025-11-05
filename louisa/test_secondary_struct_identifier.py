from get_secondary_struct import identify_secondary_structure_spans

ss1 = "   EEEEE   HHHHHHHH  EEEEE   IGNOR EEEEEE   HHHHHHHHHHH  EEEEE  HHHH   "
expected1 = [(4, 8), (12, 19), (22, 26), (36, 41), (45, 55), (58, 62), (65, 68)]

ss2 = "HHHHHHH   HHHHHHHHHHHH      HHHHHHHHHHHHEEEEEEEEEEHHHHHHH EEEEHHH "
expected2 = [(1, 7), (11, 22), (29, 40), (41, 50), (51, 57), (59, 62), (63, 65)]

ss3 = "EEEEEEEEE EEEEEEEE EEEEEEEEE H EEEEE H H H EEEEEEEE"
expected3 = [(1,9), (11, 18), (20, 28), (30, 30), (32, 36), (38, 38), (40, 40), (42, 42), (44, 51)]

input_list=[ss1,ss2,ss3]
expected_list=[expected1, expected2, expected3]

def test_secondary_struct_identifier():
    for ele in range(len(input_list)):
        print((input_list[ele]))
        # assert identify_secondary_structure_spans(input_list[ele]) == expected_list[ele]