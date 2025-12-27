import math_utils


def main():
    print("Area Calculator")
    print("1. Circle")
    print("2. Rectangle")
    print("3. Triangle")
    print("4. Square")

    choice = input("Enter your choice (1-4): ").strip()

    try:
        if choice == "1":
            radius = float(input("Enter radius: "))
            area = math_utils.area_circle(radius)
            print(f"Area of Circle: {area:.2f}")

        elif choice == "2":
            length = float(input("Enter length: "))
            width = float(input("Enter width: "))
            area = math_utils.area_rectangle(length, width)
            print(f"Area of Rectangle: {area:.2f}")

        elif choice == "3":
            base = float(input("Enter base: "))
            height = float(input("Enter height: "))
            area = math_utils.area_triangle(base, height)
            print(f"Area of Triangle: {area:.2f}")

        elif choice == "4":
            side = float(input("Enter side: "))
            area = math_utils.area_square(side)
            print(f"Area of Square: {area:.2f}")

        else:
            print("Invalid choice.")

    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
