from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, APIException
from .models import (
    JobSeeker, Company, Location, Industry, Language,
    Certification, Education, Skill, CareerHistory
)
from .serializers import (
    UserSerializer, JobSeekerSerializer, CompanySerializer,
    LocationSerializer, IndustrySerializer, LanguageSerializer,
    CertificationSerializer, EducationSerializer, SkillSerializer,
    CareerHistorySerializer,
    UserRegistrationSerializer, JobSeekerSerializer2
)
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer 
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()  # Create the user
        # Check if the user type is JobSeeker before creating a JobSeeker instance
        if user.user_type == 'Job Seeker':
            JobSeeker.objects.create(user=user)

        elif user.user_type == 'Employer':
            # Get company data from request payload
            company_data = self.request.data
            industry_id = company_data.get('industry_id')
            industry = Industry.objects.get(id=industry_id)
            logo = self.request.FILES.get('logo')  # Correctly handle the uploaded logo file
            Company.objects.create(
                user=user,
                company_name=company_data.get('company_name'),
                company_email=company_data.get('company_email'),
                company_size=company_data.get('company_size'),
                website=company_data.get('website'),
                description=company_data.get('description'),
                industry=industry,
                registration_number=company_data.get('registration_number'),
                logo=logo,  # Save the uploaded logo file
            )

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

class JobSeekerListCreateView(generics.ListCreateAPIView):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer2
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class JobSeekerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer2
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method == 'PATCH' or self.request.method == 'PUT' or self.request.method == 'POST':
            return JobSeekerSerializer
        return JobSeekerSerializer2
    

class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT', 'POST']:
            return CompanySerializer  # Use the same serializer for updates
        return CompanySerializer  # Default to the same serializer for retrieval

class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class IndustryListCreateView(generics.ListCreateAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class LanguageListCreateView(generics.ListCreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

class CertificationListCreateView(generics.ListCreateAPIView):
    serializer_class = CertificationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Get certification records associated with the user's JobSeeker profile
        return Certification.objects.filter(jobseeker__user=self.request.user)

    def perform_create(self, serializer):
        # Get the JobSeeker instance for the authenticated user
        try:
            job_seeker = JobSeeker.objects.get(user=self.request.user)
        except JobSeeker.DoesNotExist:
            raise ValidationError("You must have a JobSeeker profile to add certification records.")
        
        # Create the certification record
        certification = serializer.save()
        # Add it to the JobSeeker's certifications
        job_seeker.certifications.add(certification)

class EducationListCreateView(generics.ListCreateAPIView):
    serializer_class = EducationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Get education records associated with the user's JobSeeker profile
        return Education.objects.filter(jobseeker__user=self.request.user)

    def perform_create(self, serializer):
        # Get the JobSeeker instance for the authenticated user
        try:
            job_seeker = JobSeeker.objects.get(user=self.request.user)
        except JobSeeker.DoesNotExist:
            raise APIException("You must have a JobSeeker profile to add education records.")
        
        # Check if the user already has this specific education record
        if job_seeker.education.filter(course_or_qualification=serializer.validated_data['course_or_qualification']).exists():
            raise APIException("You have already added an education record for this course or qualification.")
        
        # Create the education record
        education = serializer.save()
        # Add it to the JobSeeker's education
        job_seeker.education.add(education)

class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = (permissions.IsAuthenticated,)

class CareerHistoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CareerHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Get career history records associated with the user's JobSeeker profile
        return CareerHistory.objects.filter(job_seeker__user=self.request.user)
    
    def perform_create(self, serializer):
        # Get the JobSeeker instance for the authenticated user
        try:
            job_seeker = JobSeeker.objects.get(user=self.request.user)
        except JobSeeker.DoesNotExist:
            raise APIException("You must have a JobSeeker profile to add career history records.")
        
        # Get the new career history data
        new_start_date = serializer.validated_data.get('start_date')
        new_end_date = serializer.validated_data.get('end_date')

        # Check if there is an ongoing career history record
        ongoing_records = job_seeker.career_history.filter(end_date__isnull=True)
        if ongoing_records.exists():
            raise APIException("You must end your current career history before adding a new one.")

        # Check for overlapping career history records
        overlapping_records = job_seeker.career_history.filter(
            (Q(start_date__lte=new_end_date) & Q(end_date__gte=new_start_date)) |
            (Q(start_date__gte=new_start_date) & Q(end_date__lte=new_end_date))
        )

        if overlapping_records.exists():
            raise APIException("The new career history overlaps with existing records. Please adjust the dates.")

        # Create the career history record
        career_history = serializer.save()
        # Add it to the JobSeeker's career history
        job_seeker.career_history.add(career_history)



@api_view(['GET'])
def is_jobseeker(request):
    is_jobseeker = JobSeeker.objects.filter(user=request.user).exists()
    return Response({'is_jobseeker': is_jobseeker})

@api_view(['GET'])
def is_company(request):
    is_company = Company.objects.filter(user=request.user).exists()
    return Response({'is_company': is_company})

class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        # Get the JobSeeker instance for the authenticated user
        try:
            job_seeker = JobSeeker.objects.get(user=self.request.user)
        except JobSeeker.DoesNotExist:
            raise APIException("You must have a JobSeeker profile to add skills records.")
        
        # Create the skill record
        skill = serializer.save()
        # Add it to the JobSeeker's skills
        job_seeker.skills.add(skill)

class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CareerHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CareerHistory.objects.all()
    serializer_class = CareerHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)


class CertificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = (permissions.IsAuthenticated,)

class FeaturedCompanyListView(generics.ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Company.objects.filter(is_verified=True).order_by('-id')

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CompanyListView(generics.ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Company.objects.filter(is_verified=True).order_by('-id')
        search = self.request.query_params.get('search', None)
        industry = self.request.query_params.get('industry', None)

        if search:
            queryset = queryset.filter(
                Q(company_name__icontains=search) |
                Q(description__icontains=search)
            )
        
        if industry:
            queryset = queryset.filter(industry__id=industry)

        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, self.request)
        return paginated_queryset
