from django.urls import path
from .views import MessagesConversationView, ConversationPriveeView, MessageVocalView

urlpatterns = [
    path("friends/messages/<int:conversation_id>/", MessagesConversationView.as_view()),
    path("friends/conversation/<int:user_id>/", ConversationPriveeView.as_view()),
    path("friends/message-vocal/", MessageVocalView.as_view()),

]
