from django.shortcuts import render,redirect
from .forms import FeedbackForm
from django.http import Http404, request

resources = [
    {
        "id": 1,
        "title": "CheckiO (Python)",
        "type": "Game",
        "description": "Explore floating islands by solving Python coding puzzles, building functions, and advancing your hero through levels.",
        "url": "https://py.checkio.org/",
        "image": "resources/checkio.png"
    },
    {
        "id": 2,
        "title": "CodinGame (Python / JS)",
        "type": "Game",
        "description": "Play action-packed arcade games and puzzles where your code controls the gameplay and characters in real-time.",
        "url": "https://www.codingame.com/",
        "image": "resources/codingame.png"
    },
    {
        "id": 3,
        "title": "Flexbox Froggy (CSS)",
        "type": "Game",
        "description": "Help Froggy and his friends reach their lilypads by writing real CSS Flexbox layout code in interactive puzzles.",
        "url": "https://flexboxfroggy.com/",
        "image": "resources/flexbox-froggy.jpg"
    },
    {
        "id": 4,
        "title": "CSS Grid Garden (CSS)",
        "type": "Game",
        "description": "Water your carrot garden and clear weeds by writing CSS Grid code across 28 fun, puzzle-filled levels.",
        "url": "https://cssgridgarden.com/",
        "image": "resources/grid-garden.jpeg"
    },
    {
        "id": 5,
        "title": "CodeCombat (JavaScript / Python)",
        "type": "Game",
        "description": "Control your hero's movements, attacks, and magic spells by writing real code to battle through dungeon levels.",
        "url": "https://codecombat.com/",
        "image": "resources/codecombat.webp"
    },
    {
        "id": 6,
        "title": "Elevator Saga (JavaScript)",
        "type": "Game",
        "description": "Program the algorithms for an elevator system using JavaScript to transport passengers efficiently without overloading.",
        "url": "http://play.elevatorsaga.com/",
        "image": "resources/elevator-saga.png"
    }
]

def feedback(request):
    theme = get_theme(request)

    if request.method == "POST":
        form = FeedbackForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            rating = form.cleaned_data["rating"]

            print(name)
            print(email)
            print(message)
            print(rating)

            return redirect("feedback_thanks")

    else:
        form = FeedbackForm()

    return render(
        request,
        "core/feedback.html",
        {
            "form": form,
            "theme": theme
        }
    )


def feedback_thanks(request):
    theme = get_theme(request)

    return render(
        request,
        "core/feedback_thanks.html",
        {
            "theme": theme
        }
    )
    
def home_view(request):

    theme = get_theme(request)

    return render(
        request,
        "core/home.html",
        {
            "theme": theme,
        }
    )

def resource_list(request):

    theme = get_theme(request)

    return render(
        request,
        "core/resource_list.html",
        {
            "resources": resources,
            "theme": theme,
        }
    )


def resource_detail(request, id):
    theme = get_theme(request)
    for resource in resources:
        if resource["id"] == id:
            return render(
                request,
                "core/resource_detail.html",
                {
                    "resource": resource,
                    "theme": theme
                }
            )

    return render(
                request,
                "core/404.html",
                {
                    "theme": theme
                },
                status=404
            )




def get_theme(request):
    theme = request.COOKIES.get("theme")

    if theme not in ["light", "dark"]:
        theme = "light"

    return theme


def preferences(request):

    theme = get_theme(request)

    if request.method == "POST":

        selected_theme = request.POST.get("theme")

        if selected_theme not in ["light", "dark"]:
            selected_theme = "light"

        response = redirect("preferences")

        response.set_cookie(
            "theme",
            selected_theme,
            max_age=60 * 60 * 24 * 30
        )

        return response

    return render(
        request,
        "core/preferences.html",
        {
            "theme": theme,
        }
    )
    
    
def toggle_favorite(request, id):

    # Check that the resource exists
    resource_exists = any(
        resource["id"] == id
        for resource in resources
    )

    if not resource_exists:
        raise Http404("Resource not found")

    # Get favorites from the session
    favorites = request.session.get("favorites", [])

    # Add or remove the ID
    if id in favorites:
        favorites.remove(id)
    else:
        favorites.append(id)

    # Save the updated list
    request.session["favorites"] = favorites

    return redirect("resource_detail", id=id)


# VIEW FAVORITES
def favorites(request):
    theme = get_theme(request)

    favorite_ids = request.session.get("favorites", [])

    favorite_resources = []

    for resource in resources:
        if resource["id"] in favorite_ids:
            favorite_resources.append(resource)

    return render(
        request,
        "core/favorites.html",
        {
            "favorites": favorite_resources,
            "theme": theme
        }
    )