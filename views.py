@login_required
def submit(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    # assuming Exam is linked to Course
    course = exam.course

    # enrollment check (adjust field names if needed)
    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=course
    )

    questions = Question.objects.filter(exam=exam)

    if request.method == "POST":
        submission = Submission.objects.create(
            user=request.user,
            exam=exam,
            enrollment=enrollment
        )

        total_score = 0
        possible_score = 0

        for question in questions:
            choice_id = request.POST.get(str(question.id))

            if not choice_id:
                continue

            choice = get_object_or_404(Choice, id=choice_id)

            # link selected choice to submission
            submission.choices.add(choice)

            # scoring using required method
            if question.is_get_score(choice):
                total_score += question.score

            possible_score += question.score

        submission.total_score = total_score
        submission.possible_score = possible_score
        submission.save()

        return redirect("show_exam_result", result_id=submission.id)

    return render(request, "exam/submit.html", {
        "exam": exam,
        "questions": questions
    })
