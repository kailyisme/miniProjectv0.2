from src.ui_handlers import import_List_Options

def test():
    #assemble test
    def mock_readMenu(aString):
        list_a = []
        list_b = [["a", "not"], ["test", "successful"], ["Successful"]]
        return list_a, list_b
    
    expected = ["a", "test", "Successful"]
    
    #act on test
    
    result = import_List_Options("", mock_readMenu)
    
    #assert test result
    
    assert expected == result

if __name__ == "__main__":
    test()