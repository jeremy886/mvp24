from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "E", "Easy"
        MEDIUM = "M", "Medium"
        HARD = "H", "Hard"

    text = models.TextField('question')
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
    difficulty = models.CharField(
        max_length=1,
        choices=Difficulty.choices,
        blank=True,
        default=Difficulty.MEDIUM,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question: {self.text}"


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )
    text = models.TextField('choice')
    is_correct = models.BooleanField(default=False)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"Choice: {self.text}"


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    questions = models.ManyToManyField(
        Question,
        related_name="quizzes",
    )
    max_questions = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"Quiz: {self.title}"

    class Meta:
        verbose_name_plural = "Quizzes"  # ensures Admin UI displays the plural name correctly

    def get_questions(self):
        return self.questions.all()

    def add_question(self, question):
        if self.questions.count() >= self.max_questions:
            raise ValueError(f"Cannot add more than {self.max_questions} questions to this quiz.")
        self.questions.add(question)


class UserAnswer(models.Model):
    """
    Need to consider how to calculate the percentage score and letter grade
    Method 1: Client side using Javascript or HTMX
    Method 2: Server side using @perperty
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_answers')
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    selected_choice = models.ForeignKey('Choice', on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"Answer for Question ID {self.question.id} by {self.user.username}"
