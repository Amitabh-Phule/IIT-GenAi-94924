def count_even_odd(numbers_str: str):
    """Count even and odd integers from a comma-separated string.

    Returns a tuple (num_even, num_odd).
    """
    parts = [p.strip() for p in numbers_str.split(',') if p.strip()]
    nums = []
    for p in parts:
        try:
            nums.append(int(p))
        except ValueError:
            continue
    num_even = sum(1 for n in nums if n % 2 == 0)
    num_odd = len(nums) - num_even
    return num_even, num_odd

def main():
    s = input('Enter numbers (comma-separated): ')
    even, odd = count_even_odd(s)
    print('Number of even numbers:', even)
    print('Number of odd numbers:', odd)

if __name__ == '__main__':
    main()
