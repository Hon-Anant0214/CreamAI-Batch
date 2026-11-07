print(f"GATENavigator")
print(f"Your GATE Preparation Assistant")
while True:

    print(f"Maain Menu")
    print(f"1.About GATENavigator")
    print(f"2.Sample questions")
    print(f"3.Check your score")
    print(f"0.Exit")
    n = int(input("enter your choice: "))

    if n==1:
        print("GATENavigator is an AI-powered educational assistant designed to help students prepare for the Graduate Aptitude Test in Engineering (GATE). It provides study resources, answers questions, explains technical concepts, and helps students practice for the examination.")
        
    elif n== 2:
        print(f"What is an Operating System?")
        print(f"Explain the difference between RAM and ROM.")
        print(f"What is a data structure?")
        print(f"Explain the difference between stack and queue.")
        

    elif n == 3:
        j = int(input("Enter your score"))
        if j <= 80:
            print("Good score")
        elif j >= 80 and j <= 60:
            print("average score")
        else:
            print("work hard")
        



