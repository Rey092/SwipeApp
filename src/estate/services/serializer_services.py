
def update_related_object(serializer, instance, validated_data, field):
    if 'complex_benefits' in validated_data:
        benefits_serializer = serializer.fields[field]
        benefits_instance = getattr(instance, field)
        benefits_data = validated_data.pop(field)
        benefits_serializer.update(benefits_instance, benefits_data)
