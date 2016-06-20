from game import views


urlpatterns = [
    url(r'^game/', game.views.index),
]
