from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

GRADE_LEVELS = [
    ("Preschool", "Preschool"),
    ("Grade 1", "Grade 1"),
    ("Grade 2", "Grade 2"),
    ("Grade 3", "Grade 3"),
    ("Grade 4", "Grade 4"),
    ("Grade 5", "Grade 5"),
    ("Grade 6", "Grade 6"),
]
GRADE_LEVEL_VALUES = [g[0] for g in GRADE_LEVELS]

LEVEL_GROUPS = [
    ("Preschool", "Preschool"),
    ("Elementary", "Elementary"),
]

ELEMENTARY_GRADES = ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6"]


def grades_for_level_group(level_group):
    if level_group == "Preschool":
        return ["Preschool"]
    return ELEMENTARY_GRADES


# Colors the in-game color-detector recognizes. Each color can only belong to
# ONE active student at a time so the detector can tell students apart.
COLOR_PALETTE = [
    ("Red", "#E8493C"),
    ("Blue", "#3B7CB0"),
    ("Green", "#5DBB8E"),
    ("Yellow", "#F2C94C"),
    ("Purple", "#9B6FDE"),
    ("Orange", "#F2994A"),
    ("Teal", "#4DAEB0"),
    ("Pink", "#E8887A"),
    ("Brown", "#A97155"),
    ("Cyan", "#5BA9C4"),
    ("Lime", "#9ABF5C"),
    ("Magenta", "#C1558B"),
]


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    class_name = models.CharField(max_length=120, blank=True)

    def display_name(self):
        return self.user.get_full_name() or self.user.username

    def __str__(self):
        return self.display_name()


class Student(models.Model):
    GENDER_CHOICES = [("Male", "Male"), ("Female", "Female")]

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="students")
    name = models.CharField(max_length=120)
    grade = models.CharField(max_length=20, choices=GRADE_LEVELS)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    color_name = models.CharField(max_length=20)
    color_hex = models.CharField(max_length=7)
    points = models.PositiveIntegerField(default=0)
    badges = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def latest_attempt(self):
        return self.attempts.order_by("-played_at").first()

    @property
    def average_score(self):
        agg = self.attempts.aggregate(models.Avg("score"))["score__avg"]
        return round(agg) if agg is not None else None


class Quiz(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=150)
    subject = models.CharField(max_length=80, default="New")
    level_group = models.CharField(max_length=20, choices=LEVEL_GROUPS)
    source_filename = models.CharField(max_length=255, blank=True)
    source_file = models.FileField(upload_to="lesson_files/", blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def average_score(self):
        agg = self.attempts.aggregate(models.Avg("score"))["score__avg"]
        return round(agg) if agg is not None else None

    @property
    def wrong_count(self):
        """Students who scored below the 'mastered' threshold on this quiz."""
        return self.attempts.filter(score__lt=60).count()

    @property
    def total_attempts(self):
        return self.attempts.count()


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text[:50]


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text


class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attempts")
    score = models.PositiveIntegerField(help_text="Percentage score, 0-100")
    played_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-played_at"]

    @property
    def status(self):
        return "Great" if self.score >= 60 else "Needs Support"

    def __str__(self):
        return f"{self.student} \u00b7 {self.quiz} \u00b7 {self.score}%"
