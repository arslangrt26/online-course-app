# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Exam, Question, Result


@login_required
def submit(request, exam_id):
    """
    Handles exam submission.
    Calculates score and saves result.
    """
    exam = get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.filter(exam=exam)

    if request.method == "POST":
        score = 0
        total = questions.count()

        for question in questions:
            selected_answer = request.POST.get(str(question.id))

            # assuming correct_answer is stored in question.correct_option
            if selected_answer == question.correct_option:
                score += 1

        result = Result.objects.create(
            user=request.user,
            exam=exam,
            score=score,
            total=total
        )

        return redirect("show_exam_result", result_id=result.id)

    return render(request, "exam/submit.html", {
        "exam": exam,
        "questions": questions
    })


@login_required
def show_exam_result(request, result_id):
    """
    Displays the exam result to the user.
    """
    result = get_object_or_404(Result, id=result_id, user=request.user)

    percentage = 0
    if result.total > 0:
        percentage = (result.score / result.total) * 100

    return render(request, "exam/result.html", {
        "result": result,
        "percentage": percentage
    })
