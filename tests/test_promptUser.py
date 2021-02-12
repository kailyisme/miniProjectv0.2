from src.ui_handlers import prompt_User

def test():
    #assemble test
    mock_inputText = "  aTest  "
    
    def mock_input_func(aString, **kwargs):
        return mock_inputText
    
    # mock_input = Empty()
    # mock_input.prompt = mock_input_func
    
    expected = "aTest"
    
    #act on test
    
    result = prompt_User(None,None,mock_input_func)

    #assert test result
    
    assert expected == result

if __name__ == "__main__":
    test()