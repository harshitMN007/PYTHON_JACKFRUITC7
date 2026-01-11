def check_password_strength(password):
    feedback = []
    
    length_score = 0
    if len(password) >= 16:
        length_score = 3
    elif len(password) >= 12:
        length_score = 2
    elif len(password) >= 8:
        length_score = 1
    else:
        feedback.append("Length: Too short (minimum 8 characters required)")
    
    has_upper = False
    for c in password:
        if c.isupper():
            has_upper = True
            break
    
    has_lower = False
    for c in password:
        if c.islower():
            has_lower = True
            break
    
    has_digit = False
    for c in password:
        if c.isdigit():
            has_digit = True
            break
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:'\",.<>?/`~"
    has_special = False
    for c in password:
        if c in special_chars:
            has_special = True
            break
    
    char_score = 0
    if has_upper:
        char_score += 1
    else:
        feedback.append("Missing: Uppercase letter (A-Z)")
    
    if has_lower:
        char_score += 1
    else:
        feedback.append("Missing: Lowercase letter (a-z)")
    
    if has_digit:
        char_score += 1
    else:
        feedback.append("Missing: Number (0-9)")
    
    if has_special:
        char_score += 1
    else:
        feedback.append("Missing: Special character (!@#$%)")
    
    total_score = length_score + char_score
    
    if total_score <= 2:
        strength = "😭🔴VERY WEAK🔴😭"
    elif total_score <= 4:
        strength = "☹️🟠WEAK🟠☹️ "
    elif total_score <= 5:
        strength = "😐🟡MEDIUM🟡😐"
    else:
        strength = "😃🟢STRONG🟢😃"	
    
    print("\n" + "="*60)
    print("PASSWORD STRENGTH ANALYZER")
    print("="*60)
    print(f"Length: {len(password)} characters")
    print(f"Score: {total_score}/7 ({total_score/7*100:.0f}%)")
    print(f"Strength: {strength}")
    print("-"*60)
    
    if feedback:
        print("REQUIREMENTS MISSING:")
        for issue in feedback:
            print(issue)
    else:
        print("All password requirements met successfully!")
    
    print("="*60)

print("PROFESSIONAL PASSWORD STRENGTH CHECKER")
print("Enter 'quit' to exit\n")

while True:
    pwd = input("Enter password to analyze: ").strip()
    if pwd.lower() == 'quit':
        print("Password analysis complete.")
        break
    if not pwd:
        print("Please enter a password.\n")
        continue
    check_password_strength(pwd)
    print()