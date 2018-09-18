from test_helper import run_common_tests, failed, passed, get_answer_placeholders


answer_conditions = ["sha_obj.hexdigest()","calculate_hash(block.nonce)", "str(hash_to_check)[0:NUM_ZEROS] == '0'*NUM_ZEROS",
                     "difficulty_condition"]

def test_answer_placeholders():
    placeholders = get_answer_placeholders()
    for placeholder,answer in zip(placeholders,answer_conditions):
        if placeholder == answer.lstrip().rstrip():       # TODO: your condition here
            passed()
        else:
            print "Expected",answer
            failed()


if __name__ == '__main__':
    run_common_tests()
    test_answer_placeholders()       # TODO: uncomment test call
