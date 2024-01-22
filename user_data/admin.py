from django.contrib import admin

from chat.models import Message,Conversation
admin.site.register(Message)
admin.site.register(Conversation)

from expense.models import Expense
admin.site.register(Expense)

from notepad.models import Note
admin.site.register(Note)

from shortlink.models import Link
admin.site.register(Link)

from todo.models import Todo
admin.site.register(Todo)

from storage.models import Storage, GithubInfo
admin.site.register(Storage)
admin.site.register(GithubInfo)