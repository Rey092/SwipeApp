from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from src.estate.models import Complex
from src.users.models import Contact


class ComplexContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "phone", "email"]


# @extend_schema_serializer(
#     examples=[
#         OpenApiExample(
#             "Nmae",
#             value={
#                 "ceiling_height": 1.5,
#             },
#             request_only=True,  # signal that example only applies to requests
#             response_only=False,  # signal that example only applies to responses
#         ),
#     ],
# )
class ComplexSerializer(serializers.ModelSerializer):
    complex_contact = ComplexContactSerializer(many=False, read_only=False)

    class Meta:
        model = Complex
        fields = ["complex_contact", "name", "address", "map_lat", "map_lng", "is_commissioned", "commission_date",
                  "description", "complex_status", "complex_type", "complex_class", "technology", "territory",
                  "distance_to_sea", "invoice", "ceiling_height", "gas", "heating", "electricity", "sewerage",
                  "water_supply", "formalization", "payment_options", "purpose", "payment_part"]
        read_only_fields = ["id", "created_date", "owner"]

    def create(self, validated_data):
        contact_data = validated_data.pop('complex_contact')
        complex_obj = Complex.objects.create(**validated_data)
        Contact.objects.create(**contact_data, complex=complex_obj, contact_type="Отдел продаж")
        return complex_obj
