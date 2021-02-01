import src.core as core

# class Empty:
#     pass

def test_promptUser():
    #assemble test
    mock_inputText = "  aTest  "
    
    def mock_input_func(str):
        return mock_inputText
    
    # mock_input = Empty()
    # mock_input.prompt = mock_input_func
    
    expected = "aTest"
    
    #act on test
    
    result = core.promptUser(mock_input_func)
    
    #assert test result
    
    assert expected == result
    print("Passed promptUser function test")

if __name__ == "__main__":
    test_promptUser()
    print("Every test successful")