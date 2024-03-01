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

from storage.models import File,Folder
admin.site.register(File)
admin.site.register(Folder)


from photu.models import Photo,Repo
admin.site.register(Photo)
admin.site.register(Repo)

from git.models import FileInfo,Chunk
admin.site.register(FileInfo)
admin.site.register(Chunk)