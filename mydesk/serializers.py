from rest_framework.serializers import ModelSerializer
from .models import Project, Task, Comment

class ProjectSerializer(ModelSerializer):

    class Meta:
        model= Project
        fields= '__all__'

    def update(self, instance, validated_data):
        user_ids = validated_data.get('users', None)
        users_list = set(instance.users.values_list('id', flat = True))
        print(users_list)
        project = super().update(instance, validated_data)
        project.users.set(users_list)
        for user_id in user_ids:
            if user_id not in users_list:
                project.users.add(user_id)
        return project
    
class TaskSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'