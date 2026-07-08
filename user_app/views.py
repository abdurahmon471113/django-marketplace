from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from main.forms import RegisterForm

# render → показывает HTML страницу пользователю
# redirect → отправляет пользователя на другой URL


# UserCreationForm → готовая форма регистрации (username, password1, password2)
# AuthenticationForm → готовая форма логина (проверка username + password)


# login → "включает" пользователя в систему (создаёт сессию)
# logout → "выключает" пользователя (удаляет сессию)


# =========================
# РЕГИСТРАЦИЯ
# =========================
def register_view(request):
    # request → это всё, что пришло от браузера (GET или POST + данные)

    if request.method == "POST":
        # POST = пользователь отправил форму (нажал кнопку "зарегистрироваться")

        form = RegisterForm(request.POST)
        # создаём форму и передаём туда данные, которые ввёл пользователь

        if form.is_valid():
            # проверка:
            # - пароли совпадают
            # - username не занят
            # - нет ошибок

            user = form.save()
            # создаётся новый пользователь в базе данных (таблица auth_user)

            login(request, user)
            # автоматически "входим" этого пользователя (создаётся session)

            return redirect("home")
            # после регистрации отправляем пользователя на главную страницу

    else:
        # GET = пользователь просто открыл страницу регистрации

        form = RegisterForm()
        # пустая форма (чтобы показать поля)

    return render(request, "user_app/register.html", {"form": form})
    # render:
    # берёт HTML файл
    # вставляет туда форму
    # и отправляет готовую страницу в браузер


# =========================
# ЛОГИН
# =========================
def login_view(request):

    form = AuthenticationForm(request, data=request.POST or None)
    # создаём форму логина
    # если POST → берём данные
    # если GET → форма пустая

    if request.method == "POST" and form.is_valid():
        # если пользователь отправил форму И данные правильные

        user = form.get_user()
        # получаем пользователя из базы данных (если он найден)

        login(request, user)
        # создаём сессию → пользователь становится "вошедшим"

        return redirect("home")
        # отправляем на главную страницу

    return render(request, "user_app/login.html", {"form": form})
    # показываем страницу логина (даже если есть ошибки)


# =========================
# ЛОГАУТ
# =========================
def logout_view(request):

    logout(request)
    # удаляем session → пользователь выходит из системы

    return redirect("home")
    # отправляем на главную страницу
