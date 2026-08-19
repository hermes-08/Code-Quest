import json
import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Recruit

#HELPER FUNCTION: GET RECRUIT CONTEXT
def get_recruit_context(request):
    """Ensures sidebar and quest status always have data if logged in."""
    if request.user.is_authenticated:
        try:
            return {'recruit': request.user.recruit}
        except Recruit.DoesNotExist:
            return {}
    return {}

#  QUEST DATA: 8 Boxes with 10 Questions Each (Choice and Text Types)
QUEST_DATA = {
    'box1': [
        {'id': 1, 'type': 'choice', 'q': 'What is the output of print(2+2)?', 'options': ['2', '4', '22'], 'a': '4'},
        {'id': 2, 'type': 'choice', 'q': 'Which is a string?', 'options': ['"Hello"', '5', 'True'], 'a': '"Hello"'},
        {'id': 3, 'type': 'choice', 'q': 'How do you start a comment?', 'options': ['//', '/*', '#'], 'a': '#'},
        {'id': 4, 'type': 'choice', 'q': 'What does int() do?', 'options': ['Decimal', 'Whole Number', 'Text'], 'a': 'Whole Number'},
        {'id': 5, 'type': 'choice', 'q': 'Define a variable "x" as 5.', 'options': ['x : 5', 'x = 5', 'let x = 5'], 'a': 'x = 5'},
        {'id': 101, 'type': 'choice', 'q': 'What is the correct way to output "Hello World"?', 'options': ['echo("Hello")', 'print("Hello")', 'p("Hello")'], 'a': 'print("Hello")'},
        {'id': 102, 'type': 'choice', 'q': 'Which is a float?', 'options': ['5', '5.0', '"5"'], 'a': '5.0'},
        {'id': 103, 'type': 'choice', 'q': 'Result of 10 / 2?', 'options': ['5', '5.0', '2'], 'a': '5.0'},
        {'id': 104, 'type': 'choice', 'q': 'Which is a boolean?', 'options': ['True', '"True"', 'true'], 'a': 'True'},
        {'id': 105, 'type': 'choice', 'q': 'What does type(5) return?', 'options': ['<class "int">', '<class "str">', 'integer'], 'a': '<class "int">'},
    ],
    'box2': [
        {'id': 6, 'type': 'choice', 'q': 'Which symbol is "Equal to"?', 'options': ['=', '==', '!='], 'a': '=='},
        {'id': 7, 'type': 'choice', 'q': 'What follows an "if" statement?', 'options': [':', ';', '.'], 'a': ':'},
        {'id': 8, 'type': 'choice', 'q': 'Which keyword is for a "catch-all"?', 'options': ['else', 'elif', 'otherwise'], 'a': 'else'},
        {'id': 9, 'type': 'choice', 'q': 'Check if "x" is NOT equal to 5?', 'options': ['x <> 5', 'x not 5', 'x != 5'], 'a': 'x != 5'},
        {'id': 10, 'type': 'choice', 'q': 'Result of (5 > 3 and 2 > 4)?', 'options': ['True', 'False', 'None'], 'a': 'False'},
        {'id': 106, 'type': 'choice', 'q': 'Keyword for "else if" in Python?', 'options': ['else if', 'elseif', 'elif'], 'a': 'elif'},
        {'id': 107, 'type': 'choice', 'q': 'Result of (not True)?', 'options': ['True', 'False', 'None'], 'a': 'False'},
        {'id': 108, 'type': 'choice', 'q': 'Which checks if 5 is less than or equal to 10?', 'options': ['5 <= 10', '5 < 10', '5 =< 10'], 'a': '5 <= 10'},
        {'id': 109, 'type': 'choice', 'q': 'Result of (True or False)?', 'options': ['True', 'False', 'None'], 'a': 'True'},
        {'id': 110, 'type': 'choice', 'q': 'Symbol for modulo (remainder)?', 'options': ['/', '//', '%'], 'a': '%'},
    ],
    'box3': [
        {'id': 11, 'type': 'choice', 'q': 'Which loop runs while true?', 'options': ['for', 'while', 'if'], 'a': 'while'},
        {'id': 12, 'type': 'choice', 'q': 'How do you stop a loop?', 'options': ['stop', 'exit', 'break'], 'a': 'break'},
        {'id': 13, 'type': 'choice', 'q': 'Function for a sequence 0-4?', 'options': ['list()', 'range()', 'seq()'], 'a': 'range()'},
        {'id': 14, 'type': 'choice', 'q': 'Loop keyword to pick items?', 'options': ['in', 'from', 'at'], 'a': 'in'},
        {'id': 15, 'type': 'choice', 'q': 'What is an infinite loop?', 'options': ['Runs once', 'Never runs', 'Runs forever'], 'a': 'Runs forever'},
        {'id': 111, 'type': 'choice', 'q': 'Range(3) produces which numbers?', 'options': ['1,2,3', '0,1,2,3', '0,1,2'], 'a': '0,1,2'},
        {'id': 112, 'type': 'choice', 'q': 'Which loop is best for a known number of items?', 'options': ['while', 'for', 'if'], 'a': 'for'},
        {'id': 113, 'type': 'choice', 'q': 'What does "pass" do in a loop?', 'options': ['Stops it', 'Nothing', 'Skips one turn'], 'a': 'Nothing'},
        {'id': 114, 'type': 'choice', 'q': 'How many times does range(5, 5) run?', 'options': ['5', '1', '0'], 'a': '0'},
        {'id': 115, 'type': 'choice', 'q': 'Range(0, 10, 2) starts with 0. What is next?', 'options': ['1', '2', '5'], 'a': '2'},
        
    ],
    'box4': [
        {'id': 16, 'type': 'choice', 'q': 'How do you create a list in Python?', 'options': ['(1,2)', '{1,2}', '[1,2]'], 'a': '[1,2]'},
        {'id': 17, 'type': 'choice', 'q': 'What method adds an item to the end of a list?', 'options': ['.add()', '.append()', '.insert()'], 'a': '.append()'},
        {'id': 18, 'type': 'text', 'q': 'What is the index of the first item in a list?', 'a': '0'},
        {'id': 19, 'type': 'text', 'q': 'What function returns the length of a list?', 'a': 'len'},
        {'id': 20, 'type': 'choice', 'q': 'Which one is a Dictionary?', 'options': ['[1,2]', '{"a":1}', '(1,2)'], 'a': '{"a":1}'},
        {'id': 116, 'type': 'choice', 'q': 'Which is an immutable "tuple"?', 'options': ['[1,2]', '(1,2)', '{1,2}'], 'a': '(1,2)'},
        {'id': 117, 'type': 'text', 'q': 'Method to remove a specific item from a list?', 'a': 'remove'},
        {'id': 118, 'type': 'choice', 'q': 'Result of ["a"] * 2?', 'options': ['["a2"]', '["a", "a"]', '["aa"]'], 'a': '["a", "a"]'},
        {'id': 119, 'type': 'text', 'q': 'Method to remove the last item of a list?', 'a': 'pop'},
        {'id': 120, 'type': 'choice', 'q': 'Which symbol accesses a Dictionary value?', 'options': ['my_dict["key"]', 'my_dict("key")', 'my_dict.key'], 'a': 'my_dict["key"]'},
    ],
    'box5': [
        {'id': 26, 'type': 'text', 'q': 'What keyword is used to create a function?', 'a': 'def'},
        {'id': 27, 'type': 'choice', 'q': 'How do you call a function named "my_func"?', 'options': ['call my_func', 'my_func()', 'run my_func'], 'a': 'my_func()'},
        {'id': 28, 'type': 'text', 'q': 'Keyword used to send a value back from a function?', 'a': 'return'},
        {'id': 29, 'type': 'choice', 'q': 'Which is a valid function parameter?', 'options': ['def func(x):', 'def func(5):', 'def func("x"):'], 'a': 'def func(x):'},
        {'id': 30, 'type': 'text', 'q': 'What do we call variables inside the function ()?', 'a': 'parameters'},
        {'id': 121, 'type': 'text', 'q': 'A function that calls itself is called...?', 'a': 'recursion'},
        {'id': 122, 'type': 'choice', 'q': 'What is a "lambda" function?', 'options': ['A long function', 'Anonymous function', 'System function'], 'a': 'Anonymous function'},
        {'id': 123, 'type': 'text', 'q': 'Keyword used to modify a global variable inside a function?', 'a': 'global'},
        {'id': 124, 'type': 'choice', 'q': 'What does a function return if there is no return statement?', 'options': ['0', 'None', 'False'], 'a': 'None'},
        {'id': 125, 'type': 'choice', 'q': 'How do you provide a default value to a parameter?', 'options': ['func(x : 5)', 'func(x = 5)', 'func(default x 5)'], 'a': 'func(x = 5)'},
    ],
    'box6': [
        {'id': 21, 'type': 'text', 'q': 'Keyword to create a class?', 'a': 'class'},
        {'id': 22, 'type': 'text', 'q': 'Name of the constructor method?', 'a': '__init__'},
        {'id': 23, 'type': 'text', 'q': 'Keyword that refers to the instance itself?', 'a': 'self'},
        {'id': 24, 'type': 'text', 'q': 'Concept of hiding data within a class?', 'a': 'encapsulation'},
        {'id': 25, 'type': 'text', 'q': 'Term for a class taking properties from another?', 'a': 'inheritance'},
        {'id': 126, 'type': 'text', 'q': 'What do we call a function that belongs to a class?', 'a': 'method'},
        {'id': 127, 'type': 'choice', 'q': 'How do you create an object from class "Dog"?', 'options': ['d = new Dog()', 'd = Dog()', 'd = class Dog'], 'a': 'd = Dog()'},
        {'id': 128, 'type': 'text', 'q': 'Variable shared by all instances of a class?', 'a': 'class variable'},
        {'id': 129, 'type': 'choice', 'q': 'Which method is called when an object is deleted?', 'options': ['__del__', '__init__', '__stop__'], 'a': '__del__'},
        {'id': 130, 'type': 'text', 'q': 'The process of creating an object from a class?', 'a': 'instantiation'},
    ],
    'box7': [
        {'id': 31, 'type': 'text', 'q': 'What is the term for many forms in OOP?', 'a': 'polymorphism'},
        {'id': 32, 'type': 'choice', 'q': 'Which represents a private variable?', 'options': ['x', '_x', '__x'], 'a': '__x'},
        {'id': 33, 'type': 'text', 'q': 'Class that cannot be instantiated?', 'a': 'abstract'},
        {'id': 34, 'type': 'text', 'q': 'Method to convert object to string?', 'a': '__str__'},
        {'id': 35, 'type': 'choice', 'q': 'Is Python interpreted or compiled?', 'options': ['Compiled', 'Interpreted'], 'a': 'Interpreted'},
        {'id': 131, 'type': 'choice', 'q': 'What does "super()" do?', 'options': ['Calls parent class', 'Closes class', 'Deletes class'], 'a': 'Calls parent class'},
        {'id': 132, 'type': 'text', 'q': 'A method with the same name as parent but different logic?', 'a': 'overriding'},
        {'id': 133, 'type': 'choice', 'q': 'Which checks if an object is an instance of a class?', 'options': ['is_a()', 'isinstance()', 'type_check()'], 'a': 'isinstance()'},
        {'id': 134, 'type': 'text', 'q': 'Standard library to handle dates and times?', 'a': 'datetime'},
        {'id': 135, 'type': 'choice', 'q': 'Which keyword is used to import a library?', 'options': ['use', 'include', 'import'], 'a': 'import'},
    ],
    'box8': [
        {'id': 36, 'type': 'text', 'q': 'Keyword used to skip the rest of a loop iteration?', 'a': 'continue'},
        {'id': 37, 'type': 'text', 'q': 'What is the base class for all classes in Python 3?', 'a': 'object'},
        {'id': 38, 'type': 'choice', 'q': 'Which operator is used for exponentiation (power)?', 'options': ['^', 'exp', '**'], 'a': '**'},
        {'id': 39, 'type': 'text', 'q': 'What is the output of print(2 ** 3)?', 'a': '8'},
        {'id': 40, 'type': 'choice', 'q': 'Which error is raised when a list index is out of range?', 'options': ['KeyError', 'IndexError', 'ValueError'], 'a': 'IndexError'},
        {'id': 136, 'type': 'choice', 'q': 'Block used to handle errors?', 'options': ['try / except', 'do / catch', 'if / error'], 'a': 'try / except'},
        {'id': 137, 'type': 'text', 'q': 'Keyword to force an error to occur?', 'a': 'raise'},
        {'id': 138, 'type': 'choice', 'q': 'Which block always runs after try/except?', 'options': ['catch', 'finally', 'end'], 'a': 'finally'},
        {'id': 139, 'type': 'text', 'q': 'Statement used for debugging/checking conditions?', 'a': 'assert'},
        {'id': 140, 'type': 'choice', 'q': 'Result of 10 // 3 (floor division)?', 'options': ['3', '3.33', '4'], 'a': '3'},
    ]
}

# VIEW FUNCTIONS

def index(request):
    """Signup and Login Terminal Logic."""
    if request.method == "POST":
        form_type = request.POST.get('form_type')
        if form_type == 'signup':
            full_name = request.POST.get('full_name')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            email = request.POST.get('email')
            password = request.POST.get('password')

            # CHECKER: Prevent Duplicate Signups
            if User.objects.filter(username=email).exists():
                messages.error(request, "CRITICAL ERROR: Recruit ID already active.")
                return render(request, 'cq.html')

            user = User.objects.create_user(username=email, email=email, password=password)
            Recruit.objects.create(user=user, full_name=full_name, age=age, gender=gender)
            login(request, user)
            return redirect('quest_selection')

        elif form_type == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('quest_selection')
            else:
               messages.error(request, "INVALID TERMINAL ACCESS: CHECK SEC_KEY")
            return render(request, 'cq.html')
        
    return render(request, 'cq.html')

def check_email_exists(request):
    """API endpoint for real-time username availability check."""
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

@login_required
def quest_selection(request):
    """The Language Selector View."""
    return render(request, 'cq_languages.html', get_recruit_context(request))

@login_required
def python_start(request):
    """The Python Mission Map with Correct Level Status."""
    recruit = request.user.recruit
    context = get_recruit_context(request)
    
    # Passing current_level allows HTML to lock boxes > unlocked_level
    context.update({
        'current_level': recruit.unlocked_level,
        'round_name': "Easy Round" if recruit.unlocked_level <= 3 else "Medium Round"
    })
    return render(request, 'python_quiz.html', context)

@login_required
def level_one_quiz(request, box_num=1):
    """Mission View with Strict Access Control."""
    recruit = request.user.recruit
    
    # LOCK CHECK: Stop users from jumping levels via URL
    if int(box_num) > recruit.unlocked_level:
        messages.warning(request, f"ACCESS DENIED: Box {box_num} is currently locked.")
        return redirect('python_start')

    box_key = f'box{box_num}'
    raw_questions = QUEST_DATA.get(box_key, QUEST_DATA['box1'])
    questions = random.sample(raw_questions, min(len(raw_questions), 5))
    
    context = get_recruit_context(request)
    context.update({
        'questions': questions, 
        'box_num': box_num,
        'current_level': recruit.unlocked_level
    })
    return render(request, 'quiz_level.html', context)

@login_required
def submit_quiz_result(request):
    """Process Mission Success and Update Recruit Progress."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            level = int(data.get('level'))
            is_correct = data.get('is_correct')
            recruit = request.user.recruit
            
            added_exp = 0
            if is_correct:
                if level <= 3: base_xp, farm_xp = 40, 15
                elif level <= 6: base_xp, farm_xp = 80, 35
                else: base_xp, farm_xp = 150, 70
                
                # Check if this is the first completion
                if level not in recruit.completed_levels:
                    recruit.completed_levels.append(level)
                    added_exp = base_xp
                else:
                    added_exp = farm_xp 
                
                recruit.exp += added_exp
                
                # LEVEL UP LOGIC: Automatically unlock next box
                while recruit.exp >= recruit.exp_required:
                    if recruit.unlocked_level < 8:
                        recruit.exp -= recruit.exp_required
                        recruit.unlocked_level += 1
                    else:
                        recruit.exp = recruit.exp_required 
                        break
                recruit.save()

            return JsonResponse({
                'added_exp': added_exp,
                'total_exp': recruit.exp,
                'next_level_at': recruit.exp_required,
                'progress': recruit.progress_percentage,
                'unlocked_level': recruit.unlocked_level,
                'rank': recruit.rank 
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def leaderboard(request):
    recruits = Recruit.objects.all().order_by('-unlocked_level', '-exp')
    context = get_recruit_context(request)
    context.update({'recruits': recruits})
    return render(request, 'leaderboard.html', context)

@login_required
def leaderboard_data(request):
    """Handles the AJAX filtering for the ranking tabs"""
    rank_filter = request.GET.get('rank', 'ALL')
    all_recruits = Recruit.objects.all().order_by('-unlocked_level', '-exp')
    
    filtered_list = []
    for r in all_recruits:
        if rank_filter == 'ALL' or r.rank.upper() == rank_filter.upper():
            filtered_list.append({
                'name': r.full_name,
                'level': r.unlocked_level,
                'exp': r.exp,
                'rank': r.rank
            })
    return JsonResponse({'leaderboard': filtered_list})