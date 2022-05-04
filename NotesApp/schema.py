import graphene
from users.schema import Query as UserQuery, Mutation as UserMutation
from notes.schema import Query as NotesQuery, Mutation as NotesMutation

class Query(UserQuery, NotesQuery):
    pass

class Mutation(UserMutation, NotesMutation):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)