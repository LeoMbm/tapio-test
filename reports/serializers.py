from rest_framework import serializers

from reports.models import ReportModel, SourceModel


class ReportSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    date = serializers.DateField()

    class Meta:
        model = ReportModel
        fields = '__all__'

    def create(self, validated_data):
        return ReportModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance


class SourceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField()
    value = serializers.FloatField()
    emission_factor = serializers.FloatField()
    total_emission = serializers.FloatField(read_only=True)
    lifetime = serializers.IntegerField()
    acquisition_year = serializers.IntegerField()
    report = serializers.PrimaryKeyRelatedField(queryset=ReportModel.objects.all())

    class Meta:
        model = SourceModel
        fields = '__all__'

    # def create(self, validated_data):
    #     value = validated_data['value']
    #     emission_factor = validated_data['emission_factor']
    #     total_emission = value * emission_factor
    #     validated_data['total_emission'] = total_emission
    #     source = SourceModel.objects.create(**validated_data)
    #     return source


class SourceDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SourceModel
        fields = '__all__'
        depth = 1