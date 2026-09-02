from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/upload/", views.upload_quiz, name="upload_quiz"),

    path("students/", views.students_view, name="students"),
    path("students/<int:pk>/remove/", views.remove_student, name="remove_student"),

    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("quizzes/", views.scoreboard, name="scoreboard"),
    path("quizzes/<int:pk>/edit/", views.edit_questions, name="edit_questions"),
    path("quizzes/<int:pk>/publish/", views.publish_quiz, name="publish_quiz"),
    path("quizzes/<int:pk>/questions/add/", views.add_question, name="add_question"),
    path("quizzes/<int:pk>/questions/<int:question_id>/delete/", views.delete_question, name="delete_question"),

    path("student-scores/", views.student_scores, name="student_scores"),
    path("performance/", views.performance, name="performance"),
]
