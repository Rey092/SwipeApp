from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from src.estate.models import (
    Advertisement,
    Apartment,
    ApartmentGalleryImage,
    Complaint,
    Complex,
    ComplexBenefits,
    ComplexDocument,
    ComplexGalleryImage,
    ComplexNews,
)
from src.estate.services.serializer_services import update_related_object
from src.users.models import Contact


class ComplexContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "phone", "email"]


class ComplexGalleryImageSerializer(ModelSerializer):
    class Meta:
        model = ComplexGalleryImage
        fields = ["id", "image", "complex"]

    def validate_complex(self, complex_obj):
        """Check that the complex is owned by the current user."""

        user = self.context.get("user")
        if complex_obj.owner is user or user.is_staff:
            return complex_obj
        else:
            raise serializers.ValidationError("Вы не имеете права доступа к данному ЖК")


class ComplexGalleryImageRestrictedSerializer(ComplexGalleryImageSerializer):
    class Meta(ComplexGalleryImageSerializer.Meta):
        read_only_fields = ["complex"]


class ComplexNewsSerializer(ModelSerializer):
    class Meta:
        model = ComplexNews
        fields = ["id", "title", "description", "complex", "created_date"]
        read_only_fields = ["created_date"]

    def validate_complex(self, complex_obj):
        """Check that the complex is owned by the current user."""

        user = self.context.get("user")
        if complex_obj.owner.pk == user.pk or user.is_staff:
            return complex_obj
        else:
            raise serializers.ValidationError("Вы не имеете права доступа к данному ЖК")


class ComplexNewsRestrictedSerializer(ComplexNewsSerializer):
    class Meta(ComplexNewsSerializer.Meta):
        read_only_fields = ["complex", "created_date"]


class ComplexDocumentSerializer(ModelSerializer):
    class Meta:
        model = ComplexDocument
        fields = ["id", "name", "file", "complex"]
        read_only_fields = ["created_date"]

    def validate_complex(self, obj):
        """Check that the complex is owned by the current user."""

        user = self.context.get("user")
        if obj.owner is user or user.is_staff:
            return obj
        else:
            raise serializers.ValidationError("Вы не имеете права доступа к данному ЖК")


class ComplexDocumentRestrictedSerializer(ComplexNewsSerializer):
    class Meta(ComplexNewsSerializer.Meta):
        read_only_fields = ["complex", "created_date"]


class ComplexBenefitsSerializer(ModelSerializer):
    class Meta:
        model = ComplexBenefits
        fields = ["id", "playground", "school", "nursery_school", "parking"]
        read_only_fields = ["created_date"]


class ComplexSerializer(ModelSerializer):
    complex_contact = ComplexContactSerializer(many=False, read_only=False)
    complex_benefits = ComplexBenefitsSerializer(many=False, read_only=False)

    class Meta:
        model = Complex
        fields = ["id", "complex_contact", "name", "address", "map_lat", "map_lng", "is_commissioned",
                  "commission_date", "description", "complex_status", "complex_type", "complex_class", "technology",
                  "territory", "distance_to_sea", "invoice", "ceiling_height", "gas", "heating", "electricity",
                  "sewerage", "water_supply", "formalization", "payment_options", "purpose", "payment_part",
                  "complex_benefits"]
        read_only_fields = ["created_date", "owner"]

    def create(self, validated_data):
        contact_data = validated_data.pop('complex_contact')
        benefits_data = validated_data.pop('complex_benefits')
        complex_obj = Complex.objects.create(**validated_data)

        Contact.objects.create(**contact_data, complex=complex_obj, contact_type="Отдел продаж")
        ComplexBenefits.objects.create(**benefits_data, complex=complex_obj)
        return complex_obj

    def update(self, instance, validated_data):
        update_related_object(self, instance, validated_data, field='complex_contact')
        update_related_object(self, instance, validated_data, field='complex_benefits')

        return super().update(instance, validated_data)


class ApartmentSerializer(ModelSerializer):
    schema = serializers.ImageField(max_length=None, use_url=False, allow_null=True, required=False)
    floor_schema = serializers.ImageField(max_length=None, use_url=False, allow_null=True, required=False)

    class Meta:
        model = Apartment
        fields = "__all__"
        read_only_fields = ["created_date", "owner"]

    def create(self, validated_data):
        apartment_obj = Apartment.objects.create(**validated_data)
        Advertisement.objects.create(apartment=apartment_obj)
        return apartment_obj


class ApartmentDeveloperSerializer(ApartmentSerializer):
    class Meta(ApartmentSerializer.Meta):
        model = Apartment
        read_only_fields = ["id", "address", "map_lat", "map_lng", "moderation_status", "foundation",
                            "purpose", "rooms", "layout", "furnish", "area", "kitchen_area", "has_balcony",
                            "heating_type", "payment_options", "commission", "communication_type", "price",
                            "description", "for_sale", "schema", "floor_schema", "created_date"]


class ApartmentRestrictedSerializer(ApartmentSerializer):
    class Meta(ApartmentSerializer.Meta):
        model = Apartment
        read_only_fields = ["created_date", "owner", "moderation_status", "complex_relation_status", "corpus",
                            "section", "floor", "riser", "owner", "number", "complex", "is_booked"]


class ApartmentGalleryImageSerializer(ModelSerializer):
    class Meta:
        model = ApartmentGalleryImage
        fields = ["id", "apartment", "image"]

    def validate_apartment(self, obj):
        """Check that the complex is owned by the current user."""

        user = self.context.get("user")
        if obj.owner.pk == user.pk or user.is_staff:
            return obj
        else:
            raise serializers.ValidationError("Вы не имеете права доступа к данным Апартаментам")


class ApartmentGalleryImageRestrictedSerializer(ApartmentGalleryImageSerializer):
    class Meta(ApartmentGalleryImageSerializer.Meta):
        read_only_fields = ["apartment"]


class ComplaintSerializer(ModelSerializer):
    apartment = PrimaryKeyRelatedField(queryset=Apartment.objects.all())

    class Meta:
        model = Complaint
        fields = ["id", "text", "apartment", "created_by", "created"]
        read_only_fields = ["apartment", "created_by", "created"]


class ComplaintRestrictedSerializer(ComplaintSerializer):
    class Meta(ComplaintSerializer.Meta):
        model = Complaint
        fields = ["id", "text", "apartment", "created_by", "created"]
        read_only_fields = ["created_by", "created", "is_reviewed"]


class AdvertisementSerializer(ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ["id", "text", "apartment", "add_text", "text", "add_color", "color", "is_big", "is_raisable",
                  "is_turbo", "is_active", "created", "updated", "expiration", "auto_renewal"]
        read_only_fields = ["apartment", "is_active", "created", "updated", "expiration", "auto_renewal"]
