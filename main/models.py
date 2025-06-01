from django.db import models
from django.core.validators import RegexValidator,MaxValueValidator,MinValueValidator,FileExtensionValidator
from datetime import datetime as dt, timedelta as td
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
class Person(models.Model):
    name=models.CharField(max_length=50)
    familyName=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    birthdate=models.DateField()
    def __str__(self) -> str:
        return '%s %s'%(self.name,self.familyName)
    class Meta:
        abstract=True
        ordering=['name','familyName']
    
class TutorGrade(models.TextChoices):
    ASST='Assistant'
    ASSOC='Associate'
    PROF='Professor'
    EXPR='Expert'

class Tutor(Person):
    photo=models.ImageField(upload_to='images/tutor_avatars/',blank=True,null=True)
    #1st method to define choices : using a list of tuples
    '''grade=models.CharField(max_length=50,choices=[('ASST','Assistant'),
                                                  ('ASSOC','Associate'),
                                                  ('PROF','Professor'),
                                                  ('EXPR','Expert')],
                                                  default='ASST')
                                                  
    '''
    #2nd method to define choices : using a models.TextChoices class
    grade=models.CharField(max_length=50,choices=TutorGrade.choices,default=TutorGrade.ASST)
    def __str__(self) -> str:
        return f'{super().__str__()} ({self.grade})'
    class Meta:
        db_table='tutors'
def CourseNameValidator(value:str):
    if 'course' not in value.lower() or str(dt.now().year) not in value:
        raise ValidationError('The course name must contain the word "course" and the current year.')
class Course(models.Model):
    #id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100,unique=True,
                          validators=[CourseNameValidator])
    startDate=models.DateField(default=dt.now)
    nbLectures=models.PositiveSmallIntegerField()
    duration=models.DurationField()
    coefficient=models.FloatField(validators=[
                        MinValueValidator(1,'Value must be at list ONE.'),
                        MaxValueValidator(3,'Value must be at most THREE.')
    ])
    courseAvatar=models.ImageField(upload_to='images/course_avatars/',blank=True,null=True,
                                   validators=[FileExtensionValidator(['png','gif'])])
    #relationship between Course and Tutor (1-*)
    tutor=models.ForeignKey(Tutor,on_delete=models.SET_NULL,null=True,
                            related_name='courses')
    def __str__(self) -> str:
        return f'{self.name} ({self.tutor.name} {self.tutor.familyName})'
    
    #redefining the clean method 
    # to validate the course duration and start date
    #duration must be between 21 hours and 84 hours
    #start date must be at least 7 days from now
    def clean(self):
        if self.duration<td(hours=21) or self.duration>td(hours=84):
            raise ValidationError('The course duration must be between 21 and 84 hours.')
        if self.startDate<dt.now().date()+td(days=7):
            raise ValidationError('The course start date must be at least 7 days from now.')

    class Meta:
        db_table='courses'
        ordering=['name'] #order by name in ascending order
        #ordering=['-name'] #order by name in descending order
        #ordering=['startDate','duration','coefficient']

class Student(Person):
    cin = models.CharField(max_length=8, primary_key=True,
                     validators=[RegexValidator(regex=r'^\d{8}$',
                                                message='The CIN must be of 8 digits.'
                                                )
                                ])
    #relationship between Student and Course (*-*) through Enrollement
    courses = models.ManyToManyField(Course, through='Enrollment',
                               through_fields=('student', 'course'),
                               related_name='students')
    class Meta:
        db_table="students"

class Profile(models.Model):
    linkedIn=models.URLField()
    github=models.URLField()
    photo=models.ImageField(upload_to="images/student_images/",null=True, blank=True)
    #relationship between Profile and Student (1-1)
    student=models.OneToOneField(Student,on_delete=models.CASCADE,primary_key=True,
                                 related_name='profile')
    class Meta:
        db_table="profiles"
        ordering=["linkedIn","github"]
class Location(models.Model):
    locationNumber=models.CharField(max_length=10)
    streetName=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    zipCode=models.CharField(max_length=10)
    #relationship between Location and Course (*-*)
    #this line will create a table named locations_courses (The association table)
    #related_name : the name of the reverse relation from the related object back to this one
    courses=models.ManyToManyField(Course,db_table='courses_locations',
                                   related_name='locations')
    class Meta:
        db_table="locations"
        constraints=[models.UniqueConstraint(
            fields=["locationNumber","streetName","zipCode"],
            name="unique_location"
        )]
class Enrollment(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    registrationDate=models.DateField(auto_now_add=True)
    result=models.FloatField()
    def __str__(self) -> str:
        return self.student.cin+"-"+self.course.name
    class Meta:
        db_table="enrollments"
        constraints=[models.UniqueConstraint(
            fields=["student","course"],
            name="unique_enrollment_student_course"
        )]
        ordering=["registrationDate"]

class AdminTheme(models.Model):
    name = models.CharField(max_length=100, unique=True)
    css_url = models.URLField(blank=True, null=True, validators=[URLValidator()])
    js_url = models.URLField(blank=True, null=True, validators=[URLValidator()])
    scss_file = models.FileField(upload_to='admin_themes_source/%Y/%m/%d/', blank=True, null=True, validators=[FileExtensionValidator(['scss'])])
    js_file = models.FileField(upload_to='admin_themes_source/%Y/%m/%d/', blank=True, null=True, validators=[FileExtensionValidator(['js'])])
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    accessibility_suggestions = models.TextField(blank=True, null=True)

    def clean(self):
        if self.css_url and not self.css_url.endswith('.css'):
            raise ValidationError({'css_url': 'CSS URL must end with .css'})
        if self.js_url and not self.js_url.endswith('.js'):
            raise ValidationError({'js_url': 'JS URL must end with .js'})
        if not (self.css_url or self.scss_file):
            raise ValidationError('Either a CSS URL or an SCSS file must be provided.')
        if not (self.js_url or self.js_file):
            raise ValidationError('Either a JS URL or a JS file must be provided.')

    def __str__(self):
        return self.name