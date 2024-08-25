from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Choice, UserAnswer


def calculate_grade(correct_answers, total_questions):
    score_percentage = round((correct_answers / total_questions) * 100)

    if score_percentage >= 90:
        return 'A+'
    elif score_percentage >= 80:
        return 'A'
    elif score_percentage >= 70:
        return 'B'
    elif score_percentage >= 60:
        return 'C'
    elif score_percentage >= 50:
        return 'D'
    elif score_percentage >= 40:
        return 'E'
    else:
        return 'F'


@login_required
def quiz_select(request):
    user = request.user

    # Get all quizzes
    quizzes = Quiz.objects.all()

    # List to store quizzes with their grades
    quizzes_with_grades = []

    # Calculate the grade for each completed quiz
    for quiz in quizzes:
        user_answers = UserAnswer.objects.filter(user=user, quiz=quiz)
        if user_answers.count() == quiz.questions.count():  # Check if the quiz is completed
            total_questions = quiz.questions.count()
            correct_answers = user_answers.filter(is_correct=True).count()
            grade = calculate_grade(correct_answers, total_questions)
            quizzes_with_grades.append({'quiz': quiz, 'grade': grade})
        else:
            quizzes_with_grades.append({'quiz': quiz, 'grade': None})

    context = {
        'quizzes_with_grades': quizzes_with_grades,
    }

    return render(request, 'quiz/quiz_select.html', context)


@login_required
def quiz_take(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    user = request.user

    # Get the list of questions for the quiz
    questions = quiz.questions.all()

    # Find the current question to answer
    user_answers = UserAnswer.objects.filter(user=user, quiz=quiz)
    if user_answers.exists():
        answered_question_ids = user_answers.values_list('question_id', flat=True)
        next_question = questions.exclude(id__in=answered_question_ids).first()
    else:
        next_question = questions.first()

    # If all questions are answered, redirect to the report
    if not next_question:
        return redirect('quiz_report', pk=quiz.pk)

    # Calculate the current question number for display
    question_number = questions.filter(id__lte=next_question.id).count()

    # Handle the POST request (submitting an answer)
    if request.method == 'POST':
        selected_choice_id = request.POST.get('choice')
        if selected_choice_id:  # Ensure a choice was selected
            selected_choice = get_object_or_404(Choice, id=selected_choice_id)
            is_correct = selected_choice.is_correct

            # Save the user's answer
            UserAnswer.objects.create(
                user=user,
                quiz=quiz,
                question=next_question,
                selected_choice=selected_choice,
                is_correct=is_correct
            )

            # Redirect to the same view to move to the next question
            return redirect('quiz_take', pk=quiz.pk)

    # Render the current question
    context = {
        'quiz': quiz,
        'question': next_question,
        'choices': next_question.choices.all(),
        'question_number': question_number,
        'total_questions': questions.count()
    }
    return render(request, 'quiz/quiz_take.html', context)


@login_required
def quiz_report(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    user = request.user

    # Get the user's answers for this quiz
    user_answers = UserAnswer.objects.filter(user=user, quiz=quiz)

    # Redirect to the quiz if it's not yet completed
    if user_answers.count() < quiz.questions.count():
        return redirect('quiz_take', pk=quiz.pk)

    # Calculate score and grade
    total_questions = quiz.questions.count()
    correct_answers = user_answers.filter(is_correct=True).count()
    score_percentage = round((correct_answers / total_questions) * 100)

    if score_percentage >= 90:
        letter_grade = 'A+'
    elif score_percentage >= 80:
        letter_grade = 'A'
    elif score_percentage >= 70:
        letter_grade = 'B'
    elif score_percentage >= 60:
        letter_grade = 'C'
    elif score_percentage >= 50:
        letter_grade = 'D'
    elif score_percentage >= 40:
        letter_grade = 'E'
    else:
        letter_grade = 'F'

    # Prepare the correct answers
    for answer in user_answers:
        answer.correct_choice = answer.question.choices.filter(is_correct=True).first()

    # Context for rendering the template
    context = {
        'quiz': quiz,
        'user_answers': user_answers,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'score_percentage': score_percentage,
        'letter_grade': letter_grade,
    }

    return render(request, 'quiz/quiz_report.html', context)
