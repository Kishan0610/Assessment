from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'updated_at']
        read_only_fields = ['created_at', 'created_by', 'updated_at']

class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()
    users = UserSerializer(many=True)
    created_by = serializers.StringRelatedField()
    
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']
        read_only_fields = ['created_at', 'created_by']

class ClientDetailSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()
    created_by = serializers.StringRelatedField()
    
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']
    
    def get_projects(self, obj):
        projects = obj.projects.all()
        return ProjectSerializer(projects, many=True).data

class ProjectCreateSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    class Meta:
        model = Project
        fields = ['project_name', 'users']
    
    def create(self, validated_data):
        users = validated_data.pop('users')
        project = Project.objects.create(
            project_name=validated_data['project_name'],
            client=self.context['client'],
            created_by=self.context['request'].user
        )
        project.users.set(users)
        return project