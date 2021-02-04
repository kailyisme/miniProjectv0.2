from tests import test_promptUser as test_promptUser
from tests import test_importListOptions as test_importListOptions

if __name__ == "__main__":
    test_promptUser.test()
    test_importListOptions.test()
    print("Every test successful")