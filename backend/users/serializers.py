from rest_framework import serializers

from .models import User, Subscription


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, author=obj.id).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    #recipes = serializers.SerializerMethodField()
    #recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    #def get_recipes(self, obj):
    #    request = self.context.get('request')
    #    limit = request.GET.get('recipes_limit')
    #    queryset = Recipe.objects.filter(author=obj.author)
    #    if limit:
    #        queryset = queryset[:int(limit)]
    #    return CropRecipeSerializer(queryset, many=True).data

    #def get_recipes_count(self, obj):
    #    return Recipe.objects.filter(author=obj.author).count()
