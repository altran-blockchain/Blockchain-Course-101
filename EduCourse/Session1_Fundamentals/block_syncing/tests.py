from test_helper import run_common_tests, failed, passed, get_answer_placeholders


answer_conditions = ["list()", "load_from_dict(block_dict)" "is_valid(cur_block)", "append(cur_block)"]

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
