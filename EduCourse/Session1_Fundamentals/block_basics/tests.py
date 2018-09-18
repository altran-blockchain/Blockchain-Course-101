from test_helper import run_common_tests, failed, passed, get_answer_placeholders


answer_conditions = ["self.index", "self.timestamp", "self.prev_hash", "self.data", "self.hash", "self.nonce",
                     "test_block.block"]

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
    test_answer_placeholders()


