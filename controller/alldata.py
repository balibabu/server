from todo.models import Todo
from todo.serializers import TodoSerializer
from notepad.models import Note
from notepad.serializers import NoteSerializer
from expense.models import Expense
from expense.serializers import ExpenseSerializer

def get_all_data(user):
    todos=Todo.objects.filter(user=user)
    todoSer = TodoSerializer(todos, many=True)
    notes=Note.objects.filter(user=user)
    noteSer = NoteSerializer(notes, many=True)
    expenses=Expense.objects.filter(user=user)
    expenseSer = ExpenseSerializer(expenses, many=True)
    
    data={
        "username":user.username,
        "userid":user.id,
        "todo":todoSer.data,
        "note":noteSer.data,
        "expense":expenseSer.data
    }
    return data