from re import L
import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Notes, Labels

class LabelType(DjangoObjectType):
    class Meta:
        model = Labels

class NoteType(DjangoObjectType):
    class Meta:
        model = Notes

class Query(graphene.ObjectType):
    all_notes = graphene.List(NoteType)
    specific_note = graphene.Field(NoteType, slug=graphene.String())
    all_labels = graphene.List(LabelType)
    specific_label = graphene.Field(LabelType, slug=graphene.String())
    
    # all_notes
    def resolve_all_notes(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('User is not authenticated')
        return Notes.objects.filter(user=user)
    
    # specific_note
    def resolve_specific_note(self, info, slug):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('User is not authenticated')
        return Notes.objects.get(user=user, slug=slug)
    
    # all_labels
    def resolve_all_labels(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('User is not authenticated')
        return Labels.objects.filter(user=user)
        
    # specific_label
    def resolve_specific_label(self, info, slug):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('User is not authenticated')
        return Labels.objects.get(user=user, slug=slug)
    
    
# mutations

# Label mutations
class CreateLabelMutation(graphene.Mutation):
    class Arguments:
        label = graphene.String(required=True)
    
    label = graphene.Field(LabelType)
    
    def mutate(self, info, label):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('User is not authenticated')
        label = Labels(user=user, label=label)
        label.save()
        return CreateLabelMutation(label=label)
    
class UpdateLabelMutation(graphene.Mutation):
    class Arguments:
        slug = graphene.String(required=True)
        label = graphene.String(required=True)
    
    label = graphene.Field(LabelType)
    
    def mutate(self, info, slug, label):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('User is not authenticated')
        getLabel = Labels.objects.get(user=user, slug=slug)
        getLabel.label = label
        getLabel.save()
        return UpdateLabelMutation(label=getLabel)
    
class DeleteLabelMutation(graphene.Mutation):
    class Arguments:
        slug = graphene.String(required=True)
    
    success = graphene.Boolean()
    
    def mutate(self, info, slug):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('User is not authenticated')
        getLabel = Labels.objects.get(user=user, slug=slug)
        getLabel.delete()
        return DeleteLabelMutation(success=True)
    
# Note Mutations
class CreateNoteMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=False)
        labels = graphene.List(graphene.String, required=False)
    
    note = graphene.Field(NoteType)
    
    def mutate(self, info, title,**kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('User is not authenticated')
        content = kwargs.get('content', None)
        labels = kwargs.get('labels', None)
        note = Notes(user=user, title=title)
        note.save()
        if content:
            note.content = content
        if labels:
            for label in labels:
                get_or_create_label = Labels.objects.get_or_create(user=user, label=label)
                note.labels.add(get_or_create_label[0])
        note.save()
        return CreateNoteMutation(note=note)
        
class UpdateNoteMutation(graphene.Mutation):
    class Arguments:
        slug = graphene.String(required=True)
        title = graphene.String(required=False)
        content = graphene.String(required=False)
        labels = graphene.List(graphene.String, required=False)
        
    note = graphene.Field(NoteType)
    
    def mutate(self, info, slug, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('User is not authenticated')
        title = kwargs.get('title', None)
        content = kwargs.get('content', None)
        labels = kwargs.get('labels', None)
        getNote = Notes.objects.get(user=user, slug=slug)
        if title:
            getNote.title = title
        if content:
            getNote.content = content
        if labels:
            getNote.labels.clear()
            for label in labels:
                get_or_create_label = Labels.objects.get_or_create(user=user, label=label)
                getNote.labels.add(get_or_create_label[0])
        getNote.save()
        return UpdateNoteMutation(note=getNote)
    
class DeleteNoteMutation(graphene.Mutation):
    class Arguments:
        slug = graphene.String(required=True)
    
    success = graphene.Boolean()
    
    def mutate(self, info, slug):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('User is not authenticated')
        note = Notes.objects.get(user=user, slug=slug)
        note.delete()
        return DeleteNoteMutation(success=True)
    
class Mutation(graphene.ObjectType):
    # labels
    add_label = CreateLabelMutation.Field()
    update_label = UpdateLabelMutation.Field()
    delete_label = DeleteLabelMutation.Field()
    # note
    create_note = CreateNoteMutation.Field()
    update_note = UpdateNoteMutation.Field()
    delete_note = DeleteNoteMutation.Field()