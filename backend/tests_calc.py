from app.services.calc import calculate_pages_read, completions_in_log

def test_circular_math():
    # Normal range
    assert calculate_pages_read(1, 10) == 10
    assert calculate_pages_read(10, 10) == 1
    assert calculate_pages_read(1, 600) == 600
    
    # Wrap-around
    # 595 to 5 should be (600-595+1) + 5 = 6 + 5 = 11
    assert calculate_pages_read(595, 5) == 11
    
    # Wrap-around 600 to 1
    assert calculate_pages_read(600, 1) == 2
    
    print("✅ Circular math tests passed!")

def test_completion_detection():
    # Wrap detection
    assert completions_in_log(595, 5) == 1
    
    # Finish at 600
    assert completions_in_log(580, 600) == 1
    
    # Normal reading
    assert completions_in_log(1, 100) == 0
    
    print("✅ Completion detection tests passed!")

if __name__ == "__main__":
    try:
        test_circular_math()
        test_completion_detection()
    except AssertionError as e:
        print(f"❌ Tests failed: {e}")
